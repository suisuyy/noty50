from django import forms

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from note.models import Note
# Create your views here.
def index(request):
    user=request.user

    if user.is_authenticated==False:
        user=User.objects.get(username="others")
    context={
        'username': user.username,
        'userid': user.id,
        'notes': user.notes.all()
    }
    #if post,save that note then display all note as normal
    if request.method=="POST":
        title=request.POST['titleinput']
        content=request.POST['noteinput']
        if len(title)==0 or len(content)==0:
            return render(request,"error.html",context={"errormsg": "empty title or note,please check your input"})
        new_note=Note()
        new_note.user=user;
        new_note.level=3;
        new_note.title=request.POST['titleinput']
        new_note.content=request.POST['noteinput']
        new_note.save();
        return render(request,"note/index.html",context=context)        
    

    if 'keyword' in request.GET:
        #filter keyword in two 
        context['notes']=context['notes'].filter(content__contains=request.GET['keyword']) | context['notes'].filter(title__contains=request.GET['keyword'])

    return render(request,"note/index.html",context=context)