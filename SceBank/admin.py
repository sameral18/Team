from .models import *
from .models import ContactUsModel, ContactAdmin,SmmaryDataBank
# Register your models here.
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User

admin.site.register(addstudent)
admin.site.register(courses)
# admin.site.register(Timesheet)
admin.site.register(ContactAdmin)
admin.site.register(AdminMessage)
admin.site.register(ContactUsModel)
admin.site.register(SmmaryDataBank)
