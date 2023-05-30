import smtplib
from email.mime.image import MIMEImage
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

    def email_notif(self, email, html_file):
        s = smtplib.SMTP_SSL(host='smtp.mail.ru', port=465)
        s.login(self.__MY_ADDRESS, self.__PASSWORD)
        msg = MIMEMultipart()
        msg['From'] = self.__MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "This is TEST"
        #message = f'Dear user! This is your task today: {task}. Regards'
        #msg.attach(MIMEText(message, 'plain'))
        html = html_file
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        fp = open('header_logo1.jpg', 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        msg_image.add_header('Content-ID', '<image1>')
        msg.attach(msg_image)
        s.send_message(msg)
        del msg
        s.quit()

