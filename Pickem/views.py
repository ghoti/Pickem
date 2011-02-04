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
from datetime import datetime, timedelta

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
            return HttpResponseRedirect('/user/%s' % request.POST['username'])
    else:
        form = UserCreationForm()
    return render_to_response('register.html', {'form':form}, context_instance=RequestContext(request))

def profile(request, profile):
    try:
        u = User.objects.get(username=profile)
    except User.DoesNotExist:
        #return render_to_response('profile.html', context_instance=RequestContext(request))
        messages.add_message(request, messages.INFO, 'User does not exists')
    #get_or_create would be AWESOME right about here - so get on that
    try:
        p = Profile.objects.get(user=u.id)
    except Profile.DoesNotExist:
        p = Profile(user=u.id, w=0,l=0)
        p.save()
        p = Profile.objects.get(user=u.id)
    return render_to_response('profile.html', {'u':u.username, 'p':p}, context_instance=RequestContext(request))

@decorators.permission_required(perm='User.is_staff')
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
        elif Game.objects.filter(week=week, away=team2).exists() or Game.objects.filter(week=week, home=team1).exists():
            messages.add_message(request, messages.INFO, 'That team is already playing that week')
        #a team can't play itself
        elif team1 == team2:
            messages.add_message(request, messages.INFO, 'A team cannot play itself, now can it?')
        #if everything is gravy, then add it to the db and return back
        else:
            g = Game(week=week, home=team2, away=team1, status='Pending', deadline=request.POST['timestamp'])
            g.save()
            messages.add_message(request, messages.INFO, 'Game Added')
        return HttpResponseRedirect('/add_game')
    else:
        form = Form()
    return render_to_response('add_game.html', {'form':form, 'teams':t}, context_instance=RequestContext(request))

def gamelist(request):
    games = Game.objects.all().order_by('week')
    return render_to_response('games.html', {'games':games}, context_instance=RequestContext(request))

def game(request, gameno):
    try:
        g = Game.objects.get(id=gameno)
    except Game.DoesNotExist:
        g = None
    if g:
        away = Team.objects.get(call=g.away)
        home = Team.objects.get(call=g.home)

        p = Pick.objects.filter(game=gameno)
        homepicks = []
        awaypicks = []
        if p.exists():
            for i in p:
                if i.pick == away.id:
                    awaypicks.append(User.objects.get(id=i.user).username)
                else:
                    homepicks.append(User.objects.get(id=i.user).username)

        return render_to_response('game.html', {'game':g, 'away':away.name, 'home':home.name, 'hpicks':homepicks,
                                                'apicks':awaypicks}, context_instance=RequestContext(request))

    else:
        return render_to_response('game.html', {'game':None}, context_instance=RequestContext(request))

@decorators.permission_required('User.is_staff')
def make_winner(request, gameno):
    try:
        g = Game.objects.get(id=gameno)
    except Game.DoesNotExist:
        messages.add_message(request, messages.INFO, 'That game does not exists')
        return HttpResponseRedirect('/')

    if Game.objects.get(id=gameno).status == 'FINAL':
        messages.add_message(request, messages.INFO, 'That game has already been decided')
        return HttpResponseRedirect('/game/%s' % gameno)

    away = Team.objects.get(call=g.away)
    home = Team.objects.get(call=g.home)

    if request.method == 'POST':
        if not request.POST['winner'] or not request.POST['homescore'] or not request.POST['awayscore']:
            print request.POST['winner'], request.POST['homescore'], request.POST['awayscore']
            messages.add_message(request, messages.INFO, 'There was missing information in deciding the game')
            return HttpResponseRedirect('/game/%s' % gameno)
        try:
            g.homescore = int(request.POST['homescore'])
            g.awayscore = int(request.POST['awayscore'])
        except ValueError:
            messages.add_message(request, messages.INFO, 'Scores are usually some number, not sure what that was')
            return HttpResponseRedirect('/game/%s' % gameno)

        g.status = 'FINAL'
        g.winner = request.POST['winner']
        g.save()

        if int(request.POST['winner']) == away.id:
            away.w += 1
            home.l += 1
        else:
            away.l += 1
            home.l += 1

        away.save()
        home.save()

        p = Pick.objects.filter(game=gameno)
        for i in p:
            print i.user
            u = Profile.objects.get(id=User.objects.get(id=i.user).id)
            if i.pick == int(request.POST['winner']):
                u.w += 1
            else:
                u.l += 1
            u.save()

        messages.add_message(request, messages.INFO, 'Game has been processed')
        return HttpResponseRedirect('/')
    else:
        form = Form()
    return render_to_response('make_winner.html', {'away':away, 'home':home, 'gameid':gameno},
                              context_instance=RequestContext(request))

@decorators.login_required
def create_pick(request, gameno):
    try:
        g = Game.objects.get(id=gameno)
    except Game.DoesNotExist:
        g = None

    if Pick.objects.filter(user=request.session.get('_auth_user_id'), game=gameno).exists():
        messages.add_message(request, messages.INFO, 'You already have a pick for this game')
        return HttpResponseRedirect('/mypicks')

    if datetime.now() - Game.objects.get(id=gameno).deadline > timedelta(seconds=0):
        messages.add_message(request, messages.INFO, 'Sorry, the deadline has passed to pick for that game')
        return HttpResponseRedirect('/mypicks')

    if g:
        away = Team.objects.get(call=g.away)
        home = Team.objects.get(call=g.home)
        if request.method == 'POST':
            if not request.POST['pick']:
                messages.add_message(request, messagees.INFO, 'You did not make a selection!')
                return HttpResponseRedirect('/pick/%i' % gameno)
            p = Pick(user=request.session.get('_auth_user_id'), game=gameno, week=g.week, pick=request.POST['pick'])
            p.save()
            messages.add_message(request, messages.INFO, 'Pick added!')
            return HttpResponseRedirect('/mypicks')
        else:
            form = Form()

    return render_to_response('pick.html', {'form':form, 'away':away, 'home':home, 'gameid':gameno},
                              context_instance=RequestContext(request))

@decorators.login_required
def my_picks(request):
    p = Pick.objects.filter(user=request.session.get('_auth_user_id')).order_by('week')
    mypicks = []
    if p.exists():
        for i in p:
            mypicks.append([i.week, i.game, Team.objects.get(id=i.pick).name])
    return render_to_response('mypick.html', {'picks':mypicks}, context_instance=RequestContext(request))

def stats(request):
    s = Profile.objects.all().order_by('-w')
    rank = []
    for i in s:
        rank.append([User.objects.get(id=i.user), i.w, i.l])
    return render_to_response('stats.html', {'rank':rank}, context_instance=RequestContext(request))
