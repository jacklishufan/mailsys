from django.contrib import admin
import login.models as models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.UserTicket)
