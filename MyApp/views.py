from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User, auth
from django.views.generic import DeleteView
from MyApp.models import UProfile
from django.urls import reverse
from MyApp.models import Job


# Create your views here.
from MyApp.forms import CreatePostForm
from MyApp.models import Post, Contact
from MyApp.models import PostComment
from MyApp.templatetags import extras



def view_posts(request):
    context = {}

    posts = Post.objects.all().filter(status=True)
    context['posts'] = posts
    return render(request, 'view_status.html', context)


def your_area(request):
    context = {}
    user = request.user
    posts = Post.objects.filter(author=user, status=True)
    context['posts'] = posts
    return render(request, 'view_area.html', context)


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['pass']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'invalid user')
            return redirect('MyApp:login')

    else:
        return render(request, 'login.html')


# for registeration
def reg(request):
    if request.method == 'POST':
        first_name = request.POST['First Name']
        last_name = request.POST['Last Name']
        username = request.POST['User Name']
        password1 = request.POST['Password']
        password2 = request.POST['Confirm Password']
        email = request.POST['Email Id']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User name taken')
                return redirect('MyApp:reg')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'emial taken')
                return redirect('MyApp:reg')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                print('user created')
        else:
            messages.info(request, 'password is not matching')
            return redirect('MyApp:reg')
        return redirect('MyApp:login')
    else:
        return render(request, 'reg.html')


def logout(request):
    auth.logout(request)
    return redirect('MyApp:index')


@login_required
def post_report(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        context['message'] = 'To report the post, You have to login first.'
    post_form = CreatePostForm(request.POST or None)
    if post_form.is_valid():
        post_form = post_form.save(commit=False)
        author = User.objects.filter(email=user.email).first()
        post_form.author = author
        post_form.save()
        context['message'] = 'Your Post has been created successfully. '
    post_form = CreatePostForm()
    context['post_form'] = post_form
    return render(request, 'post_report.html', context)


def contact1(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname', '')
        last_name = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        feedback = request.POST.get('feedback', '')
        contact1 = Contact(contact_first=first_name, contact_last=last_name,
                           contact_email=email, contact_subject=subject, contact_feedback=feedback)
        contact1.save()
        messages.success(request, 'Your Query Successfully Submitted. ')
        return render(request, 'contact.html')
    else:
        return render(request, 'contact.html')




def about1(request):
    return render(request, 'about.html')


def job1(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        country = request.POST.get('country', '')
        pnumber = request.POST.get('phone', '')
        tech = request.POST.get('technology', '')
        exp = request.POST.get('E_Y', '')
        company =request.POST.get('subject', '')
        quall = request.POST.get('education', '')
        resume = request.POST.get('file upload', '')
        user = request.user
        posts = Post.objects.filter(author=user).count()
        if posts >= 2:
            job1 = Job(job_name=name, job_email=email, job_country=country, job_contact=pnumber,job_tech=tech,job_exp=exp,job_company=company,job_qual=quall,job_resume=resume)

            job1.save()
            messages.info(request, 'Your form Successfully Submitted. ')
            return render(request, 'jobs.html')
        else:
            messages.info(request, 'you should have atleast 2 posts to apply this job. ')
            return render(request, 'jobs.html')

    else:
        return render(request, 'jobs.html')


def detail_view(request, pk):
    context = {}

    post = get_object_or_404(Post, pk=pk)
    # Passing Comments
    comments = PostComment.objects.filter(post=post, parent=None)
    replies = PostComment.objects.filter(post=post).exclude(parent=None)
    replydict = {}
    for reply in replies:
        if reply.parent.pk not in replydict.keys():
            replydict[reply.parent.pk] = [reply]
        else:
            replydict[reply.parent.pk].append(reply)
    context['comments'] = comments
    context['replydict'] = replydict
    context['post'] = post

    return render(request, 'detail.html', context)



def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        postpk = request.POST.get('postpk')
        post = Post.objects.get(pk=postpk, status=True)
        parentpk = request.POST.get('parentpk')
        if parentpk == '':
            comment = PostComment(comment=comment, user=user, post=post)
            comment.save()
        else:
            parent = PostComment.objects.get(pk=parentpk)
            comment = PostComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
    return redirect("MyApp:view_posts")



def seeprofile(request):
    context = {}
    profile = UProfile.objects.all()
    context = {'profile': profile}
    return render(request, 'showp.html', context)


def dev_info(request):
    return render(request,'dev_info.html')


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/view_status'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.name:
            return True
        return False
