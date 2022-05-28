from datetime import date
from itertools import count

from multiprocessing import context
from random import choices
from django.shortcuts import redirect, render , HttpResponseRedirect
from . forms  import *
from django.contrib.auth import views 
from django.contrib import messages
from django.views import View, generic
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.models import User
from .models import Post, Replie 
from accounts.models import  Profile
from tkinter import *
from .models import Upload_Notes
from dashboard.forms import PostContent,ReplyContent
import io
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from django.db.models import Count
# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required(login_url = 'login')
def admin_home(request):
    pending_notes = Upload_Notes.objects.filter(status="pending").count()
    accepted_notes = Upload_Notes.objects.filter(status="Accept").count()
    rejected_notes = Upload_Notes.objects.filter(status="Reject").count()
    all_notes = Upload_Notes.objects.all().count()
    
   # data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False)).order_by('-user__last_login')[:10]
    data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False), Q(user__last_login__isnull=False)).order_by('-user__last_login')
    user= User.objects.values_list('last_login')
    context={
        'pending_notes':pending_notes,
        'accepted_notes':accepted_notes,
        'rejected_notes':rejected_notes,
        'all_notes':all_notes,
        'data':data,
        'user':user
    }
    return render(request,"instructor/admin_home.html",context)


@login_required
def show_all_users(request):
    data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False))
    return render(request, "instructor/showallusers.html", {'data': data})
   

@login_required
def delete_post(request, pk=None):
    post = Post.objects.filter(id=pk)
    post.delete()
    return redirect('/forum')

def delete_reply(request, pk=None):
    reply = Replie.objects.filter(id=pk)
    reply_instance = get_object_or_404(Replie,id=pk)
    post_pk=reply_instance.post.id
    reply.delete()
    return redirect(reverse('dashboard:discussion', args=[post_pk])) 

  

@login_required
def user_home(request):
    return render(request,"user/user_home.html")

@login_required
def delete_user(request,pk=None):
        User.objects.get(id=pk).delete()
        return redirect("/showallusers")

@login_required
def forum(request):
    user = request.user
 
    profile = Profile.objects.all()
    if request.method=="POST": 
        form=PostContent(request.POST)
        if form.is_valid():  
          user = request.user
          image = request.user.profile.image
          content = request.POST.get('post_content','')
          post = Post(user1=user, post_content=content, image=image)
          post.save()
          messages.success(request, f'Your Question has been posted successfully!!')
          return redirect('/forum')
        else:
            form=PostContent()  
    posts = Post.objects.filter().order_by('-timestamp')
    form= PostContent()
    context={
        'posts':posts,
        'form':form
    }
    return render(request, "forum.html",context)


def edit_post(request, pk):

    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect(reverse('dashboard:discussion', args=[post.id]))
    else:
        form = UpdatePostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'edit_post.html', context)

def edit_reply(request, pk):
    reply = Replie.objects.get(id=pk)

    if request.method == 'POST':
        form = UpdateReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, "Reply updated successfully!")
            return redirect(reverse('dashboard:discussion', args=[reply.post.id]))
    else:
        form = UpdateReplyForm(instance=reply)
    context = {
        'form': form
    }
    return render(request, 'edit_reply.html', context)
@login_required(login_url = 'login')   
def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method=="POST":
        form=ReplyContent(request.POST)
        if form.is_valid():  
          user = request.user
          image = request.user.profile.image
          desc = request.POST.get('reply_content','')
          post_id =request.POST.get('post_id','')
          reply = Replie(user = user, reply_content = desc, post=post, image=image)
          reply.save()
          messages.success(request, f'Your Reply has been posted successfully!!')
          return redirect(f'/discussion/{post_id}')
        else:
            form=ReplyContent()
    form= ReplyContent()
             
    return render(request, "discussion.html", {'post':post, 'replies':replies,'form':form})    


@login_required
def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        branch = request.POST['branch']
        subject = request.POST['subject']
        notes = request.FILES['notesfile']
        filetype = request.POST['filetype']
        description = request.POST['description']

        user = User.objects.filter(username=request.user.username).first()
        Upload_Notes.objects.create(user=user,uploadingdate=date.today(),branch=branch,subject=subject,notesfile=notes,
                                 filetype=filetype,description=description,status='pending')
        messages.success(request,f"Notes uploaded from {request.user.username} successfully!")
        return redirect('/view_mynotes')
    return render(request,'user/upload_notes.html')

@login_required
def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Upload_Notes.objects.filter(user = user)

    context = {'notes':notes}
    return render(request,'user/view_mynotes.html',context)

@login_required 
def delete_mynotes(request,pk=None):
    notes = Upload_Notes.objects.get(id=pk)
    notes.delete()
    return redirect("/view_mynotes")

@login_required
def pending_notes(request):
    pnotes = Upload_Notes.objects.filter(status = "pending")

    context = {'pnotes':pnotes}
    return render(request,'instructor/pending_notes.html',context)
@login_required
def assign_status(request, pk=None):
    notes = Upload_Notes.objects.get(id=pk)
    if request.method=='POST':
        status = request.POST['status']
        try:
            notes.status = status
            notes.save()
            messages.success(request,f" assign status to Notes successfully!")
            return redirect("/accepted_notes")
        except:
         messages.error(request, 'Something went wrong, Try Again')
    context = {'notes':notes,}
    return render(request,'instructor/assign_status.html',context)


def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Upload_Notes.objects.filter(status = "Accept")
    context = {'notes':notes}
    return render(request, 'instructor/accepted_notes.html',context)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Upload_Notes.objects.filter(status = "Reject")
    context = {'notes':notes}
    return render(request, 'instructor/rejected_notes.html',context)

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Upload_Notes.objects.all()
    context = {'notes':notes}
    return render(request, 'instructor/all_notes.html',context)

def delete_notes(request,pk=None):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Upload_Notes.objects.get(id=pk)
    notes.delete()
    messages.success(request,f"  Notes  delated  successfully!")
    return  redirect('/all_notes')
# def delete_notes(request, pk=None):
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return redirect('login')
#         print(request.POST.get('notesid'))
#         notes = Upload_Notes.objects.get(id=int(request.POST.get('notesid')))
#         notes.delete()
#         return JsonResponse({'msg': 'Notes deleted successfully !'})

def view_allnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Upload_Notes.objects.filter(status='Accept')
    context = {'notes':notes}
    return render(request, 'user/view_allnotes.html',context)    


def notessharing(request):
    user = User.objects.get(id=request.user.id)
    mynotes = Upload_Notes.objects.filter(user = user).count()
    allnotes = Upload_Notes.objects.filter(status='Accept').count()
    context={
        'mynotes':mynotes,
        'allnotes':allnotes
    }
    return render(request,"user/notessharing.html",context)
