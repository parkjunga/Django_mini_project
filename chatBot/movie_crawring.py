import requests
import telegram
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

bot = telegram.Bot(token='1390302525:AAHfbQVdvUrYrMYSMqACSc62WcErBEJxwSQ')
url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0059&date=20200813'

# 반복이 필요한 부분은 함수로 선언
def job_function():
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    # 가쟈올 부분
    sphereX = soup.select_one('span.sphereX')
    if sphereX:
        sphereX = sphereX.find_parent('div',class_='col-times')
        title = sphereX.select_one('div.info-movie > a > strong').text.strip()
        print(title + '예매가 오픈되었습니당')
        bot.sendMessage(chat_id=1242107778, text=title + '예매가 오픈되었습니당')
        sched.pause() # 열린경우에만 보내고 스케줄러 중단한다
    else:
        print('안열림')
        bot.sendMessage(chat_id=1242107778, text='아직 예매가 오픈되지 않았습니다!')

sched = BlockingScheduler()
# 스케줄 등록 ,interval 일정간격 반복 , 30초에 한번씩
sched.add_job(job_function, 'interval', seconds =30 )
sched.start()