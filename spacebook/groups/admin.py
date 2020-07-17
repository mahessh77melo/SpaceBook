from django.contrib import admin

# Register your models here.
from groups import models

class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.Group)
