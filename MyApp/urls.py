from django.urls import path
from MyApp import views
from django.contrib.auth import views as auth_views

app_name = 'MyApp'

urlpatterns = [
    path('postComment/', views.postComment, name='postComment'),
    path('contact/', views.contact1, name='contact'),
    path('posts/', views.view_posts, name='view_posts'),
    path('area/', views.your_area, name='your_area'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('logout/', views.logout, name='logout'),
    path('post_report/', views.post_report, name='post_report'),
    path('about/',views.about1, name='about'),
    path('showp/',views.seeprofile,name='showp'),
    path('job/', views.job1, name='jobs'),
    path('dev_info/',views.dev_info,name='dev_info'),
    path('<pk>/', views.detail_view, name='detail'),





    # path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
    # name='password_reset'), path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
    # template_name='password_reset_done.html'),name='password_reset_done'),

]
