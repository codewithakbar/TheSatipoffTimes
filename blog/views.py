from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count

from django.contrib.auth.models import User
from blog.forms import EmailPostForm, CommentForm
from .models import FilesAdmin, Post, Comment, Category
from taggit.models import Tag
from .data_parse.parse_csgo import collect_data
from .templatetags.blog_tags import get_most_commented_posts

def rek_list(request):
    post_tag = Post.tags.all()

    post_tags_ids = post_tag.values_list('id', flat=True)    

    avto_sim = Post.published.filter(tags__in=post_tags_ids)
    avto_sim = avto_sim.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[14:]

    return render(request, 'blog/post/asosiy.html', {
        'avto_sim': avto_sim,
    })


def asosiy_list(request, tag_slug=None):
    object_list = Post.published.all()
    categories = Category.objects.get(name="Avto")
    post_tag = Post.tags.all()
    postla = Post.objects.all()
    

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    #List of similar posts
    post_tags_ids = post_tag.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]

    # One of similar post
    one_similar_post = Post.published.filter(tags__in=post_tags_ids)
    one_similar_post = one_similar_post.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:1]

    # get most commeted post
    one_most_com_post = get_most_commented_posts(count=1)

    # 4dan keyingi
    tort_keyin_similar = Post.published.filter(tags__in=post_tags_ids)
    tort_keyin_similar = tort_keyin_similar.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[5:9]

    # 9dan keyingi
    toqqiz_keyin_similar = Post.published.filter(tags__in=post_tags_ids)
    toqqiz_keyin_similar = toqqiz_keyin_similar.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[9:14]

    # footer rek 
    avto_sim = Post.published.filter(tags__in=post_tags_ids)
    avto_sim = avto_sim.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[14:17]


    paginator = Paginator(object_list, 9) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)


    return render(request,
                 'blog/post/asosiy.html',
                 {'tag': tag,
                  'page': page,
                  'posts': posts,
                  'postla': postla,
                  'post_tag': post_tag,
                  'avto_sim': avto_sim,
                  'categories': categories,
                  'similar_posts': similar_posts,
                  'one_similar_post': one_similar_post,
                  'one_most_com_post': one_most_com_post,
                  'tort_keyin_similar': tort_keyin_similar,
                  'toqqiz_keyin_similar': toqqiz_keyin_similar})


def post_list(request, tag_slug=None,  category_slug=None):
    categories = Category.objects.all()
    object_list = Post.published.all()
    post_tag = Post.tags.all()
    category = None
    tag = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list, 9) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                 'blog/post/list.html',
                 {'page': page,
                  'posts': posts,
                  'post_tag': post_tag,
                  'tag': tag,
                  'category': category,
                  'categories': categories})


def post_detail_tag(request, tag_slug=None):
    object_list = Post.published.all()
    post_tag = Post.tags.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 9) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',
                 {
                    'tag': tag,
                    'page': page,
                    'posts': posts,
                    'post_tag': post_tag,

                  })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # post viewers
    post.views = post.views + 1
    post.save()

    # list of active comments for this list
    comments = post.comments.filter(active=True)

    post_tag = Post.tags.all()

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment obj but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]    

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                  'comments': comments,
                  'new_comment': new_comment,
                  'comment_form': comment_form,
                  'post_tag': post_tag,
                  'similar_posts': similar_posts}) 



def post_share(request, post_id):
    # retrive post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 9
    template_name = 'blog/post/list.html'





