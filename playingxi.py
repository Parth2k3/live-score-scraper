from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('C:/Users/sony/Downloads/chromedriver.exe') 
driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get("https://crex.live/scoreboard/RRE/1P0/9th-Match/DF/DG/ajm-vs-sha-9th-match-emirates-d20-league-2024/info")  # Replace with the actual live score URL
# driver.execute_script("""
#     const ads = document.querySelectorAll('.GoogleActiveViewElement');
#     ads.forEach(ad => ad.style.display = 'none');
# """)
driver.execute_script("document.querySelector('ins.adsbygoogle').style.display = 'none';")

def fetch_bench():
    
    bench=[]
    playerssec = driver.find_element(By.CSS_SELECTOR, 'div.on-bench-wrap')
    players = playerssec.find_elements(By.CSS_SELECTOR, 'div.p-name')
    for player in players:
        bench.append(player.text)
    
    return bench


def fetch_playingxi():
    playing=[]
    playerssec = driver.find_element(By.CSS_SELECTOR, 'div.playingxi-card')
    players = playerssec.find_elements(By.CSS_SELECTOR, 'div.p-name')
    for player in players:
        playing.append(player.text)
    return playing

def get_playing11(results, i):
  while True:
    print('getting playing 11 .. ')
    playing_xi1=[]
    playing_xi2 = []
    btn = driver.find_elements(By.CSS_SELECTOR, "button.playingxi-button")[1]
    time.sleep(1)
    btn.click()
    time.sleep(1)
    bench_toggle2 = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.bench-toggle"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", bench_toggle2)
    driver.execute_script("arguments[0].click();", bench_toggle2)
    playing_xi2 = fetch_playingxi()
    bench2 = fetch_bench()
    time.sleep(1)
    btn = driver.find_elements(By.CSS_SELECTOR, "button.playingxi-button")[0]
    head = driver.find_element(By.CSS_SELECTOR, 'div.playingxi-header')
    driver.execute_script("arguments[0].scrollIntoView(true);", head)
    time.sleep(1)
    btn.click()
    time.sleep(1)
    playing_xi1 = fetch_playingxi()

    header = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.playingxi-card"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", header)
    time.sleep(1)
    bench1 = fetch_bench()
    if playing_xi1 or playing_xi2 or bench1 or bench2:
        results[i] =({
            'team1':playing_xi1,
            'team2':playing_xi2,
            'bench1': bench1,
            'bench2':bench2
            })
    else:
        results[i] = ("Could not retrieve live score.")
    time.sleep(10)