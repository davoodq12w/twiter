from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, "blog/post_list.html", context)


def filtering(text: str):
    words = ['fuck', 'shet', 'fuck you']
    for word in words:
        if word in text:
            return False
    return True


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comment_form = CommentForm()
    comments = post.comments.filter(status=True)
    user_login = request.user
    same_person = (post.auther_id == user_login)
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'same_person': same_person,
    }
    return render(request, "blog/post_detail.html", context)


@login_required
def add_post(request, id):
    context = {}
    word_filter = True
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        user = User.objects.get(id=id)
        posts = Post.published.all()
        if form.is_valid():
            cd = form.cleaned_data
            if filtering(cd['description']) and filtering(cd['title']):
                post_obj = Post.objects.create(auther_id=id)
                post_obj.title = cd['title']
                post_obj.description = cd['description']
                post_obj.status = Post.Status.PUBLISHED
                post_obj.save()
                Image.objects.create(post=post_obj, image=form.cleaned_data['image'])
                post_obj.save()
            else:
                form = PostForm()
                word_filter = False
                context = {
                    'form': form,
                    'word_filter': word_filter,
                }
                return render(request, "forms/add_post.html", context)
            context = {
                'username': user.username,
                'id': id,
                'posts': posts
            }
            return render(request, 'blog/post_list.html', context)

    else:
        form = PostForm()
        context = {
            'form': form,
            'word_filter': word_filter,
        }
    return render(request, "forms/add_post.html", context)


def log_in(request):
    user_available = False
    password_correct = False
    posts = Post.published.all()
    context = {}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            f_username = cd['username']
            f_password = cd['password']
            try:
                user = get_object_or_404(User, username=f_username)
            except:
                login_form = LoginForm()
                context = {
                    'login_form': login_form,
                    'user_available': user_available,
                    'password_correct': password_correct,
                }
                return render(request, 'forms/login.html', context)

            if user.check_password(f_password):
                login(request, user)
                context = {
                    'username': user.username,
                    'posts': posts,
                    'id': user.id,
                }

                return render(request, 'blog/post_list.html', context)
            else:
                login_form = LoginForm()
                context = {
                    'login_form': login_form,
                    'user_available': True,
                    'password_correct': password_correct,
                }
                return render(request, 'forms/login.html', context)
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form,
            'user_available': True,
            'password_correct': True,
        }
    return render(request, 'forms/login.html', context)


def add_comment(request, post_id):
    word_filter = True
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        comment = None
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            if filtering(comment.text) and filtering(comment.auther):
                comment.status = True
                comment.post = post
                comment.save()
            else:
                word_filter = False
                comment_form = CommentForm()
                context = {
                    'comment_form': comment_form,
                    'word_filter': word_filter
                }
                return render(request, 'forms/add_comment.html', context)

        context = {
            'post': post,
            'comment_form': comment_form,
            'comment': comment,
            'word_filter': word_filter
        }
        return render(request, 'forms/add_comment.html', context)
    else:
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'word_filter': word_filter
        }
    return render(request, 'forms/add_comment.html', context)


def post_search(request):
    query = None
    posts_results = []
    images_results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = Post.published.annotate(similarity=TrigramSimilarity('title', query)) \
                .filter(similarity__gt=0.1)
            results2 = Post.published.annotate(similarity=TrigramSimilarity('description', query)) \
                .filter(similarity__gt=0.1)
            results3 = Image.objects.annotate(similarity=TrigramSimilarity('title', query)) \
                .filter(similarity__gt=0.1)
            results4 = Image.objects.annotate(similarity=TrigramSimilarity('description', query)) \
                .filter(similarity__gt=0.1)
            posts_results = (results1 | results2).order_by('-similarity')
            images_results = (results3 | results4).order_by('-similarity')
    context = {
        'query': query,
        'posts_results': posts_results,
        'images_results': images_results,
    }
    return render(request, 'blog/post_search.html', context)


@login_required
def delete_post(request, id):
    context = {
        'id': id,
    }
    return render(request, 'blog/delete_post.html', context)


@login_required
def delete_post_confirmed(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    posts = Post.published.all()
    user = User.objects.get(id=post.auther_id)

    context = {
        'posts': posts,
        'username': user.username,
        'id': user.id,
    }
    return render(request, "blog/post_list.html", context)


def add_account(request):
    context = {}
    username_available = False
    password_match = True
    posts = Post.published.all()
    if request.method == 'POST':
        form = AddAccountForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            for user in User.objects.all():
                if user.username == cd['username']:
                    username_available = True
                    form = AddAccountForm()
                    context = {
                        'form': form,
                        'username_available': username_available,
                        'password_match': password_match,
                    }
                    return render(request, 'forms/add_account.html', context)

            if cd['password'] == cd['confirm_password']:
                user = User.objects.create()
                user.username = cd['username']
                user.set_password(cd['password'])
                user.save()
                context = {
                    'username': user.username,
                    'id': user.id,
                    'posts': posts,
                }
                return render(request, 'blog/post_list.html', context)
            else:
                password_match = False
                form = AddAccountForm()
                context = {
                    'form': form,
                    'username_available': username_available,
                    'password_match': password_match,
                }
                return render(request, 'forms/add_account.html', context)
    else:
        form = AddAccountForm()
        context = {
            'form': form,
            'username_available': username_available,
            'password_match': password_match,
        }
    return render(request, 'forms/add_account.html', context)


@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    posts = Post.published.filter(auther_id=id)
    context = {
        'user': user,
        'posts': posts,
        'id': id,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request, id):
    context = {}

    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        user = User.objects.get(id=id)
        if form.is_valid():
            cd = form.cleaned_data
            user.username = cd['username']
            if cd['confirm_password'] == cd['password']:
                posts = Post.published.filter(auther_id=id)
                user.set_password(cd['password'])
                user.save()
                context = {
                    'id': id,
                    'user': user,
                    'posts': posts,
                }
                return render(request, 'blog/profile.html', context)
            else:
                form = EditProfileForm()
                context = {
                    'form': form,
                    'id': id,
                    'password_match': False,
                }
                return render(request, 'forms/edit_profile.html', context)
    else:
        form = EditProfileForm()
        context = {
            'form': form,
            'id': id,
            'password_match': True,
        }
    return render(request, 'forms/edit_profile.html', context)


@login_required
def delete_account(request, id):
    user = User.objects.get(id=id)
    posts = Post.published.filter(auther_id=id)
    context = {
        'id': id,
        'posts': posts,
        'user': user,
    }
    return render(request, 'blog/delete_account.html', context)


@login_required
def delete_account_confirmed(request, id):
    user = User.objects.get(id=id)
    user.delete()
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, "blog/post_list.html", context)


def home_screen(request):
    posts = Post.published.all()
    if request.user:
        user = User.objects.get(id=request.user.id)
        context = {
            'username': user.username,
            'posts': posts,
            'id': user.id,
        }
        return render(request, 'blog/post_list.html', context)
    return redirect('blog:post_list')
