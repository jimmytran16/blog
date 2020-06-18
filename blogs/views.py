from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import User,Post
import hashlib, uuid
from .forms import PostUploadForm
from .ProfilePicForm import ProfilePicForm

# Create your views here.
# REQUEST HANDLERS

def home(request):
    if check_if_logged_in(request): # call this function to check if user is currently logged in
        return redirect('dashhome')
    context={}
    post = reversed(validatePostPictures(Post.objects.all()))
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
    user.first_name = user.first_name.title() + ' ' + user.last_name.title()
    user = [user.email,user.first_name,user.last_name,user.id]
    request.session['user'] = user
    return

def dashboard(request): # This func will redirect you to the user's dashboard
    context = {}
    try:
        if request.session['user']:
            context['logged_in'] = True
            context['first_name'] = request.session['user'][1]
            context['form'] = PostUploadForm()
            return render(request,'dashboard/dashboard.html',context)
        else:
            context['error'] = "Please log in!"
            return render(request,'blogs/login.html',context)
    except Exception as error:
        context['error'] = "Please log in!"
        print(error)
        return render(request,'blogs/login.html',context)

def dash_home(request): # home page after user log in
    context = {}
    if not check_if_logged_in(request):
        return redirect('home')
    context['first_name'] = request.session['user'][1]
    context['logged_in'] = True
    post = reversed(validatePostPictures(Post.objects.all()))
    print(f'Dashhome -- {post}')
    context['post'] = post
    return render(request,'dashboard/index.html',context)

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
            return redirect('dashhome')
        else:
            context['error'] = 'Error submitting the post!'
            return render(request,"dashboard/dashboard.html",context)
    else:
        return HttpResponse({"Error":'GET / Method is not allowed!'})

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

def usersPosts(request):
    context = {}
    if not check_if_logged_in(request): #authenticate the user
        return redirect('login')
    else:
        context['first_name'] = request.session['user'][1]
        context['logged_in'] = True
        try:
            users_post = Post.objects.filter(user_email = request.session['user'][0])
            print(users_post)
            context["post"] = users_post
        except Exception as error:
            context["post"] = None
        return render(request,'dashboard/myposts.html',context)

def editPost(request,id): #shows the user's post, and getting the post ID to query for content
    context = {}
    if not check_if_logged_in(request):
        return redirect('login')
    else:
        post = Post.objects.filter(pk=id).first()
        context['post'] = post
        context['first_name'] = request.session['user'][1]
        context['logged_in'] = True
        return render(request,'dashboard/editpostpage.html',context)

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

def deletePost(request,id): #delete the post. Will get a Post ID in the parameter to delete the specfic post
    context = {}
    try:
        Post.objects.filter(pk=id).delete() #query to the database to get the Post object, then deletes it
    except Exception as error:
        context['error'] = "Failed to delete the post! Please try again!"
        return render(request,'dashboard/editpostpage.html',context)
    return redirect("dashhome") 


def settingsPage(request): #handler to go to the settings page of user's profile
    context =  {}
    if not check_if_logged_in(request):
        return redirect('login')
    else:
        user = User.objects.filter(pk=request.session['user'][3]).first()
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


def validatePostPictures(posts):
    for post in posts:
        try:
            post = post.author.profile.url
        except Exception:
            post.author.profile = False
    return posts

def trimDescription(text):
    if len(text) > 35: # Chcking the lenght of the text to simplify it to a display text
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
