import os
import time
import smtplib
import pandas as pd
import yfinance as yf

env_email = os.environ.get('email')
env_password = os.environ.get('password')


class stock_alerts:
    
    def __init__(self, ticker, user_input, email, password):
        self.ticker = ticker
        self.user_input = user_input
        self.email = email
        self.password = password
        self.trigger = None

    def vwap_cross_up(self):
        self.alert_text = 'umn no'
        self.price = pd.DataFrame()
        self.vwap_output = pd.DataFrame()
        self.target = pd.DataFrame()
        self.df = yf.download(self.ticker, period='1d', interval='1m')
        self.df_ = self.df[['High', 'Low', 'Adj Close', 'Volume']]
        self.target['target'] = self.df['Adj Close']
        self.price['hello'] = (self.df['High'] + 
                               self.df['Low'] + 
                               self.df['Adj Close']) / 3
        self.vwap_output['output'] = (self.df['Volume'] * 
                            self.price['hello']) / self.df['Volume']
        if self.target['target'].iloc[-1] > self.vwap_output['output'].iloc[-1]:
            self.trigger = 1
        else:
            pass

    def vwap_cross_down(self):
        self.alert_text = 'testing body of'
        self.price = pd.DataFrame()
        self.vwap_output = pd.DataFrame()
        self.target = pd.DataFrame()
        self.df = yf.download(self.ticker, period='1d', interval='1m')
        self.df_ = self.df[['High', 'Low', 'Adj Close', 'Volume']]
        self.target['target'] = self.df['Adj Close']
        self.price['hello'] = (self.df['High'] + 
                               self.df['Low'] + 
                               self.df['Adj Close']) / 3
        self.vwap_output['output'] = (self.df['Volume'] * 
                            self.price['hello']) / self.df['Volume']
        if self.target['target'].iloc[-1] < self.vwap_output['output'].iloc[-1]:
            self.trigger = 1
        else:
            pass


    def run_email(self):
        with smtplib.SMTP('smtp.gmail.com', 587) as self.smtp:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()

            self.smtp.login(self.email, self.password)

            self.subject = 'alert'
            self.body = self.alert_text

            self.msg = f'Subject: {self.subject}\n\n{self.body}'
            self.smtp.sendmail(self.email, self.email, self.msg)
        print('sent')
        pass

    def run(self):
        while self.trigger == None:
            if self.user_input == 'vwap_cross_up':
                stock_alerts.vwap_cross_up(self)
                if self.trigger != None:
                    break
            elif self.user_input == 'vwap_cross_down':
                stock_alerts.vwap_cross_down(self)
                if self.trigger != None:
                    break
            else:
                pass
            time.sleep(60)
        if self.trigger != None:
            stock_alerts.run_email(self)
        else:
            pass

call = stock_alerts('SPY', 'vwap_cross_down', env_email, env_password)
call.run()