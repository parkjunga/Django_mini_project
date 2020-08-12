import telegram


token = '1390302525:AAHfbQVdvUrYrMYSMqACSc62WcErBEJxwSQ'
bot = telegram.Bot(token=token)
for i in bot.getUpdates():
     print(i.message)

bot.sendMessage(chat_id=1242107778 ,text='오늘날씨좋아')