# -*- coding: utf-8 -*-
from email import encoders
import os
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# 中文处理
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(to_addr_in, filepath_in, content):
    # 邮件发送和接收人配置
    from_addr = 'zhanljscarever@163.com'
    smtp_server = 'smtp.163.com'
    password = 'zlj941020'  # 这是你邮箱的第三方授权客户端密码，并非你的登录密码
    to_addr = to_addr_in
    to_addrs = to_addr.split(',')

    msg = MIMEMultipart()
    msg['From'] = _format_addr('来自呱叽网 <%s>' % from_addr)  # 显示的发件人
    # msg['To'] = _format_addr('管理员 <%s>' % to_addr)                # 单个显示的收件人
    msg['To'] = ",".join(to_addrs)  # 多个显示的收件人
    msg['Subject'] = Header(str(content), 'utf-8').encode()  # 显示的邮件标题

    # 需要传入的路径
    # filepath = r'D:\test'
    filepath = filepath_in
    r = os.path.exists(filepath)
    if r is False:
        msg.attach(MIMEText('no file...', 'plain', 'utf-8'))
    else:
        # 邮件正文是MIMEText:
        msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
        # 遍历指定目录，显示目录下的所有文件名
        pathDir = os.listdir(filepath)
        # for allDir in pathDir:
        #     child = os.path.join(filepath, allDir)
        #
        #     child.decode('gbk')  # .decode('gbk')是解决中文显示乱码问题
        #
        #     # 添加附件就是加上一个MIMEBase，从本地读取一个文件
        #     with open(child, 'rb') as f:
        #         # 设置附件的MIME和文件名，这里是txt类型:
        #         mime = MIMEBase('file', 'xls', filename=allDir)
        #         # 加上必要的头信息:
        #         mime.add_header('Content-Disposition', 'attachment', filename=allDir)
        #         mime.add_header('Content-ID', '<0>')
        #         mime.add_header('X-Attachment-Id', '0')
        #         # 把附件的内容读进来:
        #         mime.set_payload(f.read())
        #         # 用Base64编码:
        #         encoders.encode_base64(mime)
        #         # 添加到MIMEMultipart:
        #         msg.attach(mime)
    try:
        server = smtplib.SMTP(smtp_server, 25)
        # server.starttls()
        server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
        server.login(from_addr, password)
        # print to_addrs
        server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error: unable to send email")
        print(traceback.format_exc())

if __name__ == '__main__':
    send_email('959370553@qq.com,zhanljscarever@163.com', 'D:\\test')