# -*- coding: utf-8 -*-
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import sys
import  time
reload(sys)
sys.setdefaultencoding( "utf-8" )

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

class Email():
    def __init__(self):
        self.from_addr =  'mrojxing@163.com'
        self.password = 'ojxing9103123'
        self.smtp_server = 'smtp.163.com'
    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
    def send_email(self,email,msg,name):
        msg = MIMEText('<html><body><h5>+您好，'+name+msg+'+</h5></body></html>', 'html', 'utf-8')
        msg['From'] = _format_addr(u'区家兴 <%s>' % self.from_addr)
        msg['To'] = _format_addr(u'管理员 <%s>' % email)
        msg['Subject'] = Header(u'拍卖信息', 'utf-8').encode()

        server = smtplib.SMTP(self.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr, [email], msg.as_string())
        server.quit()

if __name__ == '__main__':
    entity = Email()
    entity.send_email('584765203@qq.com','嘿嘿嘿','家兴同学')

def main():
    from_addr = 'mrojxing@163.com'
    password = 'ojxing9103123'
    smtp_server = 'smtp.163.com'
    to_addr = 'mrojxing@163.com'
    localtime = time.asctime(time.localtime(time.time()))

    msg = MIMEText('<html><body><h1>+'+localtime+'+</h1></body></html>', 'html', 'utf-8')
    msg['From'] = _format_addr(u'区家兴 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(u'拍卖信息更新提醒！', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

