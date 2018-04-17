from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Referensi, Absensi, Matkul, Enrollment, Jadwal
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.http import Http404
from django.db import IntegrityError
from datetime import datetime, time
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

def send_email_salah_kelas(nama, email, random_text, jam):
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
		referensis = Referensi.objects.filter(
			mac_address__in=req['mac_address'],
			enrollment__matkul=jadwal_kuliah.matkul)
		if len(referensis) > 0 and jadwal_kuliah is not None: 
			referensi_email_sended = Absensi.objects.filter(
				jadwal=jadwal_kuliah,
				referensi__in=referensis,
				email_sended=False,
				timestamp__gte=datetime.today()
			)
			referensi_to_be_sended = []
			for ref in referensis:
				for ref_sended in referensi_email_sended:
					if ref != ref_sended:
						referensi_to_be_sended.append(True)
					else:
						referensi_to_be_sended.append(False)
			data_to_return = []
			for i in range(len(referensi_to_be_sended)):
				referensi = referensis[i]
				secret_text = secrets.token_urlsafe(16)
				if referensi_to_be_sended[i]:
					status_email = send_email(referensi.nama, referensi.email, secret_text, raspi_time)
					if status_email == 1:
						created_absensi = Absensi.objects.create(
							jadwal=jadwal_kuliah, 
							referensi=referensi, 
							random_text=secret_text)
						data_to_return.append(created_absensi.referensi.mac_address)
				else:
					status_email = send_email_salah_kelas(referensi.nama, referensi.email, secret_text, raspi_time)
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

