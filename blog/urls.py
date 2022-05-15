from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('category/', views.post_list, name='post_list'),
    path('', views.asosiy_list, name='asosiy_list'),    
    # path('category/', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_detail_tag, name='post_detail_by_tag'),
    path('<slug:category_slug>/', views.post_list, name='product_list_by_category'),

    # Bosh menu uchun "url"lar
    path('mahalliy/', views.post_list, name='mahalliy'),
    path('texno/', views.post_list, name='texno'),
    path('sport/', views.post_list, name='sport'),
    path('avto/', views.post_list, name='avto'),
    path('madaniyat/', views.post_list, name='madaniyat'),
    path('dunyo/', views.post_list, name='dunyo'),
    path('lifestyle/', views.post_list, name='lifestyle'), 
    path('kolumnistlar/', views.post_list, name='kolumnistlar'),

]
