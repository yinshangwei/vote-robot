# coding=utf-8
import json
from time import sleep, strftime, localtime
import requests


def should_start_vote():
    url = 'https://wx.swsc.com.cn:8086/servlet/json'
    payload = 'funcNo=2002337&weixinpk=gh_4a5694efad94&org_mark=2&openid=oOIFkvyV_UlGzbah841ABDJL57tk123412612'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Postman-Token': 'e4046aa1-15ce-93f9-346a-6b73f919b906'
    }
    response = requests.request('POST', url, data=payload, headers=headers)
    print '******************* {0} ********************'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    for i in range(8):
        print '第{0}名：{1}，id：{2}，票数：{3}票'.format(
            i + 1,
            json.loads(response.text)['results'][i]['customer_name'].encode('utf-8'),
            json.loads(response.text)['results'][i]['vote_id'],
            '{:,}'.format(int(json.loads(response.text)['results'][i]['vote_num']))
        )
    print ''


if __name__ == '__main__':
    while True:
        should_start_vote()
        sleep(10)
