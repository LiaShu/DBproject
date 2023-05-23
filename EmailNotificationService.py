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

    def get_contacts(self):
        contact = app_tasks.get_table(['login', 'email'], 'users')
        s = smtplib.SMTP_SSL(host='smtp.mail.ru', port=465)
        s.login(self.__MY_ADDRESS, self.__PASSWORD)
        dict_cont = {}
        for i in contact:
            dict_cont[i[0]] = i[1]
        for key, value in dict_cont.items():
            email=value
            name = key
            msg = MIMEMultipart()
            msg['From'] = self.__MY_ADDRESS
            msg['To'] = email
            msg['Subject'] = "This is TEST"
            message = f'Dear {name}! This is test letter for you. Regards'
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
            del msg
            s.quit()