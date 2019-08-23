from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=40)
    bio = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField('Recipie', related_name="favorite")
    
    def __str__(self):
        return self.name


class Recipie(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    time = models.IntegerField()
    instructions = models.CharField(max_length=500)
    #favorite = models.ManyToManyField('Recipie', related_name="favorite")


class RecipieForm(ModelForm):
    class Meta:
        model = Recipie
        fields = "__all__"
