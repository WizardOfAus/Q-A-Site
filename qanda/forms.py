from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

from django.core.exceptions import ValidationError

from qanda.models import Question, Answer


class SignUpForm(UserCreationForm):
    """This is the form used to create a new user"""
    first_name = forms.CharField(max_length=30, label="First Name")
    """The first name of the user"""
    last_name = forms.CharField(max_length=30, label="Last Name")
    """The last name of the user"""
    email = forms.EmailField(max_length=254, label="Email Address", help_text='Required. Inform a valid email address.')
    """The email address of the user (must end in kcl.ac.uk)"""
    role = forms.ChoiceField(choices=[(x,x) for x in ("Undergraduate", "Postgraduate", "Staff", "Other")], label="Role")
    """The role of the user"""
    faculty = forms.ChoiceField(
        choices=[(x, x) for x in ("Faculty of Arts & Humanities",
         "King's Business School",
         "Dental Institute",
         "Institute of Psychiatry, Psychology & Neuroscience",
         "Faculty of Life Sciences & Medicine",
         "The Dickson Poon School of Law",
         "Faculty of Natural & Mathematical Sciences",
         "Florence Nightingale Faculty of Nursing, Midwifery & Paliative Care",
         "Faculty of Social Science & Public Policy",
         "Other")],
        label="Faculty"
    )
    """The faculty of the user"""

    def clean_email(self):
        """
        Asserts the email is in the correct format
        :return: the email address
        :raises ValidationError: if the email address doesn't end in kcl.ac.uk
        """
        email = self.cleaned_data['email']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@kcl.ac.uk)", email):
            raise ValidationError("Please enter a KCL email address")
        return email

    class Meta:
        """The metadata for the Form"""
        model = User
        """The model the form creates"""
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'faculty', 'password1', 'password2')
        """The fields in the form"""


class QuestionForm(forms.ModelForm):
    """This is the form used to post a question"""
    question_title = forms.CharField(max_length=200)
    """The title of the question"""
    question_body = forms.CharField(widget=forms.Textarea)
    """The body of the question"""

    class Meta:
        """The metadata for the form"""
        model = Question
        """The model the form creates"""
        fields = ('question_title', 'question_body')
        """The fields in the form"""


class AnswerForm(forms.ModelForm):
    """This is the form used to post an answer to a question"""
    answer_text = forms.CharField(widget=forms.Textarea, label=None)
    """The text of the answer"""

    class Meta:
        """The metadata for the form"""
        model = Answer
        """The model the form creates"""
        fields = ('answer_text',)
        """The fields in the form"""
