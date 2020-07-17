from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from groups.models import Group, GroupMember
from django.views.generic import CreateView,DetailView,ListView,DeleteView,RedirectView
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from groups import models
# Create your views here.

class CreateGroup(CreateView,LoginRequiredMixin):
    fields = ['name','desc']
    model = Group

class SingleGroup(DetailView,LoginRequiredMixin):
    model = Group
    template_name = 'groups/group_detail.html'

class ListGroup(ListView,LoginRequiredMixin):
    model = Group
    template_name = 'groups/group_list.html'

class JoinGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
