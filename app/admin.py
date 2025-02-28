from django.contrib import admin

# Register your models here.
from . import models

# Register your models here.


admin.site.register(models.Review)
admin.site.register(models.Login)
admin.site.register(models.Complaint)
admin.site.register(models.User)
admin.site.register(models.Payment)