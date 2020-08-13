import requests # 사용이유: 크롤링이나 API등 데이터가져오기위해
import datetime
import telegram
import key
from apscheduler.schedulers.blocking import BlockingScheduler

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?'

SERVICE_KEY = key.API_KEY
bot = telegram.Bot(token=key.TELEGRAM_KEY)
today = datetime.datetime.today()
base_date = today.strftime("%Y%m%d") # 발표일 = 20200813 strftime 날짜와 시간 정보를 문자열로 바꿔줌
base_time = "0800" # API내에서 발표시각을 말한다.

nx = "62" #격자X
ny = "126" #격자y자

payload = 'serviceKey=' + SERVICE_KEY + '&' + \
          'dataType=json' + '&' + \
          'base_date=' + base_date + '&' + \
          'base_time=' + base_time + '&' + \
          'nx=' + nx + '&' + \
          'ny=' + ny


res = requests.get(url+payload)
STATUS = False
PTY_TATE = False
if res.json().get('response').get('header')['resultCode'] == '00':
    STATUS = True

if STATUS:

    items = res.json().get('response').get('body').get('items')
    '''
    자료구분 : Category 
    POP : 강수확률 
    PTY : 강수형태 0 - 없음 1 - 비 2 - 비/눈(진눈깨비) 3- 눈 4- 소나기
    R06 : 6시간 강수량 
    REH : 습도
    S06 : 6시간 신적설
    SKY : 하늘상태
    T3H : 3시간 ~ 기온
    UUU : 풍속 m/s
    VEC : 풍향 m/s
    '''
    data = dict()
    data['date'] = base_date
    weather = dict()
    for idx in range(len(items['item'])):

        category = items['item'][idx]['category']
        # 강수확률
        if category == 'POP':
            weather['pop'] = items['item'][idx]['fcstValue'] + "%"
        # 기온
        if category == 'T3H':
            weather['T3H'] = items['item'][idx]['fcstValue'] + "도"

        # 습도
        if category == 'REH':
            weather['REH'] = items['item'][idx]['fcstValue']
        # 기상상태
        if category == 'PTY':
            weather['PTY'] = items['item'][idx]['fcstValue']

            if weather['PTY'] == '1':
                PTY = '비'
                PTY_TATE = True
            elif weather['PTY'] == '2':
                PTY = '비/눈'
                PTY_TATE = True
            elif weather['PTY'] == '3':
                PTY = '눈'
                PTY_TATE = True
            elif weather['PTY'] == '4':
                PTY = '소나기'
                PTY_TATE = True
            else:
                PTY = '특이기상예보없음'
                PTY_TATE = False
            if PTY_TATE:
                weather['PTY_STATE'] = PTY

    data['weather'] = weather
    print(data)
    txt = '오늘(' + data['date'] + ')의 날씨를 전달드립니다.' + \
          '강수확률은 ' + data['weather']['pop'] + '이고 '

    if PTY_TATE:
        txt += '기상변화는 ' +data['weather']['PTY'] + '가 있을 것으로 보입니다.'

    txt += '더불어 오늘 기온은 ' + data['weather']['T3H'] + '일 것으로 보입니다.'
    txt += '습도는 ' + data['weather']['REH'] + '% 일것으로 확인됩니다.'

    print(txt)
        #print(items['item'][idx] )
    bot.sendMessage(chat_id=1242107778, text=txt)




