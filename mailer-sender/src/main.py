from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
import os
import time
import datetime
from rethinkdb import RethinkDB



smtp_address = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT', 465)
email_address = os.environ.get('SMTP_USER')
email_password = os.environ.get('SMTP_PASSWORD')

class Sender():
    def __init__(self):
        self.r = None
        self.server = None
        self.queue = []

    def dry_run(self):
        print("db   connection")
        if not self.__get_conn():
            return False, "Error connecting to DB"
        print("db   connection:  ok")
        print("db   data")
        if not self.__get_queue():
            return False, "Error getting queue"
        print("db   data:        ok")
        print("smtp connection")
        if not self.__get_server():
            return False, "Error connecting to SMTP"
        print("smtp connection:  ok")
        print("smtp login")
        if not self.__server_connect():
            return False, "Error logging to SMTP"
        print("smtp login:       ok")
        return True, None

    def run(self):
        if not self.__get_conn():
            return False, "Error connecting to DB"
        while len(self.queue) == 0:
            if not self.__get_queue():
                return False, "Error getting queue"
            time.sleep(0.5)
        if not self.__get_server():
            return False, "Error connecting to SMTP"
        if not self.__server_connect():
            return False, "Error logging to SMTP"
        resume = {"fail": 0, "sent": 0}
        for mail in self.queue:
            self.__update_status(mail, 'auto-try')
            message = self.__format(mail)
            sent = self.__server_send(message)
            if sent:
                self.__update_status(mail, 'sent', True)
                resume['sent'] += 1
            else:
                self.__update_status(mail, 'fail-auto-try', False)
                resume['fail'] += 1
        self.queue = []
        return True, resume

    def __get_conn(self):
        i = 0
        succes = False
        while i < 180:
            try:
                r = RethinkDB()
                r.connect("rethink-mailer", 28015, password="").repl()
                r = r.db("mailer").table("mail")
                r.count().run()
                self.r = r
                succes = True
                break
            except:
                time.sleep(1)
            i += 1
        return succes

    def __get_queue(self):
        self.queue = list(
                        self.r.filter(
                            lambda doc:
                                (doc['sent'] == False) & (doc['retry'] < 5)
                        ).run()
                     )
        print('oooo', self.queue)
        return True

    def __get_server(self):
        i = 0
        succes = False
        while i < 60:
            for context in [ssl.create_default_context, ssl._create_unverified_context]:
                try:
                    self.server =  smtplib.SMTP_SSL(smtp_address, smtp_port, context=context())
                    succes = True
                    break
                except:
                    pass
            if succes is True:
                break
            time.sleep(1)
            i += 1
        return succes

    def __server_connect(self):
        i = 0
        succes = False
        while i < 60:
            try:
                self.server.login(email_address, email_password)
                succes = True
            except:
                time.sleep(1)
            i += 1
        return succes

    def __update_status(self, mail, event, succes = None):
        now = str(datetime.datetime.utcnow())
        data = {
            "status": mail['status'] + [{'event': event, 'date': now}],
            "last_update": now
        }
        if succes is True:
            data['sent'] = True
        if succes is False:
            data['sent'] = False
            data['retry'] = mail['retry'] + 1
        self.r.get(mail['id']).update(data).run()
        return True

    def __format(self, mail):
        message = MIMEMultipart("alternative")
        message["From"] = email_address
        message["To"] = mail['to']
        message["Subject"] = mail['subject']
        message.attach(
                MIMEText(
                    mail['html'],
                    'html'
                )
        )
        return message

    def __server_send(self, message):
        succes = False
        try:
            res = self.server.sendmail(email_address, message["To"], message.as_string())
            succes = True
        except smtplib.SMTPRecipientsRefused:
            pass
        return succes

if __name__ == '__main__':
    sender = Sender()
    d, dry_run = sender.dry_run()
    if not d:
        print(dry_run)
    while True:
        succes, data = sender.run()
        msg = 'SUCCES' if succes else 'ERROR'
        print(f"[{msg}]: {data}")
        time.sleep(1)
