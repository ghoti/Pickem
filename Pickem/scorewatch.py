__author__ = 'ghoti'
import re
import urllib2

gamestring = re.compile('\w{10}(\d)=(?P<team1>[A-Za-z\s]*)(?P<score1>\d{1,2}|\d{0})\s(?:@|at)\s(?P<team2>[A-Za-z\s]*)(?P<score2>\d{1,2}|\d{0})\s\((?P<info>.*)\)')
#using nhl for now, same line format, bonus for having games going on :D
gameurl = 'http://sports.espn.go.com/nhl/bottomline/scores'

def scores():
    scores = urllib2.urlopen(gameurl).read()
    #scores = '&nfl_s_delay=120&nfl_s_stamp=0118113743&nfl_s_left1=Baltimore%2024%20%20%20^Pittsburgh%2031%20(FINAL)&nfl_s_right1_count=0&nfl_s_url1=http://sports.espn.go.com/nfl/boxscore?gameId=310115023&nfl_s_left2=^Green%20Bay%2048%20%20%20Atlanta%2021%20(FINAL)&nfl_s_right2_count=0&nfl_s_url2=http://sports.espn.go.com/nfl/boxscore?gameId=310115001&nfl_s_left3=Seattle%2024%20%20%20^Chicago%2035%20(FINAL)&nfl_s_right3_count=0&nfl_s_url3=http://sports.espn.go.com/nfl/boxscore?gameId=310116003&nfl_s_left4=^NY%20Jets%2028%20%20%20New%20England%2021%20(FINAL)&nfl_s_right4_count=0&nfl_s_url4=http://sports.espn.go.com/nfl/boxscore?gameId=310116017&nfl_s_count=4&nfl_s_loaded=true'
    scores = scores.replace('%20%20', ' @')
    scores = scores.replace('%20', ' ')
    scores = scores.replace('%26', '')
    scores = scores.replace('^', '')
    #scores = scores.replace('at', '@')
    numgames = scores.split('&')[-2][-1]
    current = 0
    games = []
    #print scores
    for i in xrange(0, int(numgames)):
        current += 3
        m = re.match(gamestring, scores.split('&')[current])
        if m:
            games.append(m.groups())
    return games