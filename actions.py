import sms
import telegram


def getAction(table):
    tables = {
        'transaction': doTransaction,
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
    req = sendSMS(data)
    res = None
    success = False
    try:
        res = req.json()
    except Exception:
        pass
    
    if not res is None:
        print('Response:', res)
        try:
            success = res.get('response',{}).get('success', False)
        except Exception:
            pass
    
    if success:
        res = sendTelegram(
            text = f'Success: SMS to {data["phone"]}: {data["text"]}'
        )
    else:
        res = sendTelegram(
            text = f'Fail: SMS to {data["phone"]}: {data["text"]}'
        )
    return res


def doMessage(data):
    print('Do message:', data)
    return sendTelegram(
        text=f'Получено сообщение {data["data"]["id"]} от {data["data"]["j"]["from"]["contact"]}: {data["data"]["j"]["message"]}',
        chat='message'
    )

def doTransaction(data):
    if data.get('action') == "INSERT" and data.get('data',{}).get('j',{}).get('type') == 'CustomerPayment':
        print('Do transaction:', data)
        return sendTelegram(
            text=f' {data["data"]["j"]["description"]} {data["data"]["j"]["business"]}: {data["data"]}',
            chat='message'
        )