# Kindle Display and Server

This project fetches my todo list and random quotes and displays them on my
kindle and converts it into a low power information display.

It is largely inspired by Matthew Petroff's [Kindle Weather
Display](http://mpetroff.net/2012/09/kindle-weather-display/). I rewrote the
server and modified the client to display my todo list and random quotes.  This
works by generating PNGs with Pillow and Python. They are served by the server
and fetched by the Kindle.

This should work with any Kindle that has been Jailbroken.

##Server

* On Ubuntu Linux, install the dependencies:

        sudo apt-get install python3-pip libfreetype6-dev
        sudo pip3 install Pillow cairosvg

* Make sure port `9876` is forwarded to your server
* `cd server/`
* Run `python3 server.py`

The server will serve at `http://<your-ip>:9876`

##Client (The Kindle)

* The following relies on Jennifer's
  [tutorial](http://www.shatteredhaven.com/2012/11/1347365-kindle-weather-display.html)
  to get SSH access
* Copy the `kindle_client` directory to `/mnt/us/` on the Kindle
* Run `chmod +x fetch_and_display.sh`
* Add the following entry to `/etc/crontab/root`:
        `* * * * * /mnt/us/kindle_display/fetch_and_display.sh`
* Run `/etc/init.d/cron restart` to restart the cron daemon
