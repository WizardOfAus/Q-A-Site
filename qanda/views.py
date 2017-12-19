from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.utils import timezone

# Create your views here.
from django.views import generic
from django.views.generic.edit import FormMixin

from qanda.forms import SignUpForm, QuestionForm, AnswerForm
from qanda.forms import SignUpForm, AnswerForm
from .models import Question, Profile, Answer


class IndexView(generic.ListView):
    template_name = "qanda/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(FormMixin, generic.DetailView):
    model = Question
    template_name = "qanda/detail.html"
    form_class = AnswerForm

    def get_success_url(self):
        return reverse('qanda:detail', kwargs={'pk': self.get_object().pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form_class()()
        return context

    def form_valid(self, form):
        question_answered = self.get_object()
        author = self.request.user.profile
        text = form.cleaned_data['answer_text']
        a = Answer(author=author, question_answered=question_answered, answer_text=text)
        a.save()
        return super().form_valid(form)


class ProfileView(generic.DetailView):
    model = Profile
    template_name = "qanda/profile.html"


class PostQuestionView(generic.FormView):
    template_name = 'qanda/post.html'
    form_class = QuestionForm
    success_url = '/'

    def get_success_url(self):
        """The redirect if the creation was successful"""
        return reverse('qanda:detail', args=(self.object.id,))

    def post(self, request, *args, **kwargs):
        """Handles the post method, returns 403 if not logged in"""
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid
        :param form: the form
        :return: The HttpResponse
        """
        clean_data = form.cleaned_data
        text = clean_data['question_body']
        title = clean_data['question_title']
        user = self.request.user.profile
        q = Question(question_title=title, question_body=text, author=user)
        q.save()
        self.object = q
        return super().form_valid(form)


def signup(request):
    """The signup view"""
    if request.method == 'POST':
        # if the method is post
        form = SignUpForm(request.POST)
        if form.is_valid():
            # if the form is valid, make a user
            user = form.save()
            user.refresh_from_db()
            user.profile.faculty = form.cleaned_data.get('faculty')
            user.profile.role = form.cleaned_data.get('role')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    # reshow the form if not valid, or not post
    return render(request, 'qanda/signup.html', {'form': form})