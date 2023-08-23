# Frigate Telegram Alerts
Script to send alerts to telegram when there is an event in frigate. Uses the Frigate API to check if there is a new event and send it to Telegram.

## Installation
1. Clone this repository
2. Install the requirements using pipenv: pipenv --rm; pipenv --clear update 
3. Run it: pipenv run python3 main.py

The best approach is to configure it at startup ysing systemd or in the cron:

@reboot sleep 5 && cd  /home/dev/frigatetelegramalerts && /usr/bin/pipenv run python main.py