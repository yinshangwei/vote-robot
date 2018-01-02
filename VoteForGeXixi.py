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
    vote_id = 22
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
    for i in range(100):
        vote_once()


def should_start_vote():
    url = 'https://wx.swsc.com.cn:8086/servlet/json'
    payload = 'funcNo=2002337&weixinpk=gh_4a5694efad94&org_mark=2&openid=oOIFkvyV_UlGzbah841ABDJL57tk123412612'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'e4046aa1-15ce-93f9-346a-6b73f919b906'
    }
    response = requests.request('POST', url, data=payload, headers=headers)
    vote_num_of_no2 = json.loads(response.text)['results'][1]['vote_num']
    vote_name_of_no2 = json.loads(response.text)['results'][1]['customer_name'].encode('utf-8')
    vote_num_of_no3 = json.loads(response.text)['results'][2]['vote_num']
    vote_name_of_no3 = json.loads(response.text)['results'][2]['customer_name'].encode('utf-8')
    print '******************* Vote For 葛溪溪********************'
    print '第二名({0})票数：{1}票'.format(vote_name_of_no2, '{:,}'.format(int(vote_num_of_no2)))
    print '第三名({0})票数：{1}票'.format(vote_name_of_no3, '{:,}'.format(int(vote_num_of_no3)))
    diff = int(vote_num_of_no2) - int(vote_num_of_no3)
    print '第二名({0})和第三名({1})相差：{2}票'.format(vote_name_of_no2, vote_name_of_no3, '{:,}'.format(diff))
    if diff < 10000:
        print '票数相差小于1万，开始投票...\n'
        return True
    else:
        print '票数相差大于1万，不再投票。\n'
        return False


if __name__ == '__main__':
    while True:
        if should_start_vote():
            print 'Start voting...'
            threadList = [
                threading.Thread(target=vote),
            ]
            for thread in threadList:
                thread.setDaemon(True)
                thread.start()
        time.sleep(10)
