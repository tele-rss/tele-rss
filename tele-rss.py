from telethon import TelegramClient
from rfeed import *
from bottle import route, ServerAdapter
import bottle
import configparser

ignore_list = []
cert_file = None
key_file = None
client = None


class CherootServer(bottle.ServerAdapter):
    def run(self, handler):  # pragma: no cover
        from cheroot import wsgi
        from cheroot.ssl import builtin
        self.options['bind_addr'] = (self.host, self.port)
        self.options['wsgi_app'] = handler

        certfile = self.options.pop('certfile', None)
        keyfile = self.options.pop('keyfile', None)
        chainfile = self.options.pop('chainfile', None)
        server = wsgi.Server(**self.options)
        if certfile and keyfile:
            server.ssl_adapter = builtin.BuiltinSSLAdapter(
                certfile, keyfile, chainfile)

        try:
            server.start()
        finally:
            server.stop()


@route('/rss-list')
def give_rss_list():
    titles=''
    for dialog in client.iter_dialogs():
        if dialog.is_channel:
            if dialog.entity.username is None:
                dialog_name = str(dialog.id)
            else:
                dialog_name = dialog.entity.username
            if dialog_name not in ignore_list:
                titles += '<br/><a href="/rss/' + dialog_name + '">' + dialog.title + '</a>: ' + str(dialog.unread_count) + '\n'
    return titles


@route('/rss/<channel_name>')
def give_rss(channel_name):
    channel_dialog = None
    feed_items = []

    for dialog in client.iter_dialogs():
        if dialog.is_channel and ((dialog.entity.username == channel_name) or (str(dialog.id) == channel_name)):
            channel_dialog = dialog
            break

    if channel_dialog is None:
        return ""

    group_entity = client.get_entity(channel_dialog.id)

    for index, message in enumerate(client.iter_messages(entity=group_entity)):
        if index >= channel_dialog.dialog.unread_count:
            break
        feed_item = get_feed_item(message)
        if feed_item is not None:
            feed_items.append(feed_item)

    client.send_read_acknowledge(group_entity, max_id=channel_dialog.dialog.top_message)

    feed = Feed(
        title=channel_name,
        link="https://t.me/" + channel_name,
        description=channel_name,
        language="ru_RU",
        lastBuildDate=channel_dialog.date,
        items=feed_items)

    return feed.rss()


@bottle.error(404)
def error404(error):
    return ""


@bottle.error(500)
def error500(error):
    return ""


def get_feed_item(message):
    message_dict = message.to_dict()
    try:
        user_mess = message_dict['message']
    except KeyError:
        return None

    channel_id = message_dict['to_id']['channel_id']
    channel_name = client.get_entity(channel_id).to_dict()['title']

    try:
        url = message_dict['media']['webpage']['url']
    except TypeError:
        url = ''
    except KeyError:
        url = ''

    mess_date = message_dict['date']

    feed_item = Item(
        title=user_mess[0:50],
        link=url,
        description=user_mess,
        author=channel_name,
        guid=Guid(user_mess),
        pubDate=mess_date
    )

    return feed_item


api_hash = None
api_id = None

try:
    config = configparser.ConfigParser()
    config.read('tele-rss.ini')
    config_tele_rss = config['tele-rss']
    api_id = int(config_tele_rss['api_id'])
    api_hash = config_tele_rss['api_hash']
    ignore_list = config_tele_rss['ignore_list'].split(',')

    if config_tele_rss['use_ssl'] == '1':
        cert_file = config_tele_rss['cert_file']
        key_file = config_tele_rss['key_file']
        if (cert_file is None) or (key_file is None):
            print("Cert file or key file are not set in config file")
            exit(-2)

except:
    print("Bad config file")
    exit(-1)

try:
    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

except ConnectionError:
    print("Cannot connect to TG")
    exit(-3)

bottle.run(host='localhost', port=8080, server=CherootServer, certfile=cert_file, keyfile=key_file)

client.run_until_disconnected()


