from django.contrib import admin
from .models import User, Student, Teacher, School
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(School)