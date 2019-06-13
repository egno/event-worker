from dotenv import load_dotenv
import os
import requests


class SMSGateway(object):

    def __init__(self):
        self.phone = None
        self.text = None
        self.businessId = None
        self.recordId = None
        self.time= None
        self.gateway=None
        self.site=None
        self.loadEnv()

    def loadEnv(self):
        load_dotenv()
        self.gateway = os.getenv("SMS_GATEWAY_URL")
        self.site = os.getenv("SITE")

    def checkParam(self):
        return (self.phone is not None) and (self.text is not None)

    def send(self):
        if not self.checkParam():
            print('No data:', self)
            return
        params = {'business_id': self.businessId,
                  'record_id': self.recordId, 'phone': self.phone, 'text': self.text}
        if self.time is not None:
            params['time'] = self.time
        try:
            res = requests.get(self.gateway, params=params)
            print('GW Send:', res.url)
            return res
        except requests.exceptions.ConnectionError as e:
            print('Error:', e)
            return

        return
