from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    """This extends a user through a 1-1 field, adding a faculty and role"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """The One to One reference to the user"""
    faculty = models.CharField(max_length=len("Florence Nightingale Faculty of Nursing, Midwifery & Paliative Care"), blank=True)
    """The faculty the User is in"""
    role = models.CharField(max_length=20, blank=True)
    """The role of the User"""


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """This creates a profile when a user is created"""
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Question(models.Model):
    """This is a question on the q&a site"""
    question_title = models.CharField(max_length=200)
    """The title of the question"""
    question_body = models.TextField()
    """The body of the question"""
    pub_date = models.DateTimeField(default=timezone.now)
    """The publication date of the question, default is the current date & time"""
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, default=None, null=True)
    """The author of the Question"""

    def __str__(self):
        """
        Gets the string representation of the Question
        :return: the title of the question
        """
        return self.question_title


class Answer(models.Model):
    """This is an answer to a question"""
    answer_text = models.TextField()
    """The text of the answer"""
    pub_date = models.DateTimeField(default=timezone.now)
    """The publication date of the answer, default is the current date & time"""
    question_answered = models.ForeignKey(Question, on_delete=models.CASCADE)
    """The question this answer has answered"""
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, default=None, null=True)
    """The auther of the answer"""

    def __str__(self):
        """
        Gets the string representation of the Answer
        :return: Answer to <question_answered.question_title> published <pub_date>
        """
        return "Answer to " + self.question_answered.question_title + " published " + str(self.pub_date)
