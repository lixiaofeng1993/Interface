import os
import smtplib
import time
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.logger import Log
from common.HTMLTestRunnerImg import HTMLTestRunner
from common import readConfig

now = time.strftime('%Y-%m-%d %H-%M-%S')


def add_case(case_path):
    """加载所有的测试用例"""
    testUnit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test*.py', top_level_dir=None)  # 定义discover方法的参数
    Log().info('测试用例：%s' % discover)
    # discover方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testUnit.addTests(test_case)
    return testUnit


def run_case(all_case, report_path):
    """执行所有测试用例，并把结果写入报告"""
    report_abspath = os.path.join(report_path, now + 'report.html')
    fp = open(report_abspath, 'wb')
    runner = HTMLTestRunner(stream=fp, verbosity=2, title=readConfig.title, description='用例执行情况：')
    runner.run(all_case)  # 调用add_case函数返回值
    Log().info('执行用例，生成HTML报告!')


def get_new_report_html(report_path_html):
    """获取最新的测试报告"""
    lists = os.listdir(report_path_html)
    for file_name in lists:
        if os.path.splitext(file_name)[1] == '.html':
            continue
        else:
            lists.remove(file_name)
    lists.sort(key=lambda a: os.path.getmtime(os.path.join(report_path_html, a)))
    Log().info('最新的测试报告是：%s' % lists[-1])
    report_file_html = os.path.join(report_path_html, lists[-1])  # 找到最新的测试报告文件
    return report_file_html


def get_new_report_excel(report_path_excel):
    """获取最新的测试报告"""
    lists = os.listdir(report_path_excel)
    for file_name in lists:
        if os.path.splitext(file_name)[1] == '.xlsx':
            continue
        else:
            lists.remove(file_name)
    lists.sort(key=lambda a: os.path.getmtime(os.path.join(report_path_excel, a)))
    Log().info('最新的测试报告是：%s' % lists[-1])
    report_file_excel = os.path.join(report_path_excel, lists[-1])  # 找到最新的测试报告文件
    return report_file_excel


def send_email(user, pwd, user_163, pwd_163, _to, smtp_service, smtp_service_163, report_file_list):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['Subject'] = readConfig.title
    msg['from'] = user
    msg['to'] = ';'.join(_to)  # 支持多个收件人
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    # 邮件正文
    # part = MIMEText('使用Jenkins第一次自动化测试报告尝试 定时 发送邮件')
    for report_file in report_file_list:
        if os.path.splitext(report_file)[1] == '.html':
            with open(report_file, 'rb') as f:
                mail_body = f.read()
            body = MIMEText(mail_body, 'html', 'utf-8')
            msg.attach(body)
            Log().info('写入邮件正文')
        att = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')  # 添加多个附件
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = 'attach;filename=' + report_file[-11:]
        msg.attach(att)
    Log().info('添加邮件附件')
    try:
        try:
            s = smtplib.SMTP()
            s.connect(smtp_service_163)
            s.login(user_163, pwd_163)
            s.sendmail(user_163, _to, msg.as_string())
            s.quit()
            Log().info('%s账号邮件发送成功！请通知相关人员查收。\n' % user_163)
        except:
            s = smtplib.SMTP_SSL(smtp_service)
            s.login(user, pwd)
            s.sendmail(user, _to, msg.as_string())
            s.quit()
            Log().info('%s账号邮件发送成功！请通知相关人员查收。\n' % user)
    except smtplib.SMTPException as e:
        Log().info('邮件发送失败的原因是：%s \n' % e)


def run_email():
    report_file_list = []
    # 测试用例路径，匹配规则
    # case_path = os.path.abspath(os.path.dirname(__file__)) + '/case'
    case_path = os.path.abspath(os.path.dirname(__file__)) + '\\case'
    all_case = add_case(case_path)
    # 生成报告测试路径
    # report_path = os.path.abspath(os.path.dirname(__file__)) + '/report'
    report_path = os.path.abspath(os.path.dirname(__file__)) + '\\report'
    run_case(all_case, report_path)
    # 获取最新的测试报告
    # report_file_html = get_new_report_html(report_path)
    # report_file_excel = get_new_report_excel(report_path)
    # report_file_list.append(report_file_html)
    # report_file_list.append(report_file_excel)
    # user = readConfig.user
    # # qq邮箱授权码
    # pwd = readConfig.pwd
    # user_163 = readConfig.user_163
    # # 163邮箱授权码
    # pwd_163 = readConfig.pwd_163
    # # _to = ['1977907603@qq.com', 'liyongfeng@tzx.com.cn']
    # _to = readConfig.to
    # smtp_service = readConfig.smtp_service
    # smtp_service_163 = readConfig.smtp_service_163
    # send_email(user, pwd, user_163, pwd_163, _to, smtp_service, smtp_service_163, report_file_list)


if __name__ == '__main__':
    run_email()
