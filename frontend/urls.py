from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog_page, name='blog'),
    path('cybersol/', views.cybersol, name='cybersol'),
    path('gallery/', views.gallery, name='gallery'),

    path("myadmin/", views.admin_login, name="admin_login"),
    path("myadmin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path('myadmin/gallery/', views.admin_gallery, name='admin_gallery'),
    path('myadmin/create-post/', views.create_post, name='create_post'),
    path('myadmin/all-posts/', views.all_posts, name='all_posts'),
    path('myadmin/admin-logout/', views.admin_logout, name='admin_logout'),
    path('myadmin/edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('myadmin/delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('myadmin/gallery/', views.admin_gallery, name='admin_gallery'),
    path('myadmin/gallery/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    path("myadmin/gallery/edit/", views.edit_gallery_image, name="edit_gallery_image"),

    # new home gallery
    path('amydmin/home_gallery/', views.admin_home_gallery, name='admin_home_gallery'),
    path('myadmin/home_gallery/delete/<int:pk>/', views.delete_home_gallery_image, name='delete_home_gallery_image'),
    path('myadmin/home_gallery/edit/', views.edit_home_gallery_image, name='edit_home_gallery_image'),

    
]

