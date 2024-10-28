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
# Path to the ChromeDriver
service = Service('C:/Users/sony/Downloads/chromedriver.exe') 
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the live score page
driver.get("https://crex.live/scoreboard/REU/1OM/4th-ODI/6I/JM/usaw-vs-zimw-4th-odi-usa-women-tour-of-zimbabwe-2024/live")  # Replace with the actual live score URL

# Define a function to fetch the live score
def fetch_live_score():
    # try:
    player_name_element = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-name")[0].find_element(By.CSS_SELECTOR, 'p')
    player_name_element2 = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-name")[1].find_element(By.CSS_SELECTOR, 'p')
    bowler_element = driver.find_elements(By.CSS_SELECTOR, "div.batsmen-partnership")[2]
    bowler_name = bowler_element.find_element(By.CSS_SELECTOR, 'div.batsmen-name').find_element(By.CSS_SELECTOR, 'p').text
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


    crr = driver.find_element(By.CSS_SELECTOR, 'div.team-run-rate').find_elements(By.CSS_SELECTOR,'span.data')[0].text
    rrr = driver.find_element(By.CSS_SELECTOR, 'div.team-run-rate').find_elements(By.CSS_SELECTOR,'span.data')[1].text
    last_balls=[]

    last_ballss = driver.find_elements(By.CSS_SELECTOR, 'div.over-ball')
    for l in last_ballss:
        last_balls.append(l.text)

    probability = {}
    team1 = driver.find_elements(By.CSS_SELECTOR, 'div.teamNameScreenText')[0].text
    team2 = driver.find_elements(By.CSS_SELECTOR, 'div.teamNameScreenText')[1].text
    percentages1 = driver.find_elements(By.CSS_SELECTOR, 'div.percentageScreenText')[0].text
    percentages2 = driver.find_elements(By.CSS_SELECTOR, 'div.percentageScreenText')[1].text
    probability[team1] = percentages1
    probability[team2] = percentages2
    
    proj_overs = driver.find_elements(By.CSS_SELECTOR, 'div.over-text')


    return {
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
try:
    while True:
        # Print the live score without reloading the page
        live_score = fetch_live_score()
        if live_score:
            print("Live Score:", live_score)
        else:
            print("Could not retrieve live score.")

        # Wait for 10 seconds before fetching again (adjust as needed)
        time.sleep(10)

finally:
    driver.quit()
