from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user      = models.OneToOneField(User,on_delete=models.CASCADE) 
    phone     = models.CharField("电话",max_length=11,unique=True,null=True,blank=True)
    sexChoice = (("男","男"),("女","女"),("保密","保密"))
    sex       = models.CharField("性别",choices=sexChoice,default="男",max_length=2)
    avatar    = models.ImageField(upload_to="avatar/%Y/%m/%d",default="avatar/defa/avatar.jpg",
                               max_length=200,verbose_name="头像")
    levelChoice = (("1","虾米"),("2","小鱼"),("3","大鱼"),("4","鲨鱼"),("5","虎鲸"),("6","渔夫"),("0","污泥"))
    level     = models.CharField("级别",choices=levelChoice,default="1",max_length=2)

    def get_info_url(self):
        return reverse('person_info',args=[self.user.pk])

    #username  = models.CharField("姓名",max_length=20)
    #email     = models.EmailField("邮箱")
    #created   = models.DateTimeField(auto_now_add=True)
    #updated   = models.DateTimeField(auto_now=True)
    #active    = models.BooleanField("帐号激活",default=True)
    


class ArticlePulished(models.Manager):

    def get_queryset(self):
        return super(ArticlePulished,self).get_queryset().filter(draft=True).filter(publish=True)

class Article(models.Model):
    title     = models.CharField("标题",max_length=50)
    author    = models.ForeignKey(User,verbose_name="作者",related_name="articles")
    content   = RichTextField("内容",config_name='article_ckeditor')
    view      = models.IntegerField("浏览量",default=0)
    click     = models.IntegerField("点赞",default=0)
    draft     = models.BooleanField("现在发表",default=True)
    publish   = models.BooleanField("是否发表",default=True)
    created   = models.DateTimeField("创建时间",auto_now_add=True)
    updated   = models.DateTimeField("更新时间",auto_now=True)
    top       = models.BooleanField("置顶",default=False)
    folower   = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="likearticles")
    tags      = TaggableManager()

    objects = models.Manager()
    getPublished = ArticlePulished()


    def __str__(self):
        
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail',kwargs={'pk':self.pk})


    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    author  = models.ForeignKey(User,verbose_name="作者")
    article = models.ForeignKey(Article,related_name="comments")
    content =  RichTextField("评论",config_name='comment_ckeditor')
    created   = models.DateTimeField("创建时间",auto_now_add=True)
    updated   = models.DateTimeField("更新时间",auto_now=True)
    active    = models.BooleanField("激活",default=True)
    
    def __str__(self):

        return "%s's comments"%self.article

    class Meta:
        ordering = ('-created',)

