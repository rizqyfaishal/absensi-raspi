from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Referensi, Absensi, Matkul, Enrollment, Jadwal, WrongClass
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.http import Http404
from django.db import IntegrityError
from datetime import datetime, time, date
import secrets
import requests
import json


def send_email(nama, email, random_text, jam):
	try:
		send = send_mail(
			'Konfirmasi',
			'Selamat ! Tekan Link Disamping-> <a href="localhost:absensikampus.herokuapp.com/absensi/konfirmasi/' + random_text
				+ '">Konfirmasi</a>' + str(jam),
			'absensi@vektorprojects.com',
			[email],
			fail_silently=False
		)
		return send
	except BadHeaderError:
		return 0

def send_email_salah_kelas(nama, email):
	try:
		send = send_mail(
			'Salah Kelas',
			'Anda salah kelas',
			'absensi@vektorprojects.com',
			[email],
			fail_silently=False
		)
		return send
	except BadHeaderError:
		return 0


@csrf_exempt
def get_mac_address_data_from_raspi(request):
	data_to_return = []
	try:
		req = json.loads(request.body)
		ruangan = req['ruangan']
		timestamp_raspi = int(req['timestamp_raspi'])
		raspi_datetime = datetime.fromtimestamp(timestamp_raspi)
		raspi_time = raspi_datetime.time()
		week_day = raspi_datetime.weekday()
		jadwal_kuliah = Jadwal.objects.filter(
			ruangan=ruangan, 
			hari=week_day,
			mulai__lte=raspi_time,
			selesai__gte=raspi_time).first()
		print(jadwal_kuliah)
		print(week_day)
		print(raspi_time)
		print(str(raspi_datetime))
		if jadwal_kuliah is not None:
			# referensis = Referensi.objects.filter(
			# 	mac_address__in=req['mac_address'],
			# 	enrollment__matkul=jadwal_kuliah.matkul)
			referensis = Referensi.objects.filter(
				mac_address__in=req['mac_address']
			)
			print(referensis)
			if len(referensis) > 0:
				curr_date = date.today()
				referensi_match_class = []
				referensi_wrong_class = []
				for ref in referensis:
					matkuls = [enroll.matkul for enroll in ref.enrollment_set.all()]
					print(matkuls)
					if jadwal_kuliah.matkul in matkuls:
						referensi_match_class.append(ref)
					else:
						wc = WrongClass.objects.filter(
							referensi=ref, 
							jadwal=jadwal_kuliah,
							timestamp__gte=datetime(curr_date.year, curr_date.month, curr_date.day)
						).first()
						if wc is None:
							referensi_wrong_class.append(ref)
							created_wc = WrongClass.objects.create(referensi=ref,
								matkul=matkul, timestamp=datetime.today())
				current_absensi = Absensi.objects.filter(
					jadwal=jadwal_kuliah,
					referensi__in=referensi_match_class,
					email_sended=True,
					timestamp__gte=datetime(curr_date.year, curr_date.month, curr_date.day)
				)
				referensi_to_be_sended = []
				for ref in referensi_match_class:
					if ref not in [ca.referensi for ca in current_absensi]:
						referensi_to_be_sended.append(ref)
				print(datetime(curr_date.year, curr_date.month, curr_date.day))
				print(referensi_to_be_sended)
				print(referensi_match_class)
				print(referensi_wrong_class)
				for referensi in referensi_to_be_sended:
					print(referensi)
					secret_text = secrets.token_urlsafe(16)
					status_email = send_email(referensi.nama, referensi.email, secret_text, raspi_time)
					print(status_email)
					if status_email == 1:
						created_absensi = Absensi.objects.create(
							jadwal=jadwal_kuliah, 
							referensi=referensi, 
							random_text=secret_text)
						data_to_return.append(created_absensi.referensi.mac_address)
				for referensi in referensi_wrong_class:
					status_email = send_email_salah_kelas(referensi.nama, referensi.email)				
		return HttpResponse(json.dumps(data_to_return), content_type='application/json')	
	except Referensi.DoesNotExist:
		raise Http404

def konfirmasi_page(request, random_text):
	get_object_or_404(Absensi, random_text=random_text)
	return render(request, 'absensi/konfirmasi_page.html', { 'random_text': random_text })


def process_konfirmasi_password(request):
	password = request.POST['password']
	random_text = request.POST['random_text']
	absensi = get_object_or_404(Absensi, random_text=random_text)
	referensi = absensi.referensi
	if referensi.password == password:
		absensi.email_confirmed = True
		absensi.save()
		return render(request, 'absensi/sukses_absensi.html')
	else:
		return HttpResponseRedirect('/absensi/konfirmasi_pagemasi/%s' % random_text)	


def form_registrasi(request):
	daftar_matkul = get_list_or_404(Matkul)
	return render(request, 'absensi/form_registrasi.html', { 'daftar_matkul': daftar_matkul })


def process_registrasi(request):
	is_validated = True
	nama = request.POST['nama']
	npm = request.POST['npm']
	email = request.POST['email']
	mac = request.POST['mac-address']
	mkl = request.POST.getlist('daftar-matkul')
	print(mkl)
	pwd = request.POST['password']
	try:
		created_referensi = Referensi.objects.create(nama=nama, npm=npm, email=email, mac_address=mac, password=pwd)
		for matkul_id in mkl:
			matkul = get_object_or_404(Matkul, pk=matkul_id)
			created_referensi.enrollment_set.create(matkul=matkul)
		return render(request, 'absensi/sukses_registrasi.html')
	except IntegrityError:
		return HttpResponseRedirect('/absensi/form')

