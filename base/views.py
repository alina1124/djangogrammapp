from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Post, Tag, PostImage, Comment, Reply
from .forms import PostForm, UserLoginFrom, UserRegisterForm, PostImageForm, CommentForm, ReplyForm
from django.db.models import Count, Q, F
from user_profile.models import Profile
from .tokens import account_activation_token


# Create your views here.

def get_pre_url(request):
    return request.META.get('HTTP_REFERER')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Thank you for your email confirmation.")
        return redirect('profile', username=user.username)
    else:
        messages.error(request, "Activation link is invalid!")


def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("base/activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = send_mail(mail_subject, message, '', [to_email], fail_silently=True)
    if email:
        success_mess = f"We have sent you a confirmation email to the {to_email}. " \
                       f"Please, follow the link in the email to finish registration."
        messages.success(request, success_mess)
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@login_required(login_url='login')
def home(request):
    user = request.user
    user_prof = Profile.objects.get(user=user)
    following = user_prof.following.all()
    posts = Post.objects.filter(Q(user__in=following) | Q(user=user)).order_by('-created_at')

    users = User.objects.exclude(username=user.username).order_by('-date_joined')[:5]

    return render(request, 'base/home.html', {
        'title': 'Djangogramm',
        'posts': posts,
        'users': users
    })


@login_required(login_url='login')
def create_post(request):
    user = request.user
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = user
            post.save()
            tags = request.POST.get('tags')
            if tags != '':
                for tag in tags.split(' '):
                    tag = tag.strip()
                    if not tag.startswith('#'):
                        tag = f'#{tag}'
                    new_tag = Tag.objects.filter(caption=tag).first()
                    if new_tag is None:
                        new_tag = Tag.objects.create(caption=tag)
                    new_tag.posts.add(post)

            for file in files:
                PostImage.objects.create(post=post, image=file)
            messages.success(request, 'Post successfully created!')

            return redirect('post-view', post_id=post.id)
        else:
            messages.error(request, 'Post creation error!')
    else:
        post_form = PostForm()

    return render(request, 'base/create_post.html', {
        'title': 'Create new post | Djangogramm',
        'post_form': post_form
    })


def user_signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('signup')
    else:
        form = UserRegisterForm()

    return render(request, 'base/signup.html', {
        'form': form,
        'title': 'Sign up'
    })


def user_login(request):
    if request.method == 'POST':
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = UserLoginFrom()

    return render(request, 'base/login.html', {
        'title': 'Log in',
        'form': form
    })


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


def delete_post(request):
    post_id = request.GET.get('post_id')
    pre_url = get_pre_url(request)

    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('profile', username=post.user.username)

    return render(request, 'base/delete_post.html', {
        'pre_url': pre_url,
    })


@login_required(login_url='login')
def post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    user = post.user
    images = PostImage.objects.filter(post=post)
    tags = Tag.objects.filter(posts=post)

    return render(request, 'base/post_view.html', {
        'post': post,
        'user': user,
        'images': images,
        'tags': tags
    })


@login_required(login_url='login')
def like_post(request):
    user = request.user
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    if user in post.likes.all():
        post.likes.remove(user)
        return redirect(get_pre_url(request))
    else:
        post.likes.add(user)
        return redirect(get_pre_url(request))


@login_required(login_url='login')
def tag_view(request, tag_name):
    tag = Tag.objects.get(caption=tag_name)
    posts = tag.posts.all()
    last_post = posts.first()

    return render(request, 'base/tag.html', {
        'tag': tag,
        'posts': posts,
        'last_post': last_post
    })


@login_required(login_url='login')
def explore(request):
    posts = Post.objects.all()
    return render(request, 'base/explore.html', {
        'title': 'Explore',
        'posts': posts
    })


@login_required(login_url='login')
def search(request):
    user = request.user
    search_query = request.GET.get('search', '')
    users = ''
    tags = ''

    if search_query and not search_query.startswith('#'):
        users = User.objects.filter(username__icontains=search_query)
    elif search_query and search_query.startswith('#'):
        if search_query == '#':
            tags = Tag.objects.all()
        else:
            tags = Tag.objects.filter(caption__icontains=search_query)
    recently_users = User.objects.exclude(username=user.username).order_by('-date_joined')[:5]
    return render(request, 'base/search.html', {
        'title': 'Search',
        'user': user,
        'recently_users': recently_users,
        'users': users,
        'tags': tags
    })


@login_required(login_url='login')
def comment(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    images = PostImage.objects.filter(post=post)
    tags = Tag.objects.filter(posts=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = user
            comm.post = post
            comm.save()
            return redirect('comment', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'base/comment.html', {
        'title': 'Comment',
        'post': post,
        'images': images,
        'tags': tags,
        'form': form
    })


def like_comment(request):
    user = request.user
    comment_id = request.GET.get('comment_id')
    comm = Comment.objects.get(id=comment_id)

    if user in comm.likes.all():
        comm.likes.remove(user)
        return redirect(get_pre_url(request))
    else:
        comm.likes.add(user)
        return redirect(get_pre_url(request))


def reply(request, comment_id):
    user = request.user
    reply_to = Comment.objects.get(id=comment_id)
    post = reply_to.post
    form = ReplyForm(request.POST)
    if form.is_valid():
        comm = form.save(commit=False)
        comm.user = user
        comm.reply_to = reply_to
        comm.save()
        return redirect('comment', post_id=post.id)
