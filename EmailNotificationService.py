import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app_tasks import app_tasks

class EmailService():

    # MY_ADDRESS = 'flyletter23@gmail.com'
    __MY_ADDRESS = 'newsletter2023@mail.ru'
    __PASSWORD = 'BKkYqNjU0crxmVEWBuxq'
    # PASSWORD = 'MyPassowrd999**'
    def __init__(self, connect):
        self.connect = connect

    def email_notif(self, dict_inf):
        s = smtplib.SMTP_SSL(host='smtp.mail.ru', port=465)
        s.login(self.__MY_ADDRESS, self.__PASSWORD)
        for k, v in dict_inf.items():
            email = k
            task = v
            msg = MIMEMultipart()
            msg['From'] = self.__MY_ADDRESS
            msg['To'] = email
            msg['Subject'] = "This is TEST"
            message = f'Dear user! This is your task today: {task}. Regards'
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
            del msg
        s.quit()

