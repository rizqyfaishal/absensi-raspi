from django.db import models

pilihan_hari = [
   (0, 'Senin'),
   (1, 'Selasa'),
   (2, 'Rabu'),
   (3, 'Kamis'),
   (4, 'Jumat'),
   (5, 'Sabtu'),
   (7, 'Minggu')
]

# Create your models here.
class Referensi(models.Model):
    mac_address = models.CharField(max_length=250, unique=True)
    nama = models.CharField(max_length=255)
    npm = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Matkul(models.Model):
    nama_matkul = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nama_matkul

class Jadwal(models.Model):
    mulai = models.TimeField()
    selesai = models.TimeField()
    hari = models.IntegerField(choices=pilihan_hari)
    ruangan = models.CharField(max_length=20)
    matkul = models.ForeignKey(Matkul, on_delete=models.CASCADE)

    def __str__(self):
        return self.matkul.nama_matkul + ' - ' + self.ruangan + ' - ' + str(self.mulai) + ' s/d ' + str(self.selesai)


class Absensi(models.Model):
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE)
    referensi = models.ForeignKey(Referensi, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)
    email_sended = models.BooleanField(default=True)
    random_text = models.CharField(max_length=255)

    def __str__(self):
        return self.referensi.nama + ' - ' + self.referensi.npm

class Enrollment(models.Model):
    referensi = models.ForeignKey(Referensi, on_delete=models.CASCADE)
    matkul = models.ForeignKey(Matkul, on_delete=models.CASCADE)

    def __str__(self):
        return self.referensi.nama + ' - ' + self.matkul.nama_matkul





    

 
