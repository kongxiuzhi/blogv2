from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$',views.ArticleListView.as_view(),name='article_list'),
    url(r'^article/(?P<pk>\d+)/$',views.ArticleDetailView.as_view(),name='article_detail'),
    url(r'^article/create/$',views.articleCreateView,name='article_create'),
    url(r'^article/edit/(?P<pk>\d+)/$',views.articleEditView,name='article_edit'),
    url(r'^article/like/$',views.articlelike,name='like'),
    url(r'^comment/(?P<pk>\d+)/$',views.commentView,name="article_comment"),
    url(r'^find/(?P<pl>.*?)/(?P<flag>\d+)/$',views.findListView,name='article_find'),
    url(r'^findTitle/',views.findTitleView,name='article_title_find'),
    url(r'^edit/user/$',views.personInfoEditView,name="person_info_edit"),
    url(r'^user/(?P<pk>\d+)/$',views.personInfoView,name="person_info"),
    url(r'^register/$',views.register,name="register"),
]