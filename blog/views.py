from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.db.models import Count
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Article,Profile
from .forms import CommentForm,UserRegistrationForm,ArticleForm,UserEditForm, ProfileEditForm

from taggit.models import Tag

# Create your views here.


def setting(request):
    hot_articles = Article.getPublished.filter(top=True)
    if not hot_articles:
        hot_articles = Article.getPublished.order_by('-click')[:5]
    tags = Tag.objects.annotate(num_art=Count('article')).order_by('-num_art')
    tag1 = tags[:3]
    tag2 = tags[3:6]
    return {"hot_articles":hot_articles,"tag1":tag1,"tag2":tag2}


@require_POST
def findTitleView(request):
    title = request.POST.get('findArticle')
    return HttpResponseRedirect(reverse('article_find',args=[title,1]))




def findListView(request,pl,flag):

    if flag=='1':
        object_list = Article.getPublished.filter(title__icontains=pl)
    else:
        tag = get_object_or_404(Tag,name=pl)
        object_list = Article.getPublished.filter(tags__in=[tag])

    paginator = Paginator(object_list,3)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request,'blog/findlist.html',{'object_list':contacts}) 



class ArticleListView(ListView):
    model = Article
    template_name = 'blog/index.html'
    paginate_by = 4
    paginate_orphans=2

    def get_context_data(self,**kwargs):
        context = super(ArticleListView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    def get_queryset(self):
        return super(ArticleListView,self).get_queryset().filter(publish=True)
        





class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'

    def get_context_data(self,**kwargs):
        context = super(ArticleDetailView,self).get_context_data(**kwargs)

        article = self.get_object()
        comments=article.comments.filter(active=True)
        article.view +=1
        article.save()
        context['comments']=comments
        context['now']=timezone.now()
        context['forms']=CommentForm()
        return context

@login_required
@require_POST
def articlelike(request):
    article_id = request.POST.get('id')

    #action = request.POST.get('action')
    if article_id:
        try:
            article = Article.objects.get(pk=article_id)
            folower = article.folower.filter(pk=request.user.pk)
            if folower:
                article.click -=1
                article.folower.remove(request.user)
            else:
                article.click +=1
                article.folower.add(request.user)
                
            article.save()

            return JsonResponse({'status':'ok','likeNum':article.click})
        except:
            pass
    return JsonResponse({'status':'ko'})


@login_required
def commentView(request,pk):
    if request.method=="POST":
        article = Article.objects.get(pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = article
            new_comment.save()
    return HttpResponseRedirect(reverse('article_detail',args=[pk]))
 

@login_required
def articleCreateView(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            new_article = article_form.save(commit=False)
            new_article.author = request.user 
            new_article.save()
            tags = article_form.cleaned_data['tags']
            for tag in tags:
                obj,created=Tag.objects.get_or_create(name=tag)
                new_article.tags.add(obj)
            
            return HttpResponseRedirect(reverse('article_detail',args=[new_article.pk]))
    else:
        article_form = ArticleForm()
    return render(request,'blog/articlecreate.html',{'article_form':article_form})

@login_required
def articleEditView(request,pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        article_form = ArticleForm(instance=article,data=request.POST)
        if article_form.is_valid():
            aticle = article_form.save()
            tags = article_form.cleaned_data['tags']
            for tag in tags:
                obj,created=Tag.objects.get_or_create(name=tag)
                article.tags.add(obj)
            return HttpResponseRedirect(reverse('article_detail',args=[pk]))
    else:
        article_form = ArticleForm(instance=article)
    return render(request,'blog/articleEdit.html',{'article_form':article_form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,"registration/register_done.html",{"username":new_user.username})
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'user_form':user_form})

@login_required
def personInfoEditView(request):
    if request.method=="POST":
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return HttpResponseRedirect(reverse("person_info",args=[request.user.pk]))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'blog/personInfoEdit.html',{'user_form':user_form,'profile_form':profile_form})

def personInfoView(request,pk):
    user = User.objects.get(pk=pk)
    flag = False
    if str(request.user.pk) == pk:
        articles = user.articles.all()
        flag = True
    else:
        articles = user.articles.filter(publish=True,draft=True)
    return render(request,'blog/personInfo.html',{"user":user,
                                                  "profile":user.profile,
                                                  "articles":articles,
                                                  "flag":flag})



'''
@require_POST
@login_required
def articlelike(request):
    user = request.user
    with open("/home/myven/dgp/ItBlog/log.txt","a") as f:
        f.write(user.username + str(timezone.now()))
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = Article.objects.get(pk=article_id)
            if action == 'like':
                article.click +=1
            else:
                article.click -=1
            article.save()
            return JsonResponse({'status':'ok','likeNum':article.click})
        except:
            pass
    return JsonResponse({'status':'ko'})
'''
