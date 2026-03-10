from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from main.models import Voting, VotingOption, Vote
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


class VotingListAPI(View):
    """API для получения списка всех голосований"""

    def get(self, request):
        votings = Voting.objects.all().order_by('-created_at')
        data = []
        for voting in votings:
            data.append({
                'id': voting.id,
                'title': voting.title,
                'creator': voting.creator.username,
                'created_at': voting.created_at.isoformat(),
                'options_count': VotingOption.objects.filter(voting=voting).count()
            })
        return JsonResponse({'status': 'success', 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class VoteCreateAPI(View):
    """API для отправки голоса через AJAX/fetch запросы"""

    def post(self, request, option_id):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

        try:
            option = get_object_or_404(VotingOption, id=option_id)

            # Защита от двойного голосования
            if Vote.objects.filter(user=request.user, option__voting=option.voting).exists():
                return JsonResponse({'status': 'error', 'message': 'Already voted'}, status=400)

            Vote.objects.create(user=request.user, option=option)
            return JsonResponse({'status': 'success', 'message': 'Vote successfully recorded'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)