# CRM-DB

tweetPuller.py has to be executed every minute. We'll add it to a cron job

env EDITOR=nano crontab -e

* * * * * /Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/bchangip/Google Drive/Universidad/Cuarto/Primer semestre/Bases de datos/CRM-DB/webserver/tweetPuller.py