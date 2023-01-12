from .models import*
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import User as uaa
from SceBank.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from SceBank import models
from django.shortcuts import redirect, render, get_object_or_404
from SceBank.models import Blog

def SmmaryDataBank(request):
    x = {'data': models.SmmaryDataBank.objects.all()}
    if request.method == 'GET':
        data = models.SmmaryDataBank()
        data.name = request.GET.get('namefile1')
        data.file = request.GET.get('myfile')
        data.active = True
        data.save()

        return render(request, 'Data.html', context=x)
    return render(request, 'SmmaryDataBank.html', context=x)
#

@login_required
def home(request):
    """
    Home page func
    Get request and retrun home page
    """
    return render(request, 'home.html')


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        proj = Project.objects.filter(title__contains=searched)
        blog = Blog.objects.filter(title__contains=searched)
        return render(request, 'search.html', {'searched': searched, 'projects': proj, 'blogs': blog})
    else:
        return render(request, 'search.html')


@login_required
def personalArea(request):
    return render(request, 'personalArea.html')


@login_required
def logoutuser(request):  # p
    if request.method == 'POST':  # method post!!!
        logout(request)
        return redirect('home')  # return home page after logout


@login_required
def userSettings(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'GET':
        form = User(instance=user)
        return render(request, 'userSettings.html', {'user': user, 'form': form})
    else:
        try:
            form = User(request.POST, instance=user)
            form.save(user)
            if validator(request.POST['password1'], request.POST['password2']):
                user.set_password(request.POST['password1'])
                user.save()
            return redirect('personalArea')
        except ValueError:
            return render(request, 'userSettings.html', {'user': user, 'form': form, 'error': 'Bad info'})


def validator(val1, val2):
    if val1 != '' and val1 == val2:
        return True
    return False


class RegisterUserForm:
    pass


'''def signupuser(request):
   
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': RegisterUserForm()})  # User creation form
    else:
        if request.POST['password1'] == request.POST['password2']:  # if first and second password equal create new user
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                      first_name=request.POST['first_name'],
                                                      last_name=request.POST['last_name'],
                                                      college=request.POST['college'], email=request.POST['email'],
                                                      major=request.POST['major'])  # create user
                user.save()  # save user
                login(request, user)
                messages.success(request, ("Registartion Successful!"))
                return redirect('home')  # return current page
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': RegisterUserForm(),
                                                           'error': 'That username has already been taken.Please try again'})
                # if user create login that exist send error massege
        else:
            return render(request, 'signupuser.html', {'form': RegisterUserForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})  # Authentication Form
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None and user.is_staff:
            return render(request, 'loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('home')  # return current page'''


class ContactUs:
    pass


def contactus(request):
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactus.html')
    else:
        form = ContactUs(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form.save()
            form = ContactUs()
            form.fields['name'] = ''
            form.fields['email'] = ''
            form.fields['subject'] = ''
            form.fields['message'] = ''
            recipients = ['serj.moskovec@gmail.com']
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            from_email = request.POST.get('email', '')
            send_mail(subject, message, from_email, recipients)
        else:
            hasError = True
            message = 'Please make sure all fields are valid'

    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError})


def contactadmin(request):
    """
    Contact US func
    Get request and return contactus page
    """
    if request.method == 'GET':
        return render(request, 'contactadmin.html')
    else:
        form = ContactAdmin(request.POST)
        message = 'Message was sent successfully'
        hasError = False
        if form.is_valid():
            form = ContactAdmin(request.POST)
            form.save()
            # form.fields['subject'] = ''
            # form.fields['message'] = ''
            # subject = request.POST['subject']
            # message = request.POST['message']
            # mail_to_admin = ContactAdmin(subject =subject,message = message)
            # mail_to_admin.save()

        else:
            hasError = True
            message = 'Please make sure all fields are valid'

    return render(request, 'contactus.html', {'form': form, 'message': message, 'hasError': hasError})






@login_required
def all_blogs(request):
    blogs = Blog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'all_blogs.html', {'blogs': blogs})


@login_required
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    return render(request, 'detail.html', {'blog': blog})


class BlogForm:
    pass


@login_required
def createBlog(request):
    if request.method == 'GET':
        return render(request, 'createPost.html')
    else:
        try:
            form = BlogForm(request.POST)  # edit form
            newblog = form.save(commit=False)  # save all input data in database
            newblog.user = request.user
            newblog.save()  # save data
            return redirect('all_blogs')
        except ValueError:
            return render(request, 'createPost.html', {'form': BlogForm(), 'error': 'Bad data passed in. Try again'})


@login_required
def editBlog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'GET':
        form = BlogForm(instance=blog)
        return render(request, 'editBlog.html', {'blog': blog, 'form': form})
    else:
        try:
            form = BlogForm(request.POST, instance=blog)
            form.save(blog)
            return redirect('detail', blog_id)
        except ValueError:
            return render(request, 'editBlog.html', {'blog': blog, 'form': form, 'error': 'Bad info'})


@login_required
def deleteBlog(request, blog_id):  # delete can do only user who create todo
    blog = get_object_or_404(Blog, pk=blog_id,
                             user=request.user)  # find todo in database(import get_object_or_404), (user=request.user) check if todo belongs to user
    if request.method == 'POST':  # Post becouse we upload data to database
        Blog.delete(blog)  # delete blog
        return redirect('all_blogs')  # return page with current todos
    # ?????????????????????????????????????????????????
    # /////////////////////////////////////////////////
    # ?????????????????????????????????????????????????
    # /////////////////////////////////////////////////

def home(request):
    return render(request,'a.html')
def f3(request):
    return render(request, 'base.html')
def f3(request):
    return render(request, 'signup.html')
def f4(request):
    return render(request,'d.html')
def f5(request):
    return render(request, 'addstudent.html')
def f6(request):
    return render(request,'f.html')


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')




def signup(request):
    def s_signup(request, student):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            s_id = request.POST['id']
            email = request.POST['email']
            college=request.POST['college']
            avg=request.POST['avg']
            if password1 == password2:
                if not s_id.objects.filter(s_id=s_id).count() == 1:
                    username(request, 'your id is wrong')
                elif User.objects.filter(username=username):
                    username.error(request, 'username is taken')

                else:
                    user = User.objects.create_user(username=username, email=email, password=password1,
                                                    last_name=last_name,
                                                    first_name=first_name)
                    user.save()
                    student.objects.create(user=user)
                    print("user is created")
                    return redirect('login')
            else:
                username.error(request, 'passwords doesnt mach')

                class AdminMessage(models.Model):
                    messageTitle = models.TextField(default="")
                    messageContent = models.TextField(default="")

                    def __str__(self):
                        return self.messageTitle
        return render(request, 'signup.html')

    if request.method == 'POST':
        s_id = request.POST.get('id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        college = request.POST.get('college')
        avg = request.POST.get('avg')


        user = uaa(username= firstname,password=password1)
        user1=models.addstudent()
        #user.user=user
        user1.s_id = s_id
        user1.first_name =firstname
        user1.last_name=lastname
        user1.email=email
        user1.password=password1
        user1.last_name=lastname
        user1.avg = avg
        user1.college=college
        user1.save()
        my_customer_group = Group.objects.get_or_create(name='students')
        my_customer_group[0].user_set.add(user)
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('login')