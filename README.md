# tele-rss
 
Simple server that provide access to your favorite 
Telegram channels as RSS feeds. Tele-rss acts as client,
so no need to add bots to channels.


## Features

- each channel available at `/rss/<channel-name>`
- list of channels available on `/rss-list`
- OPML available at `/rss-list.opml`
- Configurable via ini file
- HTTP and HTTPS access
- HTTP basic auth

## Dependencies

Require Python 3.6 and higher and following libraries

- telethon
- telethon-sync
- bottle
- cheroot
- rfeed

## First start

- Get your API ID and hash from 
https://my.telegram.org/auth
- Rename `tele-rss.ini.example` to `tele-rss.ini`
- Put API ID and hash as `api_id` and `api_hash` parameters
- start tele-rss as `python ./tele-rss.py`
- enter your phone when asked
- enter the code you recieve
- server should start serving at [http://localhost:8080](http://localhost:8080)
- check list of feeds at [http://localhost:8080/rss-list](http://localhost:8080/rss-list)
- click on any of the lists to get feed
- all channel entries served as feed items are marked as read automatically
- check list of feeds as OPML at [http://localhost:8080/rss-list.opml](http://localhost:8080/rss-list.opml)


## Additional setup

### Ignore list

Channels you don't want to see as RSS feeds can be listed in ini file.
Uncomment section in ini file

```
ignore_list = list,of,ignored,channels,or,their,id,comma,separated
```

List item can be taken from link `/rss/<channel_name_or_id>` when you click on channel link from `/rss-list` page

### Hostname/port change

Uncomment section in ini file

```
hostname = localhost
port = 8080
```

and set needed hostname and port to serve

### SSL/HTTPS

Get your certificate and private key files (self-signed or from SSL provider). Then
uncomment section in ini file

```
use_ssl = 1
cert_file = cacert.pem
key_file = privkey.pem
```

Start `tele-rss.py`, server should be available via https


### Simple authentication

Uncomment section in ini file

```
use_auth = 1
login = <your login>
password_hash = <sha256 encoded password>
```

Put desired login in `login` parameter and sha256 hash of password to `password_hash` parameter.
`/rss-list`, `/rss-list.opml` and `rss/<channel>` server endpoints will be protected by this login/password

