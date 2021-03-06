from django.db import models
import datetime


# Create your models here.
class UserTicket(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    passwd = models.CharField(max_length=500)
    time_created = models.DateTimeField(auto_now=True)
    hash_code = models.IntegerField(primary_key=True,unique=True)
    expired = models.BooleanField(default=False)
    def has_expired(self):
        if self.expired:
            return True
        else:
            de = datetime.datetime.now()-self.time_created.replace(tzinfo=None)
            delta = datetime.timedelta(minutes=10)
            return de>delta

class User(models.Model):
    name = models.CharField(max_length=20,unique=True)
    email = models.EmailField()
    passwd = models.CharField(max_length=500)
    @property
    def locked(self):
        time_now = datetime.datetime.now()
        ten_min_before = datetime.datetime.now()-datetime.timedelta(minutes=10)
        # if LogInActivity.objects.filter(user=self,log_in_time__gte=ten_min_before,log_in_time__lte=time_now,success=True).exists():
        #     return False
        if len(LogInActivity.objects.filter(user=self,log_in_time__gte=ten_min_before,log_in_time__lte=time_now,success=False))>5:
            return True
        return False

class LogInActivity(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    log_in_time = models.DateTimeField(auto_now=True)
    success = models.BooleanField()
