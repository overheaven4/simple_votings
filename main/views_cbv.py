from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Voting, VotingOption, Vote
from django.shortcuts import get_object_or_404


class VotingListView(ListView):
    """
    Альтернативная реализация списка голосований через Class-Based View.
    Заменяет функцию votes_page.
    """
    model = Voting
    template_name = 'votes.html'
    context_object_name = 'items'
    ordering = ['-created_at']
    paginate_by = 10  # Добавляем пагинацию "из коробки"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Список всех голосований'
        context['total_count'] = Voting.objects.count()
        return context


class VotingDetailView(LoginRequiredMixin, DetailView):
    """
    Альтернативная реализация просмотра голосования.
    """
    model = Voting
    template_name = 'voting_detail_cbv.html'
    context_object_name = 'voting'
    pk_url_kwarg = 'voting_id'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = self.get_object()

        # Получаем все варианты для этого голосования
        options_list = VotingOption.objects.filter(voting=voting)
        context['options'] = options_list

        # Проверяем, голосовал ли текущий юзер
        user_vote = Vote.objects.filter(
            user=self.request.user,
            option__voting=voting
        ).first()

        context['has_voted'] = bool(user_vote)
        if user_vote:
            context['user_choice'] = user_vote.option

        return context