from django.db import models
from django.utils.text import slugify
from django.urls import reverse,reverse_lazy
# Create your models here.
import misaka
from django.contrib.auth import get_user_model
from django import template
from django.contrib.auth.models import User
register = template.Library()

class Group(models.Model):
    name = models.CharField(max_length=64,unique=True)
    slug = models.SlugField(max_length=64,allow_unicode=True,unique=True)
    desc = models.TextField(max_length=256,blank=True,default='')
    desc_html = models.TextField(blank=True,default='',editable=False)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.desc_html = misaka.html(self.desc)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta():
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta():
        unique_together = ('group','user')
