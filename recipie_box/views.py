from django.shortcuts import render
from recipie_box.models import Recipie, Author, RecipieForm
from recipie_box.forms import AddAuthor, LoginForm, EditForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


def index(request, *args, **kwargs):
    html = 'index.html'
    items = Recipie.objects.all()
    return render(request, html, {"recipies": items})


def recipie(request, id, *args, **kwargs):
    u = request.user
    html = 'recipie.html'
    item = Recipie.objects.get(id=id)
    return render(request, html, {'recipie': item, 'author': u})



def author(request, id, *args, **kwargs):
    html = 'author.html'
    item = Author.objects.get(id=id)
    items = Recipie.objects.all().filter(author=item)
    favorites = item.favorite.all()
    return render(request, html, {'recipies': items, "author": item, "favorite": favorites})


@login_required
def addauthor(request, *args, **kwargs):
    html = 'genericform.html'
    if request.user:

        if not request.user.is_staff:
            raise PermissionDenied
    if request.method == "POST":
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = User.objects.create_user(
                username=data['username'], password=data['password'],
                is_staff=data['is_staff'])
            a = Author.objects.create(
                user=u, name=data['name'], bio=data['bio'])
            login(request, u)
            return HttpResponseRedirect(reverse('index'))
    form = AddAuthor()

    return render(request, html, {'form': form})


@login_required
def addrecipie(request, *args, **kwargs):
    html = 'genericform.html'

    if request.method == "POST":

        form = RecipieForm(request.POST)
        if form.is_valid():

            new_recipie = form.save()

    form = RecipieForm()

    return render(request, html, {'form': form})


def loginpage(request, *args, **kwargs):
    html = 'genericform.html'

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = authenticate(
                username=data['username'], password=data['password'])
            if u is not None:
                login(request, u)
            else:
                return HttpResponseRedirect(reverse('login'))
            destination = request.GET.get('next')
            if destination is not None:
                return HttpResponseRedirect(destination)
            else:
                return HttpResponseRedirect(reverse('index'))
    form = LoginForm()

    return render(request, html, {'form': form})


def edit_recipie(request, id): 
    instance = Recipie.objects.get(id=id)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        data = {'title': instance.title, 'description': instance.description, 'time': instance.time, 'instructions': instance.instructions}
        form = EditForm(initial=data)
    return render(request, 'editrecipie.html', {'form': form, "recipie": instance})


def add_favorite(request, id, *args, **kwargs):
    try:
        recipie = Recipie.objects.get(id=id)
        item = Author.objects.get(user=request.user)
    except add_favorite.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    item.favorite.add(recipie)
    
    return HttpResponseRedirect(reverse("index"))


def remove_favorite(request, id, *args, **kwargs):
    try:
        recipie = Recipie.objects.get(id=id)
        item = Author.objects.get(user=request.user)
    except remove_favorite.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    item.favorite.remove(recipie)

    return HttpResponseRedirect(reverse("index"))


def logoutpage(request):
    logout(request)

    return HttpResponseRedirect(reverse('index'))


