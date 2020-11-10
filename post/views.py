from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Comment,Author,Category
from .forms import CommentForm,PostForm
from marketing.models import Signup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))
    return queryset

def get_author(user):
    qs=Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset=Post.objects.all()
    query=request.GET.get('q')
    if query:
        queryset=queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context={
        'queryset':queryset
    }
    return render(request,'search_result.html',context)


def index(request):
    featured=Post.objects.filter(featured=True)
    latest=Post.objects.order_by('-timestamp')[0:3]
    if request.method == 'POST':
        email=request.POST['email']
        new_signup=Signup()
        new_signup.email=email
        new_signup.save()
    return render(request,'index.html',{'object_list':featured,'latest':latest})

def blog(request):
    catcount=category_count()
    post_list=Post.objects.all()
    paginator=Paginator(post_list,4)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    page_request_var='page'
    page=request.GET.get(page_request_var)
    # categories=Category.objects.all()
    try:
        paginator_queryset=paginator.page(page)
    except PageNotAnInteger:
        paginator_queryset=paginator.page(1)
    except EmptyPage:
        paginator_queryset=paginator.page(paginator.num_pages)
    return render(request, 'blog.html',{'queryset':paginator_queryset,
    'page_request_var':page_request_var,'most_recent':most_recent,
    'category_count':catcount})

def post(request, id):
    post=get_object_or_404(Post,id=id)
    catcount = category_count()
    form=CommentForm(request.POST or None)
    comments=Comment.objects.filter(post=post)
    if request.method=='POST':
        if form.is_valid:
            form.instance.post=post
            form.save()
            form=CommentForm()
            return HttpResponseRedirect(request.path_info)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    context = {'post': post, 'most_recent': most_recent,
               'category_count': catcount,
               'form':form,'comments':comments}
    return render(request, 'post.html',context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    author=get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author=author
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': form.instance.id}))
    context = {'form': form}
    return render(request, 'post_create.html', context)


def post_update(request, id):
    post=get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=post)
    author=get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author=author
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': form.instance.id}))
    context = {'form': form}
    return render(request, 'post_create.html', context)


def post_delete(request, id):
    post=get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))


def cat_view(request,id):
    post=Post.objects.filter(categories__id=id)
    category=Category.objects.get(id=id)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    catcount = category_count()
    context = {'posts': post, 'cat': category,
               'category_count': catcount, 'most_recent': most_recent}

    return render(request, 'category.html',context)
