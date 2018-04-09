from django.db import models

pilihan_hari = [
    ('Senin', 'Senin'),
    ('Selasa', 'Selasa'),
    ('Rabu', 'Rabu'),
    ('Kamis', 'Kamis'),
    ('Jumat', 'Jumat'),
    ('Sabtu', 'Sabtu')
]

# Create your models here.
class Referensi(models.Model):
    MAC_Address = models.CharField(max_length=250)
    Nama = models.CharField(max_length=500)
    NPM = models.CharField(max_length=100, unique=True)
    Email = models.CharField(max_length=1000)
    Password = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.MAC_Address + ' - ' + self.Nama + ' - ' + self.NPM + ' - ' + self.Email

class Matkul(models.Model):
    Nama_Matkul = models.CharField(max_length=255, default='', unique=True)

    def __str__(self):
        return self.Nama_Matkul

class Jadwal(models.Model):
    Mulai = models.TimeField()
    Selesai = models.TimeField()
    Hari = models.CharField(choices=pilihan_hari, max_length=25)
    Ruangan = models.CharField(max_length=20)
    Matkul = models.ForeignKey(Matkul, on_delete=models.CASCADE)

    def __str__(self):
        return self.Matkul.Nama_Matkul + ' - ' + self.Ruangan + ' - ' + str(self.Mulai) + ' s/d ' + str(self.Selesai)

class Absensi(models.Model):
    Jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE)
    Kelas = models.CharField(max_length=10)
    Referensi = models.ForeignKey(Referensi, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Email_Confirmed = models.BooleanField(default=False)
    Email_Sended = models.BooleanField(default=True)
    Random_Text = models.CharField(max_length=255)

    def __str__(self):
        return self.Referensi.Nama + ' - ' + self.Referensi.NPM

class Enrollment(models.Model):
    Referensi = models.ForeignKey(Referensi, on_delete=models.CASCADE)
    Matkul = models.ForeignKey(Matkul, on_delete=models.CASCADE)

    def __str__(self):
        return self.Referensi.Nama + ' - ' + self.Matkul.Nama_Matkul





    

 
