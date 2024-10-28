<h1>CREX Live Scraper</h1>
The project is based on web scraping and gathers data from crex.live about different pages. The main modules/libs used in the project are:
<ul>
  <li><strong>Requests & BeautifulSoup</strong> - The requests lib is used for extraction from static information like player names, scheduled matches, etc.</li>
  <li><strong>Selenium</strong> - Selenium is used for interacting with webpage for dynamic page elements like switching between playing xi tabs and live score updation.</li>
  <li><strong>Threading</strong> - Threading is usedfor running all 5 scripts simutaneously. It can be improved using celery and caching which can be implemented as a part of future scope.</li>
</ul>
<p>Using requests for static elements is a better choice because it is faster and lightweight and focuses on data retrieval while Selenium is preferred for dynamic elements like dropdown for
 on-bench players and live score updation, although selenium might be a little slow but it comes with the advantage of interacting with the webpage.</p>
<p>The project currently gathers over 60+ parameters from 4 different pages dynamically running every 10 seconds with the time.sleep function currently. This can also be done using cron-jobs in app dev phase.</p>
<h3>Setting up the project</h3>
<ul>
  <li><strong>Source Code</strong> - Clone the git repo's master branch and install the requirements using pip install -r requirements.txt.</li>
  <li><strong>Run main.py</strong> - Run the main.py file which is connected to all other scripts in a threaded manner, printing the results in the console every 10 seconds.</li>
</ul>
