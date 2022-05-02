from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import VoteForm, MovieForm
from .models import Movie, Vote


def index(request):
    movies = '<br>\n'.join([str(i) for i in Movie.objects.all()])
    return HttpResponse(f"Films <br> {movies}")


class MovieList(ListView):
    model = Movie
    form_class = MovieForm
    # paginate_by = 10

    def get(self, request):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, **kwargs)

    def post(self, request, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            self.object = self.form.save()
        return self.get(request, **kwargs)

def get_context_data(self, **kwargs):
    ctx = super(MovieList, self).get_context_data(**kwargs)
    page = ctx["page_obj"]
    paginator = ctx["paginator"]
    ctx["page_is_first"] = page.number == 1
    ctx["page_is_last"] = page.number == paginator.num_pages
    if self.request.user.is_authenticated:
        ctx["movie_form"] = self.form
    return ctx

class MovieDetail(DetailView):
    queryset = Movie.objects.all_about_movie()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_blank(movie=self.object)
        if vote.id:
            vote_from_url = reverse("update-vote", kwargs={"movie_id": vote.movie.id, "pk": vote.id})
        else:
            vote_from_url = reverse(
                "create-vote", kwargs={"movie_id": self.object.id})
        vote_form = VoteForm(instance=vote)
        ctx["vote_form"] = vote_form
        ctx["vote_form_url"] = vote_from_url
        ctx["score"] = int(vote.value)
    return ctx

class TopMovies(ListView):
    template_name = "core/top10_movies.html"

    def get_queryset(self):
        limit = 10
        qs = Movie.objects.top_movies(limit=limit)
        return qs

class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context["object"].id
        movie_detail_url = reverse("movie-detail", kwargs={"pk": movie_id})
        return redirect(to=movie_detail_url)

class CreateVote(CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def render_to_response(self, context, **response_kwargs):
        movie_id = ctx["odject"].id
        movie_detail_url = reverse('MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.object.movie.id
        movie_detail_url = reverse('MovieDetail', kwargs={'pk': movie_id})
        return movie_detail_url

