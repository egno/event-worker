from dotenv import load_dotenv
import os
import requests


class TgmGateway(object):

    def __init__(self):
        self.chats = {'message':None, 'main': None}
        self.loadEnv()
        self.chat = None
        self.text = None


    def loadEnv(self):
        load_dotenv()
        self.gatewayTemplate = os.getenv("TGM_GATEWAY")
        self.key = os.getenv('TGM_BOT_KEY')
        self.site = os.getenv("SITE")
        self.chats['main'] = os.getenv("TGM_CHAT_ID")
        self.chats['message'] = os.getenv("TGM_MESSAGE_CHAT_ID")

    def gateway(self):
        return self.gatewayTemplate % (self.key,)

    def checkParam(self):
        return (self.key is not None)

    def send(self):
        if not self.checkParam():
            print('No data:', self)
            return
        data = {'chat_id': self.chat or (self.chats.get('main')),
                'text': self.text}
        try:
            res = requests.post(self.gateway(), data=data, timeout=3)
            print('GW Send:', res.url)
            return res
        except requests.exceptions.ConnectionError as e:
            print('Error:', e)
            return
        
        return res
