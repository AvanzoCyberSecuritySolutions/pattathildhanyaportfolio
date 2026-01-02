from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BlogPostForm
from .models import AdminUser, Post
from django.contrib.auth.hashers import check_password

from django.shortcuts import get_object_or_404

from .models import GalleryImage, HomeGalleryImage
import os
from django.conf import settings
from django.templatetags.static import static

import json
from django.core.serializers import serialize

def index(request):
    gallery_dir = os.path.join(
        settings.BASE_DIR,
        'frontend',
        'static',
        'pattathildhanya',
        'photos',
        'gallery'
    )

    image_urls = []

    if os.path.exists(gallery_dir):
        for file in sorted(os.listdir(gallery_dir)):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_urls.append(
                    static(f'pattathildhanya/photos/gallery/{file}')
                )

    return render(request, 'pattathildhanya/index.html', {
        'image_urls': image_urls
    })

def blog(request):
    return render(request, 'pattathildhanya/blog.html')

def cybersol(request):
    return render(request, 'pattathildhanya/cybersol.html')

def gallery(request):
    return render(request, 'pattathildhanya/gallery.html')



from django.contrib import messages
from django.shortcuts import render, redirect
from frontend.models import AdminUser

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            admin = AdminUser.objects.get(email=email)

            if check_password(password, admin.password):
                request.session['admin_logged_in'] = True
                return redirect("admin_dashboard")
            else:
                messages.error(request, "Invalid password")

        except AdminUser.DoesNotExist:
            messages.error(request, "Admin user not found")

    return render(request, "admin/admin_login.html")





def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect("admin_login")

    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    drafts = Post.objects.filter(status='draft').count()

    recent_posts = Post.objects.order_by('-updated_at')[:5]

    return render(request, "admin/admin_dashboard.html", {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'drafts': drafts,
        'recent_posts': recent_posts,
    })


def admin_logout(request):
    request.session.flush()
    return redirect("admin_login")

from .models import GalleryImage

def admin_gallery(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        title = request.POST.get('title')
        if image:
            GalleryImage.objects.create(image=image, title=title)
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'admin/gallery.html', {'images': images})

def delete_gallery_image(request, pk):
    img = GalleryImage.objects.get(id=pk)
    img.delete()
    return redirect('admin_gallery')

def gallery(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'pattathildhanya/gallery.html', {'images': images})

def edit_gallery_image(request):
    if request.method == "POST":
        img_id = request.POST.get("id")
        title = request.POST.get("title")

        image_obj = GalleryImage.objects.get(id=img_id)
        image_obj.title = title

        if "image" in request.FILES:
            image_obj.image = request.FILES["image"]

        image_obj.save()
        return redirect("admin_gallery")





def admin_home_gallery(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        title = request.POST.get('title')

        if image:
            HomeGalleryImage.objects.create(image=image, title=title)

    images = HomeGalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'admin/home_gallery.html', {'images': images})


def delete_home_gallery_image(request, pk):
    img = HomeGalleryImage.objects.get(id=pk)
    img.delete()
    return redirect('admin_home_gallery')

def edit_home_gallery_image(request):
    if request.method == "POST":
        img_id = request.POST.get("id")
        title = request.POST.get("title")

        image_obj = HomeGalleryImage.objects.get(id=img_id)
        image_obj.title = title

        if "image" in request.FILES:
            image_obj.image = request.FILES["image"]

        image_obj.save()
        return redirect("admin_home_gallery")


def index(request):
    images = HomeGalleryImage.objects.all().order_by('-uploaded_at')
    image_urls = [img.image.url for img in images]

    return render(request, 'pattathildhanya/index.html', {
        'image_urls': image_urls
    })




def all_posts(request):
    return render(request, "admin/all_posts.html")


def create_post(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BlogPostForm()

    return render(request, 'admin/create_post.html', {'form': form})


def blog_page(request):
    posts = Post.objects.filter(status='published').order_by('created_at')
    return render(request, 'pattathildhanya/blog.html', {
        'posts': posts
    })



def blog_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    recent_posts = Post.objects.filter(
        status='published'
    ).order_by('-created_at')[:5]

    return render(request, 'pattathildhanya/blog_detail.html', {
        'post': post,
        'recent_posts': recent_posts

    })
  

def all_posts(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    posts = Post.objects.all().order_by('-created_at')  # get all posts
    return render(request, "admin/all_posts.html", {'posts': posts})

def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'admin/edit_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('admin_dashboard')