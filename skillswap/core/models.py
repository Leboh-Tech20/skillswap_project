from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone


# ------------------------------
# ✅ Custom User Model
# ------------------------------
class User(AbstractUser):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    video_intro_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username


# ------------------------------
# ✅ Skill and Skill Listing
# ------------------------------
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SkillListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    description = models.TextField()
    is_offer = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill.name} by {self.user.username} ({'Offering' if self.is_offer else 'Looking'})"


# ------------------------------
# ✅ Exchange
# ------------------------------
class Exchange(models.Model):
    requester = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    responder = models.ForeignKey(User, related_name='responses', on_delete=models.CASCADE)
    requested_skill = models.ForeignKey(SkillListing, related_name='requested', on_delete=models.CASCADE)
    offered_skill = models.ForeignKey(SkillListing, related_name='offered', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    start_date = models.DateTimeField()
    agreement_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requester.username} ↔ {self.responder.username} [{self.status}]"


# ------------------------------
# ✅ Message
# ------------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"


# ------------------------------
# ✅ Agreement
# ------------------------------
class Agreement(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_agreements')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_agreements')
    requested_skill = models.ForeignKey(SkillListing, on_delete=models.CASCADE)
    start_date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(default='pending', max_length=20)

    def __str__(self):
        return f"{self.requester.username} ↔ {self.responder.username} ({self.status})"


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)

    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Make sure this line exists
    
    class Meta:
        unique_together = ('reviewer', 'reviewee', 'exchange')
