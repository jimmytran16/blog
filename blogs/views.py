from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from .models import User,Post
import hashlib, uuid
from .forms import PostUploadForm
from .ProfilePicForm import ProfilePicForm
from .decorators.decor import login_required, go_to_dash_if_logged_in  #import the decorator functions from package
from django.views.decorators.cache import cache_page # decorator for caching the view

# Create your views here.
# REQUEST HANDLERS

@go_to_dash_if_logged_in
def home(request):
    context={}
    post = reversed(validatePostPictures(Post.objects.all()))
    print('just CALLED query!')
    context['post'] = post
    return render(request,'blogs/index.html',context)

@go_to_dash_if_logged_in
@cache_page(60*60*10) #cache for 10 hours on client machine
def register(request): #Register webpage
    context={}
    return render(request,'blogs/register.html')

@go_to_dash_if_logged_in
def registerSubmit(request): #Register form submitted
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
        return JsonResponse({"Error":"GET/ METHOD not allowed!"})

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

@go_to_dash_if_logged_in
@cache_page(60*60*10) #cache for 10 hours on client machine
def login(request):
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
    user.first_name = user.first_name.title() + ' ' + user.last_name.title()
    user = [user.email,user.first_name,user.last_name,user.id]
    request.session['user'] = user
    return

@login_required
def dashboard(request): # This func will redirect you to the user's dashboard
    context = {}
    if request.method == 'GET':
        try:
            context['logged_in'] = True
            context['first_name'] = request.session['user'][1]
            context['form'] = PostUploadForm()
            return render(request,'dashboard/dashboard.html',context)
        except Exception as error:
            context['error'] = "Please log in!"
            print(error)
            return render(request,'blogs/login.html',context)
    elif request.method == 'POST':
        context['error'] = 'CANT POST /'
        return HttpResponse(context)

@login_required
def dash_home(request): # home page after user log in
    context = {}
    if request.method == 'GET':
        context['first_name'] = request.session['user'][1]
        context['logged_in'] = True
        post = reversed(validatePostPictures(Post.objects.all()))
        print(f'Dashhome -- {post}')
        context['post'] = post
        return render(request,'dashboard/index.html',context)
    elif request.method == 'POST':
        context['error'] = "CANT DO POST /"
        return HttpResponse(context)

def submitPost(request):
    context = {}
    if request.method == 'POST':
        user = User.objects.filter(pk=str(request.session['user'][3])).first()
        form = PostUploadForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = request.session['user'][3] #assign the post to the current user's user_id from the session
            obj.user_email = request.session['user'][0] #assign the email of the user to the post
            obj.display_text = trimDescription(obj.description) #trim the description to make it fit to the card display
            obj.author = user
            obj.save()
            #This will remove the cache value and set it to None
            # cache.set(get_cache_key(request), None) #remove the cache key
            return redirect('dashhome')
        else:
            context['error'] = 'Error submitting the post!'
            return render(request,"dashboard/dashboard.html",context)
    else:
        return JsonResponse({"Error":'GET / Method is not allowed!'})

# def expire_page(path):
#     request = HttpRequest()
#     request.path = path
#     key = get_cache_key(request)
#     if cache.has_key(key):
#         cache.delete(key)

@login_required
def changeProfile(request,id):
    context = {}
    if request.method == 'POST':
        instance = User.objects.filter(pk = id).first()
        form = ProfilePicForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('settingsPage')
        else:
            context['error'] = 'Error uploading profile picture'
            return render(request,"dashboard/dashboard.html",context)
    else:
        return JsonResponse({"Error":"Request not allowed!"})

@login_required
def usersPosts(request):
    context = {}
    context['first_name'] = request.session['user'][1]
    context['logged_in'] = True
    try:
        _user = User.objects.filter(pk=request.session['user'][3]).first()
        users_post = Post.objects.filter(author = _user)
        print(users_post)
        context["post"] = users_post
    except Exception as error:
        context["post"] = None
    return render(request,'dashboard/myposts.html',context)

@login_required
def editPost(request,id): #shows the user's post, and getting the post ID to query for content
    context = {}
    post = Post.objects.filter(pk=id).first()
    print(post)
    context['post'] = post
    context['first_name'] = request.session['user'][1]
    context['logged_in'] = True
    return render(request,'dashboard/editpostpage.html',context)

@login_required
def comfirmEdits(request,id): #updates the user's post
    context = {}
    if request.method == "POST":
        _new_description = request.POST.get('description')
        _post_to_edit = Post.objects.filter(pk = id).first()
        _post_to_edit.description = _new_description
        _post_to_edit.display_text = trimDescription(_new_description) # trim the description text to save to the display_text for the post
        try:
            _post_to_edit.save()
        except Exception as error:
            print(f'Failed to update post {error}')
        return redirect('dashhome')
    else:
        return JsonResponse({"Error":"Method POST not allowed!"})

@login_required
def deletePost(request,id): #delete the post. Will get a Post ID in the parameter to delete the specfic post
    context = {}
    try:
        Post.objects.filter(pk=id).delete() #query to the database to get the Post object, then deletes it
        # print(f'CACHE KEY - - {get_cache_key(request)}')
        # cache.set(get_cache_key(request), None)
    except Exception as error:
        context['error'] = "Failed to delete the post! Please try again!"
        return render(request,'dashboard/editpostpage.html',context)
    return redirect("dashhome")

@login_required
def settingsPage(request): #handler to go to the settings page of user's profile
    context =  {}
    if request.method == 'GET':
        user = User.objects.filter(pk=request.session['user'][3]).first() #query to get the users information from the Users model
        try:
            profile = user.profile.url
        except Exception as error:
            print(f'PROFILE - - {error}')
            profile = None
        context['user'] = user
        context['profile'] = profile
        context['form'] = ProfilePicForm()
        context['first_name'] = request.session['user'][1]
        context['logged_in'] = True
        return render(request,'dashboard/settings.html',context)
    elif request.method == 'POST':
        context['error'] = 'POST REQUEST NOT ALLOWED'
        return JsonResponse(context)

#validate the image url .. if it does not contain an image, make the profile attribute false in order to pass into the webpage
def validatePostPictures(posts):
    for post in posts:
        try:
            post = post.author.profile.url
        except Exception:
            post.author.profile = False
    return posts

def trimDescription(text):
    if len(text) > 35: # Checking the length of the text to simplify it to a display text
        display_text = text[0:34] + '...'
    else:
        display_text = text
    return display_text

def readPost(request):
    context = {}
    post_id = request.GET.get('id')
    post = Post.objects.filter(id=post_id).first()
    try:
        img = post.author.profile
    except Exception:
        post.author.profile = False #assign false to the profile attribute of user since there is no existing profile picture
    if check_if_logged_in(request):
        context['first_name'] = request.session['user'][1]
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


# SETTINGS EDITS
def updatePassword(request):
    #validate if the user is logged in
    #---------------------------------
    #---------------------------------
    context = {}
    if request.method == 'POST':
        _password = request.POST.get('edit_password') #get the password from the field
        _user = User.objects.filter(pk=request.session['user'][3]).first() # get the user object by getting the user id from the session
        SALT = uuid.uuid4().hex #generate a random salt
        COMBINED_PASS_SALT = _password + SALT #combine the salt with the password
        _hashed_password = hashlib.sha512(COMBINED_PASS_SALT.encode('utf-8')).hexdigest() # encode the combined password and salt to UTF-8 format

        # update the salt and the password into the database
        _user.salt = SALT
        _user.password = _hashed_password
        try: #handle the exception for updating the user
            _user.save()
        except Exception as error:
            print("ERROR SAVING THE PASSWORD!")
            context['Error'] = 'Error updating password'
            return JsonResponse(context)
        return redirect('settingsPage')

    elif request.method == 'GET':
        context['Error'] = 'CANNOT do GET/ request'
        return JsonResponse(context)

import time

#This handler is to update the first name, last name, and email of the user
def updateSettingsInformation(request):
    context = {}
    if request.method == "POST":
        _first_name = request.POST.get('edit_first')  #extract fields from the body
        _last_name = request.POST.get('edit_last')
        _email_address = request.POST.get('edit_email')
        try:
            ## Query the user object and then give it new values
            _current_user = User.objects.filter(pk=request.session['user'][3]).first()
            _current_user.first_name = _first_name
            _current_user.last_name = _last_name
            _current_user.email = _email_address
            updateUserSessionValues(request,_current_user)
            _current_user.save()
        except Exception as error:
            print(f'Error updating the user email/first/last- {error}')
            context['error'] = 'Error updating settings'
            return JsonResponse(context)
        # time.sleep(3) #sleep thread for 3 seconds
        return redirect('settingsPage')
    elif request.method == "GET":
        context['error'] = 'GET METHOD IS NOT ALLOWED'
        return JsonResponse(context)

def updateUserSessionValues(request,user):
    #update the user session dictionary to a new list after they have changed their settings
    request.session['user'] = [user.email,user.first_name.title() + ' ' + user.last_name.title(),user.last_name,user.id]
