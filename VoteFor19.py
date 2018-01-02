# coding=utf-8
import json
import threading
import requests
import time
import random
import string


vote_num = 0


def get_random_string(id_length):
    rand_string = 'oOIFkvyV_'
    for i in range(id_length):
        rand_string += random.choice(string.ascii_letters + string.digits)
    return rand_string


def vote_once():
    vote_id = 19
    url = 'https://wx.swsc.com.cn:8086/servlet/json'
    openid = get_random_string(22)
    payload = 'vote_id={0}&openid={1}&org_mark=2&weixinpk=gh_4a5694efad94&funcNo=2002338'.format(vote_id, openid)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'c7b5bd68-3d92-c529-5fd9-30e1f884613e'
    }
    for i in range(3):
        try:
            response = requests.request('POST', url, data=payload, headers=headers, timeout=10)
            if json.loads(response.text)['error_no'] == '0':
                global vote_num
                vote_num += 1
        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout')
            continue
        except requests.exceptions.Timeout:
            print('Timeout')
            continue
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            continue
        except requests.exceptions.HTTPError:
            print('HTTPError')
            continue


def vote():
    for i in range(10000):
        vote_once()


if __name__ == '__main__':
    threadList = [
        threading.Thread(target=vote),
        threading.Thread(target=vote),
        threading.Thread(target=vote),
        threading.Thread(target=vote),
        threading.Thread(target=vote),
    ]
    for thread in threadList:
        thread.setDaemon(True)
        thread.start()
    thread.join()
