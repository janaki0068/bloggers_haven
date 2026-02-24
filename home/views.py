from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Comment, Like, Profile
from django.contrib import messages
from .forms import ArticleForm, CommentForm, BioForm

# Create your views here.
# home page
def index(request):
    trending_articles = Article.objects.filter(is_trending=True)
    return render(request, 'index.html', {
        'trending_articles' : trending_articles
    })

# signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('home')

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully!")
        return redirect('home')
        
    return redirect('home')
    
# login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
            
    return redirect('home')
    
# logout
def logout_view(request):
    logout(request)
    return redirect('home')
    
# dashboard
@login_required
def dashboard(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'articles': articles})
    
# create post
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id)

        Article.objects.create(
            author = request.user,
            title = title,
            content = content,
            category = category,
            image = image
            )
        messages.success(request, "Post created successfully!")
        return redirect('create_post')
        
    categories = Category.objects.all()
    return render(request, 'create_post.html', {'categories': categories})
    
# sidebar features
@login_required
def my_blogs(request):
    blogs = Article.objects.filter(author=request.user).order_by('-created_at')

    for blog in blogs:
        blog.liked_by_user = blog.likes.filter(user=request.user).exists()

    return render(request, 'my_blogs.html', {'blogs':blogs})

@login_required
def categories(request):
    category_list = Category.objects.all()
    return render(request, 'categories.html', {'categories': category_list})

@login_required
def category_blogs(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    blogs = Article.objects.filter(category=category).order_by('-created_at')
    return render(request, 'category_blogs.html',{
        'category':category,
        'blogs': blogs
    })

# edit post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Article, id=post_id, author=request.user)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            messages.success(request, "post updated successfully !")
            return redirect('my_blogs')
    else:
        form = ArticleForm(instance=post)
    return render(request, 'edit_post.html', {'form':form, 'post':post})

# delete post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Article, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('my_blogs')
    return render(request, 'confirm_delete.html', {'post': post})

# comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Article, id=post_id)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('article_detail', post_id=post.id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('my_blogs')  # only owner can edit

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('article_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)


    previous_url = request.META.get('HTTP_REFERER', f"/article/{comment.post.id}/")
    return render(request, 'edit_comment.html', {'form': form, 'previous_url': previous_url})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# like
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Article, id=post_id)
    like_obj = Like.objects.filter(post=post, user=request.user).first()
    if like_obj:
        like_obj.delete()
    else:
        Like.objects.create(post=post, user=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))



def home(request):
    category_id = request.GET.get('category')

    if category_id:
        articles = Article.objects.filter(category_id=category_id).order_by('-created_at')
    else:
        articles = Article.objects.all().order_by('-created_at')

    trending_posts = Article.objects.filter(is_trending=True).order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'articles': articles,
        'trending_posts': trending_posts,
        'categories': categories,
    }

    return render(request, 'index.html', context)


def article_detail(request, post_id):
    article = get_object_or_404(Article, id=post_id)

    # Only check likes if user is authenticated
    if request.user.is_authenticated:
        article.liked_by_user = article.likes.filter(user=request.user).exists()
    else:
        article.liked_by_user = False

    return render(request, 'article_detail.html', {'article': article})

def my_view(request):
    previous_url = request.META.get("HTTP_REFERER", "/dashboard/")
    return render(request, "template.html", {
        "previous_url": previous_url
    })

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    articles = user.articles.all().order_by('-created_at')
    next_url = request.GET.get('next', None)

    return render(request, 'user_profile.html', {
        'profile_user': user,
        'articles': articles,
        'next_url' : next_url
    })

@login_required
def edit_bio(request):
    # Make sure the profile exists; create it if it doesn't
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BioForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = BioForm(instance=profile)

    return render(request, 'edit_bio.html', {'form': form})


