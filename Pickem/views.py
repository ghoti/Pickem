# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form
from django.template.context import RequestContext
from models import Team,User,Game,Pick,Profile
from django.contrib.auth import decorators
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.contrib import messages

from scorewatch import scores

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def live(request):
    return render_to_response('live.html', {'games':scores()}, context_instance=RequestContext(request))

def allteams(request):
    t = Team.objects.all()
    return render_to_response('teams.html', {'all':t}, context_instance=RequestContext(request))

def teamcity(request, team):
    try:
        t = Team.objects.get(city=team)
    except Team.DoesNotExist:
        return render_to_response('team.html', {'errpr':True}, context_instance=RequestContext(request))
    return render_to_response('team.html', {'team':t0}, context_instance=RequestContext(request))

def teamname(request, team):
    team = team.lower().capitalize()
    try:
        t = Team.objects.get(name=team)
    except Team.DoesNotExist:
        return render_to_response('team.html', {'error':True}, context_instance=RequestContext(request))
    return render_to_response('team.html', {'team':t}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))

def profile(request, profile):
    try:
        u = User.objects.get(username=profile)
    except User.DoesNotExist:
        return render_to_response('profile.html', context_instance=RequestContext(request))
    #get_or_create would be AWESOME right about here - so get on that
    try:
        p = Profile.objects.get(user=u.id)
    except Profile.DoesNotExist:
        p = Profile(user=u.id, w=0,l=0)
        p.save()
        p = Profile.objects.get(user=u.id)
    return render_to_response('profile.html', {'u':u.username, 'p':p}, context_instance=RequestContext(request))

@decorators.login_required
def create_pick(request):
    pass

@decorators.permission_required(perm='Pick.add_game')
def add_game(request):
    t = Team.objects.all()
    if request.method == 'POST':
        #the user is dumb and will not put a number in
        if not request.POST['week']:
            messages.add_message(request, messages.INFO, 'No week specified')
            return HttpResponseRedirect('/add_game')
        #or will put something that isn't a number...
        try:
            week = int(request.POST['week'])
        except ValueError:
            form = Form()
            messages.add_message(request, messages.INFO, 'Invalid Week Specified')
            return HttpResponseRedirect('/add_game')

        team1 = request.POST['team1']
        team2 = request.POST['team2']

        #we already added this game, abandon ship!
        if Game.objects.filter(week=week, home=team2, away=team1).exists():
            messages.add_message(request, messages.INFO, 'That game already exists for that week')
        #one of the teams is already playing this week, abort!
        elif Game.objects.filter(week=week, home=team2).exists() or Game.objects.filter(week=week, away=team1).exists():
            messages.add_message(request, messages.INFO, 'That team is already playing that week')
        #a team can't play itself
        elif team1 == team2:
            messages.add_message(request, messages.INFO, 'A team cannot play itself, now can it?')
        #if everything is gravy, then add it to the db and return back
        else:
            g = Game(week=week, home=team2, away=team1)
            g.save()
            messages.add_message(request, messages.INFO, 'Game Added')
        return HttpResponseRedirect('/add_game')
    else:
        form = Form()
    return render_to_response('add_game.html', {'form':form, 'teams':t}, context_instance=RequestContext(request))

def gamelist(request):
    games = Game.objects.all()
    return render_to_response('games.html', {'games':games}, context_instance=RequestContext(request))

def game(request, gameno):
    try:
        g = Game.objects.get(id=gameno)
    except Game.DoesNotExist:
        g = None
    if g:
        away = Team.objects.get(call=g.away).name
        home = Team.objects.get(call=g.home).name
        return render_to_response('game.html', {'game':g, 'away':away, 'home':home}, context_instance=RequestContext(request))
    else:
        return render_to_response('game.html', {'game':None}, context_instance=RequestContext(request))
