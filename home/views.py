from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from .models import Project,Sentence
from wikipediaapi import Wikipedia
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required(login_url='/login')
def dashboard(request):
    projects=Project.objects.all().filter(manager=request.user)|Project.objects.all().filter(annotator=request.user)
    return render(request, 'dashboard.html', {'projects':projects})

@login_required(login_url='/login')
def createproject(request):
    if len(list(request.user.groups.filter(name='Manager'))) == 0:
        return redirect('/')
    if request.method == 'POST':
        wiki_title = request.POST.get('wiki_title')
        target_lang=request.POST.get('target_lang')
        
        new_project=Project(wiki_title=wiki_title, target_lang=target_lang,manager=request.user)
        new_project.save()
        
        intro=Wikipedia().page(wiki_title).summary
        
        sentences=intro.split('.')
        for sentence in sentences:
            if sentence!='':
                new_sentence=Sentence(project=new_project,original_sentence=sentence)
                new_sentence.save()
        messages.success(request,'Project created successfully')
        return redirect(f"/translateproject/{new_project.id}")
    
    return render(request,'createproject.html')

@login_required(login_url='/login')
def translateproject(request,pk):
    try:
        project = Project.objects.get(id=pk)
        if ((request.user==project.manager) or (request.user==project.annotator))==False:
            return redirect('/')
        if request.method == 'POST':
            project = Project.objects.get(id=pk)
            sentences = Sentence.objects.all().filter(project=project)
            for sentence in sentences:
                new_translated_sentence =request.POST.get(str(sentence.id))
                sentence.translated_sentence = new_translated_sentence
                sentence.save()
            messages.success(request,'Translation added successfully')
            return redirect('/')
        project=Project.objects.get(id=pk)
        sentences=Sentence.objects.all().filter(project=project)
        return render(request,'translateproject.html',{'project':project,'sentences':sentences})
    except:
        messages.error(request,'Some error occurred')
        return redirect('/')

def loginUser(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Logged in successfully')
            return redirect("/")
            # A backend authenticated the credentials
        else:
            return render(request, 'login.html')
            # No backend authenticated the credentials
    return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def assignannotator(request,pk):
    try:
        project=Project.objects.get(id=pk)
        if request.user!=project.manager:
            return redirect('/')
        if request.method == 'POST':
            annotator=request.POST.get('annotator')
            new_annotator=User.objects.get(username=annotator)
            project.annotator=new_annotator
            project.save()
            messages.success(request,'Annotator assigned successfully')
            return redirect('/')

        return render(request,'assignannotator.html',{'project':project})
    except:
        messages.error(request,'Some error occurred')
        return redirect('/')
