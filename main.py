import threading
from match_info import get_schedule
from live import fetch_score
from schedules import get_mschedule
from scorecard import fetch_scorecard
from playingxi import get_playing11

scripts = [get_schedule, fetch_score, get_mschedule, fetch_scorecard, get_playing11]
threads = []
results = [None] * len(scripts)

import time
for i, script in enumerate(scripts):
    thread = threading.Thread(target=script, args=(results, i))
    threads.append(thread)
    thread.start()

def monitor_results():
    while True:
        print("\nCurrent results:")
        for i, result in enumerate(results):
            print(f"Script {i + 1} result: {result}")
        time.sleep(10)  # Wait before printing results again

monitor_thread = threading.Thread(target=monitor_results)
monitor_thread.daemon = True  # Set as a daemon so it doesn't block program exit
monitor_thread.start()
