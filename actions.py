import sms
import telegram


def getAction(table):
    tables = {
        'message': doMessage,
        'SMS': doSMS
    }
    return tables.get(table)


def sendSMS(data):
    gw = sms.SMSGateway()
    gw.businessId = data.get('business_id')
    gw.recordId = data.get('record_id')
    gw.phone = data.get('phone')
    gw.text = data.get('text')
    gw.time = data.get('time')
    res = gw.send()
    return res


def sendTelegram(chat=None, text=None):
    gw = telegram.TgmGateway()
    chat = chat or 'main'
    gw.chat = gw.chats['main']
    gw.text = text
    print(text)
    res = gw.send()
    return res


def doSMS(data):
    print('Do SMS:', data)
    res = sendSMS(data)
    if res is None:
        res = sendTelegram(
            text = f'SMS to {data["phone"]}: {data["text"]}'
        )
    return res


def doMessage(data):
    print('Do message:', data)
    return sendTelegram(
        text=f'Получено сообщение {data["data"]["id"]} от {data["data"]["j"]["from"]["contact"]}: {data["data"]["j"]["message"]}',
        chat='message'
    )
