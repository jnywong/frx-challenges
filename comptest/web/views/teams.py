from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..models import Team, TeamMembership


@login_required
def list(request: HttpRequest) -> HttpResponse:
    """
    List all teams the current user is a member of
    """
    memberships = TeamMembership.objects.filter(user=request.user)
    return render(request, "teams/list.html", {"memberships": memberships})


class TeamForm(forms.Form):
    name = forms.CharField(max_length=1024)


@login_required
def create(request: HttpRequest) -> HttpResponse:
    """
    Create a new team with current user as admin
    """
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = Team()
            team.name = form.cleaned_data["name"]
            # FIXME: Transactions?
            team.save()
            membership = TeamMembership()
            membership.user = request.user
            membership.team = team
            membership.is_admin = True
            membership.save()
            return HttpResponseRedirect(reverse("teams-view", args=(team.id,)))
    else:
        form = TeamForm()
    return render(request, "teams/create.html", {"form": form})


# Intentionally not authenticated, as anyone should be able to view team membership
def view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Display information about a particular team
    """
    try:
        team = Team.objects.filter(id=id).get()
    except Team.DoesNotExist:
        raise Http404("The requested team does not exist")

    return render(request, "teams/view.html", {"team": team})


class AddMemberForm(forms.Form):
    username = forms.CharField(max_length=1024)
    is_admin = forms.BooleanField(required=False)


@login_required
def add_member(request: HttpRequest, id: int) -> HttpRequest:
    try:
        team = Team.objects.filter(id=id).get()
    except Team.DoesNotExist:
        raise Http404("The requested team does not exist")

    # FIXME: Validate that we are admin on the team so we can add people
    if request.method == "POST":
        form = AddMemberForm(request.POST)
        if form.is_valid():
            # FIXME: Handle missing users
            # FIXME: Handle an 'invitation acceptance' flow for users
            user = User.objects.filter(username=form.cleaned_data["username"]).get()
            membership = TeamMembership()
            membership.user = user
            membership.team = team
            membership.is_admin = form.cleaned_data["is_admin"]
            membership.save()
            return HttpResponseRedirect(reverse("teams-view", args=(team.id,)))
    else:
        form = AddMemberForm()
    return render(request, "teams/add-member.html", {"form": form, "team": team})
