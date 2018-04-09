from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Referensi, Absensi, Matkul, Enrollment
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import Http404
import secrets
import requests
import json

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hello")

def send_email(Nama, Email, Random_Text, jam):
	# sending_url_email = "https://api.sendinblue.com/v3/smtp/email"
	# data = {
	# 	'sender':{'name': 'Ekmal Rizki', 'email': 'ekmal.milan@yahoo.com'},
	# 	'to':[
	# 		{
	# 			'name': Nama,
	# 			'email': Email
	# 		}
	# 	],
	# 	'replyTo': { 'email': 'ekmal.milan@yahoo.com'},
	# 	'subject':'Konfirmasi',
	# 	'htmlContent':'Selamat. <a href="ekmal.herokuapp.com/music/konfirmasi/' + Random_Text + '">Link</a>'
	# }
	# headers={
	# 	'api-key':'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',
	# 	'Content-Type': 'application/json'
	# }
	# response = requests.request("POST", sending_url_email, data=json.dumps(data),headers=headers)
	send = send_mail(
		'Konfirmasi',
		jam + ' Selamat ! Tekan Link Disamping-> absensikampus.herokuapp.com/music/konfirmasi/' + Random_Text + '',
		'absensi@vektorprojects.com',
		[Email],
		fail_silently=False
	)
	return send

@csrf_exempt
def get_mac_address_data_from_raspi(request):
	try:
		req = json.loads(request.body)
		print(req)
		referensis = Referensi.objects.filter(MAC_Address__in=req['mac_address'])
		kelas = req['kelas']
		jam = req['jam']

		if len(referensis) > 0:
			absensi = [A for A in Absensi.objects.filter(NPM__in=[Ref for Ref in referensis])]
			ref_for_sending_email = [x for x in referensis if x not in [A.NPM for A in absensi]]
			refs = [(ref, secrets.token_urlsafe(16)) for ref in ref_for_sending_email]
			refs = [(ref, random_text) for (ref, random_text) in refs if send_email(ref.Nama, ref.Email, random_text) == 1]
			new_absensi = [Absensi.objects.create(NPM=ref, Kelas=kelas, Random_Text=Random_Text) for ref, Random_Text in refs]
			return HttpResponse(json.dumps([]))
		else:
			raise Http404	
	except Referensi.DoesNotExist:
		raise Http404

def konfirmasi_page(request, random_text):
	get_object_or_404(Absensi, Random_Text=random_text)
	return render(request, 'music/konfirmasi_page.html', { 'random_text': random_text })


def process_konfirmasi_password(request):
	password = request.POST['password']
	random_text = request.POST['random_text']
	absensi = get_object_or_404(Absensi, Random_Text=random_text)

	referensi = absensi.NPM
	if referensi.Password == password:
		absensi.Email_Confirmed = True
		absensi.save()
		return HttpResponse("<h1>Sukses Absensi")
		
	else:
		return HttpResponseRedirect('/music/konfirmasi/%s' % random_text)	

def form_registrasi(request):
	daftar_matkul = get_list_or_404(Matkul)
	return render(request, 'music/form_registrasi.html', { 'daftar_matkul': daftar_matkul })



def process_registrasi(request):
	nama = request.POST['nama']
	npm = request.POST['npm']
	email = request.POST['email']
	mac = request.POST['mac']
	mkl = request.POST.getlist('mkl')
	pwd = request.POST['pwd']
	created_referensi = Referensi.objects.create(Nama=nama, NPM=npm, Email=email, MAC_Address=mac, Password=pwd)
	for Matkul_id in mkl:
		matkul = Matkul.objects.get(pk=Matkul_id)
		Enrollment.objects.create(Referensi=created_referensi, Matkul=matkul)
	return HttpResponse("<h1>Sukses Registrasi")

