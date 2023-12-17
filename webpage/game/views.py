from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render 
from game.models import Game, Player, User
from game.forms import GameCreationForm
from game.apps import GameConfig as app
from game.MatchMaker import MatchMakerWarning
from tournament.models import Tournament
import json

# Create your views here.
def game_home(request):
    print(request)
    return render(request, 'game/game_creation_form.html')
    #return HttpResponse("Welcome to the game home page.")

def _build_error_payload(msg):
    return {
        'status': 'failure',
        'reason': msg
    }

@login_required
def game_join(request):
    '''
        The game request process in the frontend should result in
        a json struct sent as body to an endpoint landing on 
        the game_join() view.
    '''
    if request.method != 'POST':
        return JsonResponse(_build_error_payload('A request to send a game requires a POST request with a properly fromated body.'), status=400)
        #return HttpResponse('A request to send a game requires a POST request with a properly fromated body.', status=400)
    
    print('RECEIVED POST : ', request.POST)
    print('RECEIVED POST BODY : ', request.body)
    jsonform = json.loads(request.body)
    print('jsonform : ', jsonform)
    if not jsonform:
        return JsonResponse(_build_error_payload('Trying to create a game, but either no game creation form was sent or is malformed.'), status=400)
        #return HttpResponse('Trying to create a game, but either no game creation form was sent or is malformed.', status=400)


    form = GameCreationForm(jsonform)
    print('Form : \n', form)
    print('Form Errors : \n', form.errors)
    if not form.is_valid():
        return JsonResponse(_build_error_payload('Trying to create a game, but either no game creation form was sent or is missing fields.'), status=400)
        #return HttpResponse('Trying to create a game, but either no game creation form was sent or is missing fields.', status=400)

    print('Created form gameMode: ', form.cleaned_data['gameMode'])
    print('Created form gameType: ', form.cleaned_data['gameType'])
    #game_id = -1# default



    mm = app.get_match_maker()
    print(mm)

    try:
        lobby_game = mm.join_lobby(request.user, form.cleaned_data)
    except MatchMakerWarning as w:
        return JsonResponse(_build_error_payload(str(w)), status=400)

    if not lobby_game:
        return JsonResponse(_build_error_payload('Joining game lobby failed.'), status=400)
        #return HttpResponse('Joining game lobby failed.', status=400)

    payload = {
        'status': 'success',
        'sockID': lobby_game.sockID,
        'gameMode': form.cleaned_data['gameMode'],
        'gameType': form.cleaned_data['gameType'],
        'withAI': form.cleaned_data['withAI'] if 'withAI' in form.cleaned_data else False
    }

    ### TODO: CALL GameManager to create game according to request.
    if (form.cleaned_data['gameMode'] == 'Tournament'):
        payload['tourSockID'] = 'Tour_' + payload['sockID']
    else:
        pass

    return JsonResponse(payload)
    
''' Testing game instances creation '''
def _build_test_game(user: User) -> Game:
    return (Game.objects.create(
            host=user
            #group_id=f'game_{id}',
        )
    )
