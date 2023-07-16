from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView

from viewer.forms import MovieForm, SignUpForm
from viewer.models import Movie


def hello(request, name):
    query = request.GET.get('query', '')
    #  return HttpResponse(f'<h1>Hello, world {name}!</h1><p>This is the query: {query}</p>')
    return render(request, template_name='hello.html', context={'adjectives': ['Django', 'Python', query, name]})


@login_required
def simple_hello(request):
    return HttpResponse('Hello, world!')


def movies_list(request):
    return render(
        request, template_name="movies.html",
        context={"movies": Movie.objects.all()}
    )


# View class
# class MoviesView(View):
#     def get(self, request):
#         return render(request, template_name="movies.html", context={"movies": Movie.objects.all()})

# TemplateView:

# class MoviesView(TemplateView):
#     template_name = 'movies.html'
#     extra_context = {"movies": Movie.objects.all()}


class AdultRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        date_of_birth = self.request.user.date_of_birth
        return date_of_birth is not None and (
                datetime.datetime.now().date() - date_of_birth
        ) > datetime.timedelta(days=365 * 18)


# ListView:

class MoviesView(AdultRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'movies.html'
    model = Movie


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'create_movie.html'
    form_class = MovieForm
    success_url = "/"
    permission_required = 'viewer.add_movie'

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     Movie.objects.create(
    #         title=form.cleaned_data['title_form'],
    #         genre=form.cleaned_data['genre_form'],
    #         rating=form.cleaned_data['rating_form'],
    #         released=form.cleaned_data['released_form'],
    #         description=form.cleaned_data['description_form'],
    #     )
    #     return result

    # Definim ce se intampla cand se trimit datele si sunt valide

    # Definim de fiecare data cand formul este invalid:
    def form_invalid(self, form):
        print("Formul este invalid")
        return super().form_valid(form)


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'registration/change_pass.html'
    success_url = reverse_lazy('index')


class SignUpView(CreateView):
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('index')
    form_class = SignUpForm
