from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='referral_code')
    bio=models.TextField(blank=True)
    code=models.CharField(max_length=12,blank=True)
    recommended_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='ref_by')
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommend_profiles(self):
        qs=Profile.objects.all()
        my_recs=[]
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs

    def save(self,*args,**kwargs):
        if self.code=="":
            code = generate_ref_code()
            self.code=code
        super().save(*args,**kwargs)