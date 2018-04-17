from django.contrib import admin
from .models import Referensi, Absensi, Jadwal, Matkul, Enrollment


# Register your models here.
admin.site.register(Referensi)
admin.site.register(Absensi)
admin.site.register(Jadwal)
admin.site.register(Matkul)
admin.site.register(Enrollment)
