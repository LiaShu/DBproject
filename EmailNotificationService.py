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
            #msg.attach(MIMEText(message, 'plain'))
            html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>НЛМК IIoT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin: 0; padding: 0;">
<table align="center" bgcolor="#c1c6c8" border="0" cellpadding="0" cellspacing="0" width="600">
    <tr>
        <td align="right" background="cid:image1" height="30px" style="padding: 40px 50px 30px 0;">

            <font face="Arial" color="#2c5697" size="4"><b>Fly Lady</b></font>
            <img src="cid:logo" width = "50%">
        </td>
    </tr>
    <tr>
        <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td>
                        <font face="Arial" color="#0092bc"><b>ЦХПП.НТА-1</b></font>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 20px 0 30px 0;">
                        <font face="Arial"><b> Внимание! ${message}!</b><br></font>
                        <br>
                        Теги: ***, ***, ***<br>
                        Время: 31.03.2021 09:00 - 31.03.2021 09:10<br>
                        <br>
                        Отклонение от заданного значения более 15%
                    </td>
                </tr>
                <tr>
                    <td>
                        URL куда-нибудь
                    </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td bgcolor="#ee4c50">
            Row 3
        </td>
    </tr>
</table>
</body>
</html>
            """
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            fp = open('header_logo.jpg', 'rb')
            msg_image = MIMEImage(fp.read())
            fp.close()
            # Define the image's ID as referenced above
            msg_image.add_header('Content-ID', '<image1>')
            msg.attach(msg_image)
            s.send_message(msg)
            del msg
        s.quit()

