from django.http import HttpResponseRedirect

#DECORATOR FUNCTIONS
#this decorator function is invoked on certain routes that require user authentication in order to access
def login_required(f):
    def wrap(request, *args, **kwargs):
        print('inside login_required()')
        #this check the session if user object key exist, if not it will redirect to login page
        #else: continue with the initial request handler function
        if 'user' not in request.session.keys():
                return HttpResponseRedirect("/login")
        return f(request, *args, **kwargs)
    return wrap

#this decorator will redirect the user to the user's dashboard if they are logged in
def go_to_dash_if_logged_in(f):
    print('inside go_to_dash_if_logged_in()')
    def wrap(request,*args,**kwargs):
        if 'user' in request.session.keys():
            return HttpResponseRedirect('home') #[if use redirect() --- it continiously redirects for some reason!]
        return f(request, *args, **kwargs)
    return wrap
