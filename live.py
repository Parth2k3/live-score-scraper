from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('C:/Users/sony/Downloads/chromedriver.exe') 
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://crex.live/scoreboard/PYU/1MS/4th-Match/4T/8W/hbhw-vs-sytw-4th-match-womens-big-bash-league-2024/live")

def fetch_live_score():
    print('fetching live score ...')
    # try:
    innings_break = False
    text = driver.find_element(By.CSS_SELECTOR, 'span.font3').text.strip()
    innings_break = (text == 'Innings Break') or (text == 'Players Entering')

    if not innings_break:
        try:
            player_name_element = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-name")[0].find_element(By.CSS_SELECTOR, 'p')
        except:
            print('player 1 not found')
        try:
            player_name_element2 = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-name")[1].find_element(By.CSS_SELECTOR, 'p')
        except:
            print('player 2 not found')
        try:
            bowler_element = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-partnership")[2]
        except:
            print('bowler not found')
        try:
            bowler_name = bowler_element.find_element(By.CSS_SELECTOR, 'div.batsmen-name').find_element(By.CSS_SELECTOR, 'p').text
        except:
            print('bowler name not found')
        player_name1 = player_name_element.text
        player_name2 = player_name_element2.text
        batsman1_score = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-score")[0]
        runs1 = batsman1_score.find_elements(By.CSS_SELECTOR, 'p')[0].text
        balls1 = batsman1_score.find_elements(By.CSS_SELECTOR, 'p')[1].text

        batsman2_score = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-score")[1]
        runs2 = batsman2_score.find_elements(By.CSS_SELECTOR, 'p')[0].text
        balls2 = batsman2_score.find_elements(By.CSS_SELECTOR, 'p')[1].text

        batsman3_score = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-score")[2]
        bowler_score = batsman3_score.find_elements(By.CSS_SELECTOR, 'p')[0].text
        bowler_overs = batsman3_score.find_elements(By.CSS_SELECTOR, 'p')[1].text

        batting_team = driver.find_element(By.CSS_SELECTOR, 'div.team-1').text
        runs = driver.find_element(By.CLASS_NAME, 'f-runs').find_elements(By.CSS_SELECTOR,'span')[0].text
        overs = driver.find_element(By.CLASS_NAME, 'f-runs').find_elements(By.CSS_SELECTOR,'span')[1].text
        

    last_ball = driver.find_element(By.CSS_SELECTOR, 'div.result-box').find_element(By.CSS_SELECTOR,'span').text
    required = driver.find_element(By.CSS_SELECTOR, 'div.final-result').text

    try:
        crr = driver.find_element(By.CSS_SELECTOR, 'div.team-run-rate').find_elements(By.CSS_SELECTOR,'span.data')[0].text
    except:
        crr = 'NA'
    try:
        rrr = driver.find_element(By.CSS_SELECTOR, 'div.team-run-rate').find_elements(By.CSS_SELECTOR,'span.data')[1].text
    except:
        rrr = 'NA'
    last_balls=[]

    last_ballss = driver.find_elements(By.CSS_SELECTOR, 'div.over-ball')
    for l in last_ballss:
        last_balls.append(l.text)

    probability = {}
    try:
        team1 = driver.find_elements(By.CSS_SELECTOR, 'div.teamNameScreenText')[0].text
        team2 = driver.find_elements(By.CSS_SELECTOR, 'div.teamNameScreenText')[1].text
        percentages1 = driver.find_elements(By.CSS_SELECTOR, 'div.percentageScreenText')[0].text
        percentages2 = driver.find_elements(By.CSS_SELECTOR, 'div.percentageScreenText')[1].text
        probability[team1] = percentages1
        probability[team2] = percentages2
    except:
        print('Probability not available')

    if not ('won' in text):
        try:
            proj_overs = driver.find_elements(By.CSS_SELECTOR, 'div.over-text')
            table_rows = driver.find_element(By.CSS_SELECTOR, 'div.cl-8').find_element(By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
            projected_data = {}
            heads = driver.find_element(By.CSS_SELECTOR, 'div.projected-score').find_elements(By.CSS_SELECTOR, 'span.rr-data')

            for i in range(len(proj_overs)):
                row_data = []
                tds = table_rows[i].find_elements(By.CSS_SELECTOR, 'td')
                for i in range(tds):
                    d = tds[i].find_element(By.CSS_SELECTOR, 'span').text
                    h = heads[i].text
                    row_data.append({h:d})
                over = proj_overs[i].find_element(By.CSS_SELECTOR, 'span').text
                projected_data[over] = row_data
        except Exception as e:
            print('Projected overs not found', e)
            projected_data = ''
    else:
        projected_data = ''

    return {
        'projected_data':projected_data,
        'last_balls':last_balls,
        'crr':crr,
        'rrr':rrr,
        'required':required,
        'last_ball':last_ball,
        'runs': runs,
        'overs':overs,
        'probability':probability,
        'bat_team': batting_team,
        "batsman1":player_name1,
        'batsman2': player_name2,
        'bowler': bowler_name,
        'runs1':runs1,
        'balls1':balls1,
        'runs2':runs2,
        'balls2':balls2,
        'bowler_score':bowler_score,
        'bowler_overs':bowler_overs
    }
    # except Exception as e:
    #     print("Error fetching score:", e)
    #     return None

# Fetch live score at intervals
def fetch_score(results, i):
  while True:
    live_score = fetch_live_score()
    if live_score:
        results[i] = (live_score)
    else:
        results[i] = ("Could not retrieve live score.")
    # print(results[0])
    time.sleep(10)
# results = [None]
# fetch_score(results, 0)