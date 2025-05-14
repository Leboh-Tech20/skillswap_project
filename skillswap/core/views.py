from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import *
from .forms import ProfileForm, AgreementForm
from django.db.models import Q
from .models import User, Message
from .models import SkillListing, Agreement
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Exchange, User
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
  


def welcome_view(request):
    return render(request, 'core/welcome.html')



def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "🎉 Account created successfully! You can now log in.")
        return redirect('login')
    return render(request, 'core/register.html', {'form': form})



def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('welcome')

@login_required
def home(request):
    listings = SkillListing.objects.all()
    return render(request, 'core/home.html', {'listings': listings})

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'profile_user': user,
        'username': username
    }
    return render(request, 'core/profile.html', context)
  

from django.contrib import messages

@login_required
def post_skill(request):
    if request.method == 'POST':
        skill_id = request.POST.get('skill')
        description = request.POST.get('description')
        is_offer = request.POST.get('is_offer') == 'on'
        is_need = request.POST.get('is_need') == 'on'

        if not (is_offer or is_need):
            return render(request, 'core/post_skill.html', {
                'skills': Skill.objects.all(),
                'error': 'Please select if you are offering or looking for the skill.'
            })

        if skill_id == 'other':
            other_skill_name = request.POST.get('other_skill')
            if not other_skill_name:
                return render(request, 'core/post_skill.html', {
                    'skills': Skill.objects.all(),
                    'error': 'Please enter the custom skill name.'
                })
            skill, _ = Skill.objects.get_or_create(name=other_skill_name.strip())
        else:
            skill = Skill.objects.get(id=skill_id)

        if is_offer:
            SkillListing.objects.create(user=request.user, skill=skill, description=description, is_offer=True)
        if is_need:
            SkillListing.objects.create(user=request.user, skill=skill, description=description, is_offer=False)

        messages.success(request, '✅ Skill posted successfully!')
        return redirect('home')

    return render(request, 'core/post_skill.html', {'skills': Skill.objects.all()})


from django.contrib import messages as django_messages  # optional alias for clarity

@login_required
def message_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('messages', user_id=other_user.id)

    return render(request, 'core/message.html', {
        'chat_messages': chat_messages,  # ✅ renamed to avoid conflict
        'other_user': other_user
    })



@login_required
def match_list(request):
    user_needs = SkillListing.objects.filter(user=request.user, is_offer=False)
    user_offers = SkillListing.objects.filter(user=request.user, is_offer=True)

    matches = []

    # You are looking for X → find who offers X
    for need in user_needs:
        potential = SkillListing.objects.filter(skill=need.skill, is_offer=True).exclude(user=request.user)
        matches.extend(potential)

    # You are offering Y → find who needs Y
    for offer in user_offers:
        potential = SkillListing.objects.filter(skill=offer.skill, is_offer=False).exclude(user=request.user)
        matches.extend(potential)

    # Remove duplicates
    matches = list({m.id: m for m in matches}.values())

    return render(request, 'core/match_list.html', {'matches': matches})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Agreement, SkillListing

@login_required
def dashboard_view(request):
    agreements = Agreement.objects.filter(requester=request.user) | Agreement.objects.filter(responder=request.user)
    recent_skills = SkillListing.objects.filter(user=request.user).order_by('-created_at')[:10]

    context = {
        'agreements': agreements.distinct(),
        'recent_skills': recent_skills,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile', username=request.user.username)  # ✅ correct
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})




@login_required
def inbox_view(request):
    user = request.user

    # Get all users you've exchanged messages with
    conversations = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values('sender', 'receiver')

    # Extract unique user IDs you've chatted with
    user_ids = set()
    for conv in conversations:
        user_ids.add(conv['sender'])
        user_ids.add(conv['receiver'])
    user_ids.discard(user.id)  # Remove yourself from the list

    chat_users = User.objects.filter(id__in=user_ids)

    return render(request, 'core/inbox.html', {'chat_users': chat_users})

@login_required
def edit_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            msg.content = new_content
            msg.edited = True
            msg.save()
        return redirect('messages', user_id=msg.receiver.id if msg.receiver != request.user else msg.sender.id)

    return render(request, 'core/edit_message.html', {'message': msg})


@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)
    user_id = msg.receiver.id if msg.receiver != request.user else msg.sender.id
    msg.delete()
    return redirect('messages', user_id=user_id)




@login_required
def create_agreement(request):
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.requester = request.user
            agreement.save()
            messages.success(request, "✅ Agreement created successfully.")
            return redirect('dashboard')
    else:
        form = AgreementForm()

    return render(request, 'core/create_agreement.html', {'form': form})


from django.contrib import messages

@login_required
def leave_review(request):
    reviewee_id = request.GET.get('reviewee_id')
    exchange_id = request.GET.get('exchange_id')

    if not reviewee_id or not reviewee_id.isdigit():
        messages.error(request, "Invalid user specified for review")
        return redirect('home')

    reviewee = get_object_or_404(User, id=int(reviewee_id))
    exchange = None

    if exchange_id and exchange_id.isdigit():
        try:
            exchange = Exchange.objects.get(id=int(exchange_id))
            if request.user not in [exchange.requester, exchange.responder]:
                messages.error(request, "You can only review exchanges you participated in")
                return redirect('home')
        except Exchange.DoesNotExist:
            exchange = None

    existing_review = Review.objects.filter(
        reviewer=request.user,
        reviewee=reviewee,
        exchange=exchange
    ).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if existing_review:
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, "✅ Review updated successfully!")
            else:
                Review.objects.create(
                    reviewer=request.user,
                    reviewee=reviewee,
                    exchange=exchange,
                    rating=form.cleaned_data['rating'],
                    comment=form.cleaned_data['comment']
                )
                messages.success(request, "✅ Review submitted successfully!")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm(initial={
            'rating': existing_review.rating if existing_review else '',
            'comment': existing_review.comment if existing_review else ''
        })

    return render(request, 'core/review.html', {
        'form': form,
        'reviewee': reviewee,
        'exchange': exchange
    })
from django.shortcuts import get_object_or_404, redirect
from .models import SkillListing, Skill
from django.contrib import messages
from .forms import SkillListingForm
@login_required
def edit_skill(request, skill_id):
    skill_listing = get_object_or_404(SkillListing, id=skill_id, user=request.user)

    if request.method == 'POST':
        form = SkillListingForm(request.POST, instance=skill_listing)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Skill updated successfully.")
            return redirect('dashboard')
    else:
        form = SkillListingForm(instance=skill_listing)

    return render(request, 'core/edit_skill.html', {'form': form})

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(SkillListing, id=skill_id, user=request.user)
    skill.delete()
    messages.success(request, "✅ Skill deleted successfully.")
    return redirect('dashboard')