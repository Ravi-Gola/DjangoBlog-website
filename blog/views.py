from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
# from django.http import HttpResponse
from blog.models import Blogcomment, Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
# from blog.templatetags import extras

# Create your views here.
def home(request):
    allPost=Post.objects.all()
    if request.user.is_authenticated:
        user = request.user
        us = User.objects.get(username=user)
    else:
        us="User"
    context={"allPost":allPost,"username":us}
    return render(request,"blog/blogHome.html",context)

def about(request):
    return render(request,"blog/blogAbout.html")

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        if len(name)<2 or len(email)<5 or len(phone)<10 or len(message)<5:
            messages.error(request, 'Please fill the form details correctly.')
        else:
          user=Contact(name=name,email=email, phone=phone,message=message)
          user.save()
          messages.success(request, 'Your message Successfully received. we will reply you soon with in three days |thank you.')

    return render(request,"blog/blogContact.html")

def blog(request):
    if request.user.is_authenticated:
       allPost=Post.objects.all()
       context={"allPost":allPost}
       return render(request,"blog/blogPost.html",context)
    else:
        messages.warning(request,"Please Login or Create Your Account")
        return redirect('/')

def blogContent(request ,slug):
    if request.user.is_authenticated:
       post=Post.objects.filter(slug=slug).first()
       comments=Blogcomment.objects.filter(post=post ,parent=None)
       replies=Blogcomment.objects.filter(post=post).exclude(parent=None)
       replyDict={}
       for reply in replies:
           if reply.parent.sno not in replyDict.keys():
               replyDict[reply.parent.sno]=[reply]
           else:
               replyDict[reply.parent.sno].append(reply)
       context={"post":post,"comments":comments,"replyDict":replyDict}
       return render(request,"blog/blogContent.html",context)
    else:
        messages.warning(request,"Please Login or Create Your Account")
        return redirect('/')

def blogSearch(request):
    if request.user.is_authenticated:
           query=request.GET['search']
           if len(query) >70:
               allPost=Post.objects.none()
           else:
             allPostTitle=Post.objects.filter(title__icontains=query)
             allPostContent=Post.objects.filter(content__icontains=query)
             allPost=allPostTitle.union(allPostContent)
           context={"allPost":allPost,"query":query}
           return render(request,"blog/blogSearch.html",context)
    else:
        messages.warning(request,"Please Login or Create Your Account")
        return redirect('/')

def signup(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        Cpassword=request.POST['Cpassword']
        if len(name) < 2:
            messages.error(request, 'Please Enter Valid User Name')
        else:
             if password==Cpassword:
                try:
                  newuser = User.objects.create_user(username=name,
                                 email=email,
                                 password=password)
                  newuser.save()
                  messages.success(request,'Succesfully Created Your Account')
                except:
                  messages.error(request, 'Username Already Exists')
             else:
                messages.error(request, 'Passwords Does Not Matched')
    return redirect("/")

def Login(request):
    if request.method=="POST":
        name=request.POST['name']
        password=request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
           login(request,user)
           messages.success(request,'Login Your Account Successfully')
        else:
           messages.error(request, 'Invalid Credentials! Try Again')
    return redirect("/")

def Logout(request):
    logout(request)
    messages.success(request,'Logout Your Account Successfully')
    return redirect("/")

def Postcomment(request):
    if request.method=="POST":
        comment=request.POST.get("comment") 
        user = request.user
        postsno=request.POST.get("postsno")
        post=Post.objects.get(sno=postsno)
        parentSno=request.POST.get("parentSno")
        if parentSno=="":
           comment=Blogcomment(user=user ,comment=comment,post=post)
           comment.save()
           messages.success(request,'Successfully Post Your Comment')
        else:
            parent=Blogcomment.objects.get(sno=parentSno)
            comment=Blogcomment(user=user ,comment=comment,post=post,parent=parent)
            comment.save()
            messages.success(request,'Successfully Post Your Reply')
    return redirect(f"/{post.slug}")