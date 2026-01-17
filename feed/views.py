from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Post, Comment
from groq import Groq
import json

from django.http import JsonResponse # <--- Import this at the top

# ... existing imports ...

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    # Return JSON instead of redirecting
    return JsonResponse({
        'total_likes': post.likes.count(),
        'liked': liked
    })
# --- FEED AI LOGIC ---
@login_required
def home(request):
    if request.method == "POST":
        # --- 1. HANDLE NEW POST CREATION ---
        if 'post_content' in request.POST:
            content = request.POST.get('post_content')
            image = request.FILES.get('post_image') # Get the image
            
            post = Post.objects.create(author=request.user, content=content, image=image)
            
            # AI Logic
            try:
                if not settings.GROQ_API_KEY: raise ValueError("No Key")
                client = Groq(api_key=settings.GROQ_API_KEY)
                prompt = (f"You are a nutritionist. User posted: '{content}'. Goal: {request.user.profile.get_goal_display()}. Analyze briefly: 1.Good 2.Bad 3.Tip")
                
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                ai_response = chat.choices[0].message.content
            except Exception as e:
                print(f"AI Error: {e}")
                ai_response = "Great post! Keep tracking."

            Comment.objects.create(post=post, author_name="CalorieMedia AI", content=ai_response, is_ai=True)
            return redirect('home')

        # --- 2. HANDLE USER COMMENTS ---
        elif 'comment_content' in request.POST:
            post_id = request.POST.get('post_id')
            content = request.POST.get('comment_content')
            post = Post.objects.get(id=post_id)
            
            Comment.objects.create(
                post=post,
                author_name=request.user.username,
                content=content,
                is_ai=False
            )
            return redirect('home')

    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'feed/home.html', {'posts': posts})
@login_required
def repost_post(request, pk):
    original_post = get_object_or_404(Post, pk=pk)
    
    # Create a new post referencing the old one
    new_content = f"🔄 Repost from @{original_post.author.username}:\n\n{original_post.content}"
    
    Post.objects.create(
        author=request.user,
        content=new_content,
        image=original_post.image # Keeps the original image
    )
    
    messages.success(request, "Post reposted successfully!")
    return redirect('home')
# --- CHATBOT API LOGIC ---
@login_required
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            chat = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a fitness assistant. Keep answers under 2 sentences."},
                    {"role": "user", "content": user_message}
                ],
                # UPDATED MODEL HERE 
                model="llama-3.3-70b-versatile",
            )
            bot_reply = chat.choices[0].message.content
        except Exception as e:
            print(f"CHAT ERROR: {e}")
            bot_reply = "I am having trouble connecting right now. Please try again later."
            
        return JsonResponse({'reply': bot_reply})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('home')

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('home')
    if request.method == 'POST':
        post.content = request.POST.get('content')
        post.save()
        messages.success(request, 'Post updated.')
        return redirect('home')
    return render(request, 'feed/post_form.html', {'post': post})