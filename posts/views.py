from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Post
from marketing.models import Signup
from django.db.models import Count, Q

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset.order_by('-categories__title__count')

def get_year_count():
    queryset = Post.objects.values('timestamp__year').annotate(Count('timestamp__year'))
    return queryset.order_by('-timestamp__year')


def index(request):
    featured = Post.objects.filter(featured = True)
    latest = Post.objects.order_by("-timestamp")[0:3]
    gallery = Post.objects.order_by("-timestamp")[0:4]

    if request.method == "POST":
        email = request.POST["email"]
        if email!="" and not Signup.objects.filter(email = email).exists():
            new_signup = Signup()
            new_signup.email = email
            new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'gallery': gallery,
        'navbar_active': 'home',
    }

    return render(request, 'index.html', context)

def blog(request):
    category_count = get_category_count()
    year_count = get_year_count()
    post_list = Post.objects.order_by("-timestamp")
    latest = post_list[0:3]
    
    post_count = post_list.count()

    category_request = request.GET.get('category')
    year_request = request.GET.get('year')

    if category_request:
         post_list = post_list.filter(categories__title = category_request.capitalize()).order_by('timestamp')

    if year_request:
         post_list = post_list.filter(timestamp__year = year_request).order_by('timestamp')

    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count,
        'year_count': year_count,
        'post_count': post_count,
        'navbar_active': 'blog',
    }

    return render(request, 'blog.html', context)

'''
def blog_category(request, category):
    year_count = get_year_count()
    category_count = get_category_count()
    post_list = Post.objects.order_by("-timestamp")
    latest = post_list[0:3]
    post_count = post_list.count()
    post_list = post_list.filter(categories__title = category.capitalize()).order_by('-timestamp')

    paginator = Paginator(post_list, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count,
        'year_count': year_count,
        'post_count': post_count,
        'navbar_active': 'blog',
    }

    return render(request, 'blog.html', context)

def blog_year(request, year):
    year_count = get_year_count()
    category_count = get_category_count()
    post_list = Post.objects.order_by("-timestamp")
    latest = post_list[0:3]
    post_count = post_list.count()
    post_list = post_list.filter(timestamp__year = year).order_by('-timestamp')

    
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count,
        'year_count': year_count,
        'post_count': post_count,
        'navbar_active': 'blog',
    }

    return render(request, 'blog.html', context)
'''
def post(request, slug, id):
    post = get_object_or_404(Post, id=id)
    post.view_count += 1
    post.save()

    year_count = get_year_count()
    category_count = get_category_count()
    latest = Post.objects.order_by("-timestamp")[0:3]
    post_list = Post.objects.all()
    post_count = post_list.count()

    try:
        next_post  = post.get_next_by_timestamp()
    except:
        next_post = None

    try:
        prev_post  = post.get_previous_by_timestamp()
    except:
        prev_post = None
    

    context = {
        'post': post,
        'latest': latest,
        'category_count': category_count,
        'year_count': year_count,
        'post_count': post_count,
        'next_post': next_post,
        'prev_post': prev_post,
        'navbar_active': 'post',

    }
    return render(request, 'post.html', context)

def latest_post(request):
    
    year_count = get_year_count()
    category_count = get_category_count()
    latest = Post.objects.order_by("-timestamp")[0:3]
    post_list = Post.objects.all()
    post_count = post_list.count()
    post = latest[0]
    post.view_count += 1
    post.save()


    try:
        next_post  = post.get_next_by_timestamp()
    except:
        next_post = None

    try:
        prev_post  = post.get_previous_by_timestamp()
    except:
        prev_post = None
    

    context = {
        'post': post,
        'latest': latest,
        'category_count': category_count,
        'year_count': year_count,
        'post_count': post_count,
        'next_post': next_post,
        'prev_post': prev_post,
        'navbar_active': 'post',

    }
    return render(request, 'post.html', context)


def search(request):
    year_count = get_year_count()
    category_count = get_category_count()
    post_list = Post.objects.order_by("-timestamp")
    latest = post_list[0:3]
    post_count = post_list.count()
    
    query = request.GET.get('q')

    if query:
        post_list = post_list.filter(
            Q(title__icontains = query) |
            Q(overview__icontains = query)
        ).distinct()

    
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'latest': latest,
        'category_count': category_count,
        'year_count': year_count,
        'post_count': post_count,
        'navbar_active': 'blog',
    }

    return render(request, 'blog.html', context)