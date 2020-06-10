from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User,Post
import hashlib, uuid

# Create your views here.
#REQUEST HANDLERS

def home(request):
    if check_if_logged_in(request): # call this function to check if user is currently logged in
        return redirect('dashhome')
    context={}
    post = Post.objects.all()
    context['post'] = post
    return render(request,'blogs/index.html',context)

def register(request): #Register webpage
    if check_if_logged_in(request):
        return redirect('dashboard')
    context={}
    return render(request,'blogs/register.html')

def registerSubmit(request): #Register form submitted
    if check_if_logged_in(request):
        return redirect('dashboard')
    if request.method == 'POST':
        context = {}
        #get inputs from the form field
        _email = request.POST.get('email')
        _firstname = request.POST.get('first-name')
        _lastname = request.POST.get('last-name')
        _password = request.POST.get('password')
        print(_password)
        if check_email_duplicate(_email) is True: #Check if email is already registered
            context['error'] = 'Email already exist! Please try another email'
            return render(request,'blogs/register.html',context)

        #load the user object with the users crudentials
        try:
            SALT = uuid.uuid4().hex
            print(_password,SALT)
            COMBINED_PASS_SALT = _password + SALT
            _hashed_password = hashlib.sha512(COMBINED_PASS_SALT.encode('utf-8')).hexdigest() # encode the combined password and salt to UTF-8 format
            print(_hashed_password)
            user = User(first_name=_firstname,last_name=_lastname,email=_email,password=_hashed_password,salt=SALT)
            user.save()
        except Exception as error:
            context['error'] = 'Failed to register user!'
            print(error)
            # go the to register page with error message inside the context
            return render(request,'blogs/register.html',context)
        return render(request,'blogs/login.html',context)
    else:
        return HttpResponse({"Error":"GET/ METHOD not allowed!"})

def check_email_duplicate(email): # func to determine if an email already exists isn the database
    try:
        user = User.objects.filter(email=email).first()
        if user is not None:
            return True
        else:
            return False
    except Exception as error:
        print(f'check_email_duplicate() {error}')
        return True

def login(request):
    if check_if_logged_in(request):
        return redirect('dashboard')
    context = {}
    return render(request,'blogs/login.html')

def submitLogin(request):
    #get the username and password fields
    context = {}
    username = request.POST.get('email')
    password = request.POST.get('password')
    print(username,password)
    users = authenticate(username,password)
    #GETTING the users salt and combining it with input password, then hashing it and comparing it to the hashing password from DB
    if not users:  #if returns empty users query or password doesn't match
        context['error'] = 'Invalid username or password'
        return render(request,'blogs/login.html',context)
    else:
        auth_login(request,users)
        return redirect('dashhome')

def auth_login(request,user): #log user in by setting a list of the users attributes into the session
    user = [user.email,user.first_name,user.last_name,user.id]
    request.session['user'] = user
    return

def dashboard(request): # This func will redirect you to the user's dashboard
    context = {}
    try:
        if request.session['user']:
            context['logged_in'] = True;
            context['first_name'] = request.session['user'][1];
            return render(request,'dashboard/dashboard.html',context)
        else:
            context['error'] = "Please log in!"
            return render(request,'blogs/login.html',context)
    except Exception as error:
        context['error'] = "Please log in!"
        return render(request,'blogs/login.html',context)

def dash_home(request): # home page after user log in
    context = {}
    if not check_if_logged_in(request):
        return redirect('login')
    context['first_name'] = request.session['user'][1];
    context['logged_in'] = True
    post = Post.objects.all()
    context['post'] = post
    print(post)
    return render(request,'dashboard/index.html',context)

def submitPost(request):
    context = {}
    subject = request.POST.get('subject')
    text = request.POST.get('textfield')
    if len(text) > 35: # Chcking the lenght of the text to simplify it to a display text
        display_text = text[0:35] + '...'
    else:
        display_text = text
    try:
        user_id = request.session['user'][3]
        user_email = request.session['user'][0]
        post = Post(description=text,subject=subject,display_text=display_text,user_id=user_id,user_email=user_email)
        post.save()
    except Exception as error:
        context['error'] = 'Error submitting the post!'
        print(f'Error submitting post! {error}')
        return render(request,'dashboard/dashboard.html',context)
    return redirect('home')

def readPost(request):
    context = {}
    post_id = request.GET.get('id')
    post = Post.objects.filter(id=post_id).first()
    print(post)
    if check_if_logged_in(request):
        context['first_name'] = request.session['user'][1];
        context['logged_in'] = True
    context['post'] = post
    return render(request,'dashboard/readpost.html',context)


def auth_logout(request):
    try:
        del request.session['user']
    except Exception as error:
        print(f'auth_logout error --- {error}')
    return
def authenticate(username,password): #authenticate the user log in crudentials
    user = User.objects.filter(email=username).first() #query the database for the user with the username - returns None if there is no existing user
    if user is not None:
        if hashlib.sha512((password+user.salt).encode('utf-8')).hexdigest() == user.password: #compare passwords if user exists!
            return user
    return None


def check_if_logged_in(request):
    try:
        if request.session['user'] is not None:
            return True
        else:
            return False
    except Exception as error:
        print(f'check_if_logged_in() -- {error}')
        return False


def logout(request):
    context={}
    auth_logout(request)
    return redirect('home')
