from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
BASE_URL = "https://crex.live"

matches = []

def get_match_schedule():
    global matches
    url = f"{BASE_URL}/fixtures/match-list"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    match_list = soup.find_all("div", class_="match-item")
    matches = []
    for match in match_list:
        match_link = match.find("a", href=True)
        match_url = BASE_URL + match_link['href']
        match_time_str = match.find("div", class_="match-time").text.strip()
        match_time = datetime.strptime(match_time_str, "%Y-%m-%d %H:%M")
        matches.append({
            'url': match_url,
            'time': match_time,
        })
    return matches

def scrape_match_details(match_url):
    response = requests.get(match_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    match_info = soup.find("div", class_="match-info").text.strip()
    squads = soup.find("div", class_="squads").text.strip()
    live_data = soup.find("div", class_="live").text.strip()
    scorecard = soup.find("div", class_="scorecard").text.strip()
    
    match_details = {
        'match_info': match_info,
        'squads': squads,
        'live_data': live_data,
        'scorecard': scorecard,
    }
    return match_details

def monitor_matches():
    matches = get_match_schedule()
    for match in matches:
        match_time = match['time']
        if datetime.now() < match_time:
            delta = (match_time - datetime.now()).total_seconds()
            threading.Timer(delta, scrape_match_details, [match['url']]).start()
        else:
            scrape_match_details(match['url'])

def job():
    print("Checking for updates...")
    monitor_matches()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().minute.do(job)

@app.route('/')
def index():
    return render_template('index.html', matches=matches)

@app.route('/match/<path:match_url>')
def match_details(match_url):
    match_url = BASE_URL + '/' + match_url
    details = scrape_match_details(match_url)
    return jsonify(details)

if __name__ == "__main__":
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
