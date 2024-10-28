import requests
from bs4 import BeautifulSoup

BASE_URL = "https://crex.live"

matches_data = [] #team1, score1, over1, team2, score2, over2, status, href

def get_match_schedule():
    global matches
    url = f"{BASE_URL}/fixtures/match-list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    match_list = soup.find("ul", class_="match-list-wrapper")
    matches = soup.find_all('li', class_='match-card-container')
    for match in matches:
        href = match.find('a',href=True).get('href')
        team1 = match.find_all('div', class_='team2')[0]
        team2 = match.find_all('div', class_='team2')[1]
        team1_name = team1.find('img')['alt']
        team2_name = team2.find('img')['alt']
        status = ''
        team1_score = ''
        team2_score = ''
        if match.find('div', class_='not-started') is None:
            if match.find('span', class_='liveTag'):
                status = 'Live'
            team1_score = team1.find('span', class_='team-score').text if team1.find('span', class_='team-score') else ''
            team1_overs = team1.find('span', class_='total-overs').text if team1.find('span', class_='team-overs') else ''
            team2_overs = team2.find('span', class_='total-overs').text if team2.find('span', class_='team-overs') else ''
            team2_score = team2.find('span', class_='team-score').text if team2.find('span', class_='team-score') else ''
        verdict=''
        reason=''
        result = match.find('div', class_='result')
        if result and result.find('span', class_='liveTag') is None:
            verdict = result.find('span').text if result.find('span') else ''
            reason = result.find('span', class_='reason').text if result.find('span', class_='reason') else ''
            result = result.text
        date=''
        time=''
        if match.find('div', class_='not-started'):
            date = match.find('div', class_='not-started').find('p',class_='time').text
            time = match.find('div', class_='not-started').find('div',class_='start-text').text
        
        matches_data.append({
            'href':href,
            'team1':team1_name,
            'team2':team2_name,
            'team1_score':team1_score,
            'team1_overs': team1_overs,
            'team2_overs': team2_overs,
            'team2_score':team2_score,
            'status':status,
            'verdict': verdict,
            'reason':reason,
            'date':date,
            'time':time
        })
        print('')

get_match_schedule()
for row in matches_data:
    print(row)