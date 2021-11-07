from selenium import webdriver, common
import sqlite3
from browsermobproxy import Server
import time
import sys

URL_REGEX = 'https?://webbew.board.kettlec.tf*.*'
URL = 'https://webbew.board.kettlec.tf'

server = Server('browsermob-proxy-2.1.4/bin/browsermob-proxy')

server.start(options={
        'log_path': '/tmp'
})

db = sqlite3.connect(sys.argv[1] + "/Users")
cur = db.cursor()

cur.execute('''
    create table if not exists UsersInfo (
    id integer primary key autoincrement,
    Key text not null unique,
    Comments text,
    ImageSrc text,
    isBotChecked integer,
    timestamp datetime default current_timestamp
);
''')

proxy = server.create_proxy()
proxy.whitelist(URL_REGEX, 403)

OPTIONS = webdriver.firefox.options.Options()
OPTIONS.headless = True
OPTIONS.proxy = proxy.selenium_proxy()

driver = webdriver.Firefox(
        executable_path='geckodriver',
        service_log_path='/tmp/ff.log',
        log_path = '/tmp/gecko.log',
        options=OPTIONS
)


cookie = {'name' : 'flag', 'value' : 'Congratulations! Your picture won the kettle_ctfs best picture contest! Here is your flag: kettle_dont_trust_information_from_users'}

try:
        time.sleep(2)
        driver.get(URL)
        driver.add_cookie(cookie)
except:
        print("Failed on network error", sys.stderr)

while True:
                users = cur.execute('SELECT Key from UsersInfo where isBotChecked = 0;').fetchall()
                i = 0
                for i in range(len(users)):
                        print(f'Inner user: {users[i][0]}')
                        try:
                                driver.get(f'{URL}/{users[i][0]}')
                                time.sleep(2)
                        except common.exceptions.WebDriverException as error:
                                print(f"Inner: {error}", file=sys.stderr)
                        cur.execute('UPDATE UsersInfo SET isBotChecked = 1 WHERE Key = (?)', users[i])
                        db.commit()
                try:
                        driver.get('about:blank')
                except Exception as error:
                        print(f"Outer: {error}", file=sys.stderr)
                time.sleep(2)