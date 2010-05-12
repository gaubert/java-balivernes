# Content of the crontab
# Do crontab -e to edit and add the following lines

# run every 3 hours starting at 1 o'clock
* 1,4,7,10,13,16,19,22 * * * echo "Hello" > /tmp/hello.txt
# every 10 minutes
*/10 * * * * /tmp/new-env/bin/crontab_runner.sh >> /tmp/crontab_runner.log
# cron job every  minutes
* * * * * /tmp/new-env/bin/echo_time.sh >> /tmp/hello_every_minutes.txt
* * * * * /tmp/new-env/bin/crontab_runner.sh >> /tmp/crontab_runner.log

This needs to be done to run the generator and emailer
/tmp/new-env/bin/crontab_runner.sh >> /tmp/crontab_runner.log