import requests
from bs4 import BeautifulSoup

BASE_URL = "https://crex.live"

match_info = []

def get_match_schedule(url):
    print('getting match schedules ... ')
    global matches
    get_url = f"{BASE_URL}/{url}"
    response = requests.get(get_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    left_container = soup.find('div', class_='info-left-wrapper')
    right_container = soup.find('div', class_='info-right-wrapper')
    left_sections = left_container.find_all('div')
    league = left_sections[0].find('a').find('img').get('alt')
    match_number = left_sections[0].find('a').find('div',class_='s-format').text
    venue_detail_section = left_container.find('div', class_='venue-detail')
    # print(venue_detail_section.find_all('div'))
    # venue = venue_detail_section.find('div', class_='match-venue').find('div').text
    date = venue_detail_section.find('div', class_='match-date').find('div').text
    team1 = left_container.find_all('div',class_='form-team-name')[0].text
    team2 = left_container.find_all('div',class_='form-team-name')[1].text
    format_match = left_container.find_all('div',class_='format-match')[0]
    form_signs = format_match.find('div', class_='align-center')
    signs = form_signs.find_all('div',class_='match')
    last_matches_team1 = []
    for sign in signs:
        last_matches_team1.append(sign.text)
    format_match2 = left_container.find_all('div',class_='format-match')[1]
    form_signs2 = format_match2.find('div', class_='align-center')
    signs2 = form_signs2.find_all('div',class_='match')
    last_matches_team2 = []
    for sign in signs2:
        last_matches_team2.append(sign.text)

    table1 = left_container.find_all('app-match-info-table')[0]
    trs1 = table1.find_all('tr')
    team_comparison = []
    for tr in trs1:
        team_comparison.append({
            f"{tr.find_all('td')[1].text}":(tr.find_all('td')[0].text,tr.find_all('td')[2].text)
        })
    temp = left_container.find('div',class_='weather-temp').text
    venue_match_cnt = left_container.find('div',class_='match-count').text
    win_bat_first = left_container.find_all('span', class_='match-win-per')[0].text
    win_bowl_first = left_container.find_all('span', class_='match-win-per')[1].text
    avg_first_score = left_container.find_all('span',class_='venue-avg-val')[0].text
    avg_sec_score = left_container.find_all('span',class_='venue-avg-val')[1].text
    highest_total = left_container.find_all('span',class_='venue-score')[0].text if left_container.find_all('span',class_='venue-score') else ""
    lowest_total = left_container.find_all('span',class_='venue-score')[1].text if left_container.find_all('span',class_='venue-score') else ""
    highest_chased = left_container.find_all('span',class_='venue-score')[2].text if left_container.find_all('span',class_='venue-score') else ""
    lowest_chased = left_container.find_all('span',class_='venue-score')[3].text if left_container.find_all('span',class_='venue-score') else ""
    toss = right_container.find_all('div')[0].find('p').text
    players = right_container.find_all('div',class_='playingxi-card-row')
    playing_xi = []
    for player in players:
        pname = player.find('div', class_='p-name')
        playing_xi.append(pname.text)

    recent_matches = []
    first_team = left_container.find_all('div', class_='global-match-team')
    decisions = left_container.find_all('div', class_='match-dec-text')
    second_team = left_container.find_all('div', class_='global-match-end')

    for i in range(len(first_team)):
        recent_matches.append(
            f"{first_team[i].find('div', class_='team-name').text} ({first_team[i].find('div', class_='team-score').text},{first_team[i].find('div', class_='team-over').text}) VS {second_team[i].find('div', class_='team-name').text} ({second_team[i].find('div', class_='team-score').text},{second_team[i].find('div', class_='team-over').text}), Result - {decisions[i].text}"
        )

    match_info.append({
        'league' : league,
        'match_number' : match_number,
        # 'venue' : venue,
        'date' : date,
        'team1' : team1,
        'team2' : team2,
        'last_matches_team1' : last_matches_team1,
        'last_matches_team2' : last_matches_team2,
        'team_comparison' : team_comparison,
        'temp' : temp,
        'venue_match_cnt' : venue_match_cnt,
        'win_bat_first' : win_bat_first,
        'win_bowl_first' : win_bowl_first,
        'avg_first_score' : avg_first_score,
        'avg_sec_score' : avg_sec_score,
        'highest_total' : highest_total,
        'lowest_total' : lowest_total,
        'highest_chased' : highest_chased,
        'lowest_chased' : lowest_chased,
        'toss' : toss,
        'playing_xi' : playing_xi,
        'recent_matches' : recent_matches
    })

    return (match_info)
import time
# results = []
def get_schedule(results, i):
  while True:  
    results[i] = get_match_schedule('scoreboard/RNU/1OX/19th-Match/OT/QH/edk-vs-vls-19th-match-european-cricket-series-malta-2024/info')
    print(results[i])
    time.sleep(10)

# get_schedule(results, 2)