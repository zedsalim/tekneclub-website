import uuid
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from users.models import UserProfile
from chat_messages.forms import ContactUsForm
from .forms import *
from .models import *


def homePage_view(request):
    first_blogs = Post.objects.filter(status='Published', post_type='Blog').order_by('-created_at')[:2]
    first_events = Post.objects.filter(status='Published', post_type='Event').order_by('-created_at')[:3]
    events_with_images = []

    for event in first_events:
        first_image = PostImages.objects.filter(post=event).first()
        events_with_images.append({
            'event': event,
            'image': first_image
        })

    # Contact Us
    if request.method == 'POST':
        contact_form = ContactUsForm(request.POST)
        current_user = request.user
        if contact_form.is_valid():
            if current_user.is_authenticated:
                contact = contact_form.save(commit=False)
                contact.sender = current_user.userprofile
                contact.save()
            else:
                contact = contact_form.save()
            messages.success(request, 'Message sent successfully')
            return redirect('core:home')
        else:
            messages.error(request, 'Something went wrong!')

    else:
        contact_form = ContactUsForm(user=request.user)

    context = {
        'events_with_images': events_with_images,
        'first_blogs': first_blogs,
        'contact_form': contact_form
    }
    return render(request, 'core/index.html', context)


def eventsPage_view(request):
    user = request.user

    if user.is_authenticated:
        published_events = Post.objects.filter(status='Published', post_type='Event')
        user_events = Post.objects.filter(author=user.userprofile, post_type='Event').exclude(status='Published')
        all_events = published_events.union(user_events).order_by('-created_at')
    else:
        all_events = Post.objects.filter(status='Published', post_type='Event').order_by('-created_at')

    paginator = Paginator(all_events, 6)
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    events_with_images = []
    for event in events:
        first_image = PostImages.objects.filter(post=event).first()
        events_with_images.append({
            'event': event,
            'image': first_image
        })
    
    context = {
        'events_with_images': events_with_images,
        'page_obj': events,
    }
    return render(request, 'core/all_events.html', context)


def blogsPage_view(request):
    user = request.user
    if user.is_authenticated and user.userprofile.is_blog_poster:
        categories = Category.objects.annotate(
            post_count=Count('post', filter=Q(post__post_type='Blog'))
        )
    else:
        categories = Category.objects.annotate(
            post_count=Count('post', filter=Q(post__status='Published', post__post_type='Blog'))
        )

    selected_category = request.GET.get('category')
    if selected_category and not Category.objects.filter(slug=selected_category).exists():
        selected_category = None

    published_blogs = Post.objects.filter(status='Published', post_type='Blog')
    if selected_category:
        published_blogs = published_blogs.filter(categories__slug=selected_category)

    user_blogs = Post.objects.none()
    if user.is_authenticated and user.userprofile.is_blog_poster:
        user_blogs = Post.objects.filter(author=user.userprofile, post_type='Blog')
        if selected_category:
            user_blogs = user_blogs.filter(categories__slug=selected_category)

    all_blogs = published_blogs | user_blogs
    all_blogs = all_blogs.order_by('-created_at')

    paginator = Paginator(all_blogs, 6)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        'all_blogs': blogs,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'core/all_blogs.html', context)


def blogDetailPage_view(request, slug):
    blog_detail = get_object_or_404(Post, post_type='Blog', slug=slug)

    if blog_detail.status != 'Published' and request.user != blog_detail.author.user:
        if blog_detail.status == 'Draft':
            messages.error(request, "This blog is not published yet")
        elif blog_detail.status == 'Archived':
            messages.error(request, "This blog is archived")
        return redirect('core:home')
    context = {
        'blog_detail': blog_detail
    }
    return render(request, 'core/blog_detail.html', context)


def eventDetailPage_view(request, slug):
    event_detail = get_object_or_404(Post, post_type='Event', slug=slug)
    if event_detail.status != 'Published' and request.user != event_detail.author.user:
        if event_detail.status == 'Draft':
            messages.error(request, "This event is not published yet")
        elif event_detail.status == 'Archived':
            messages.error(request, "This event is archived")
        return redirect('core:home')
    context = {
        'event_detail': event_detail
    }
    return render(request, 'core/event_detail.html', context)


def validate_image_file(file):
    import magic

    valid_mime_types = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/svg+xml",
        "image/webp",
    ]

    # Validate MIME type
    mime_type = magic.from_buffer(file.read(), mime=True)
    if mime_type not in valid_mime_types:
        raise ValidationError("Unsupported file type.")

    # Reset file pointer to the beginning
    file.seek(0)

    # Validate file size
    max_file_size = 5 * 1024 * 1024 
    if file.size > max_file_size:
        raise ValidationError("File size exceeds the limit of 5MB.")


def compress_image(image, format, quality=10):
    buffer = BytesIO()
    if format == "PNG":
        image.save(buffer, format="PNG", optimize=True)
    else:
        image.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer


@login_required
def upload_image_view(request):
    if request.method == "POST" and request.FILES.get("imageFile"):
        image_file = request.FILES["imageFile"]
        try:
            validate_image_file(image_file)

            with Image.open(image_file) as img:
                format = img.format or "JPEG"
                unique_filename = f"{uuid.uuid4()}.{format.lower()}"
                file_path = f"images/uploads/{unique_filename}"

                if format.upper() in ["GIF", "SVG"]:
                    file_path = default_storage.save(file_path, image_file)
                else:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    compressed_image = compress_image(img, format)
                    file_path = default_storage.save(file_path, compressed_image)

                image_obj = PostImages.objects.create(image=file_path)

                image_url = f'<img class="w-full my-6 rounded-lg shadow-lg" src="{default_storage.url(file_path)}">'
                return JsonResponse(
                    {"success": True, "image_url": image_url, "image_id": image_obj.id}
                )
        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)})
        except UnidentifiedImageError:
            return JsonResponse({"success": False, "error": "Invalid image file."})
        except IOError:
            return JsonResponse({"success": False, "error": "Error processing image."})
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"An error occurred: {str(e)}"}
            )
    else:
        messages.error(request, 'Method Not Allowed!')
        return redirect('core:home')


def cleanup_unused_images():
    unused_images = PostImages.objects.filter(post__isnull=True)
    for image in unused_images:
        default_storage.delete(image.image.path)
        image.delete()


@login_required
def addBlogPost_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if not user_profile.is_blog_poster:
        messages.error(request, "You do not have permission to add blog posts.")
        return redirect("core:home")

    if request.method == "POST":
        add_blog_form = AddPostForm(request.POST)
        if add_blog_form.is_valid():
            post = add_blog_form.save(commit=False)
            post.author = user_profile
            post.post_type = "Blog"
            post.save()
            
            selected_categories = add_blog_form.cleaned_data.get("categories", [])
            post.categories.set(selected_categories)
            post.save()

            # Retrieve the image_ids and handle comma-separated values
            image_ids_str = request.POST.get("image_ids", "")
            image_ids = image_ids_str.split(",")
            image_ids = [int(image_id) for image_id in image_ids if image_id.isdigit()]

            PostImages.objects.filter(id__in=image_ids, post__isnull=True).update(post=post)
            cleanup_unused_images()

            if add_blog_form.cleaned_data['status'] == 'Draft':
                messages.info(request, "New Blog Added But Not Published (Drafted)!")
            elif add_blog_form.cleaned_data['status'] == 'Archived':
                messages.info(request, "New Blog Added But Not Published (Archived)!")
            elif add_blog_form.cleaned_data['status'] == 'Published':
                messages.success(request, "New Blog Added !")
            return redirect("core:blog-detail", post.slug)
    else:
        add_blog_form = AddPostForm()

    context = {
        "add_blog_form": add_blog_form,
    }
    return render(request, "core/new_post.html", context)


@login_required
def addEventPost_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if not user_profile.is_event_poster:
        messages.error(request, "You do not have permission to add event posts.")
        return redirect("core:home")

    if request.method == "POST":
        add_event_form = AddPostForm(request.POST)
        if add_event_form.is_valid():
            post = add_event_form.save(commit=False)
            post.author = user_profile
            post.post_type = "Event"
            post.save()
            
            selected_categories = add_event_form.cleaned_data.get("categories", [])
            post.categories.set(selected_categories)
            post.save()

            # Retrieve the image_ids and handle comma-separated values
            image_ids_str = request.POST.get("image_ids", "")
            image_ids = image_ids_str.split(",")
            image_ids = [int(image_id) for image_id in image_ids if image_id.isdigit()]

            PostImages.objects.filter(id__in=image_ids, post__isnull=True).update(post=post)
            cleanup_unused_images()

            if add_event_form.cleaned_data['status'] == 'Draft':
                messages.info(request, "New Event Added But Not Published (Drafted)!")
            elif add_event_form.cleaned_data['status'] == 'Archived':
                messages.info(request, "New Event Added But Not Published (Archived)!")
            elif add_event_form.cleaned_data['status'] == 'Published':
                messages.success(request, "New Event Added !")
            return redirect("core:event-detail", post.slug)
    else:
        add_event_form = AddPostForm()

    context = {
        "add_event_form": add_event_form,
    }
    return render(request, "core/new_post.html", context)


@login_required
def deletePost_view(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)

        if request.user == post.author.user:
            post.delete()
            messages.success(request, "Post deleted successfully")
        else:
            messages.error(request, "You do not have permission to delete this post")
    else:
        messages.error(request, "Method Not Allowed")

    return redirect('core:home')       


@login_required
def editPost_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author.user:
        if request.method == 'POST':
                updated_post_form = AddPostForm(request.POST, instance=post)
                if updated_post_form.is_valid():
                    updated_post = updated_post_form.save()
                    
                    # Retrieve the image_ids and handle comma-separated values
                    image_ids_str = request.POST.get("image_ids", "")
                    image_ids = image_ids_str.split(",")
                    image_ids = [int(image_id) for image_id in image_ids if image_id.isdigit()]

                    PostImages.objects.filter(id__in=image_ids, post__isnull=True).update(post=post)
                    cleanup_unused_images()

                    if updated_post.post_type == 'Blog' and updated_post.status == 'Published': 
                        messages.success(request, "Blog Post Updated Successfully")
                        return redirect('core:blog-detail', slug=post.slug)       
                    elif updated_post.post_type == 'Blog' and updated_post.status == 'Draft': 
                        messages.info(request, "Blog Post Updated But Not Published (Drafted)!")
                        return redirect('core:blog-detail', slug=post.slug)       
                    elif updated_post.post_type == 'Blog' and updated_post.status == 'Archived': 
                        messages.info(request, "Blog Post Updated But Not Published (Archived)!")
                        return redirect('core:blog-detail', slug=post.slug)       
                    elif updated_post.post_type == 'Event' and updated_post.status == 'Published': 
                        messages.success(request, "Event Post Updated Successfully")
                        return redirect('core:event-detail', slug=post.slug)       
                    elif updated_post.post_type == 'Event' and updated_post.status == 'Draft': 
                        messages.info(request, "Event Post Updated But Not Published (Drafted)!")
                        return redirect('core:event-detail', slug=post.slug)       
                    elif updated_post.post_type == 'Event' and updated_post.status == 'Archived': 
                        messages.info(request, "Event Post Updated But Not Published (Archived)!")
                        return redirect('core:event-detail', slug=post.slug)       
        
        updated_post_form = AddPostForm(instance=post)
        context = {
            'updated_post_form': updated_post_form,
            'post_slug': post.slug
        }
        return render(request, 'core/edit_post.html', context)

    else:
        messages.error(request, "You do not have permission to edit this post")
        return redirect('core:home')