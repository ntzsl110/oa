import os
import datetime
import traceback
from time import sleep

from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq

from utils.brower import Brower
from utils.tools import file_counts
from utils.log import logger
from settings import conf

downloads = os.path.abspath(conf.oa.email.download_path)  # 下载目录


class Oa_email():

    def __init__(self):
        """打开浏览器，用默认工号登陆
        """

        logger.info('打开浏览器，登陆OA。')

        self.brower = Brower(conf.oa.url, conf.brower.driver, downloads)  # 实例化
        self.brower.send_keys((By.ID, 'userAccount'),
                              conf.oa.login_number)  # OA登陆工号
        self.brower.send_keys((By.ID, 'userPassword'),
                              conf.oa.login_password)  # OA登陆密码
        self.brower.click((By.ID, 'mysubmit'))  # 登陆OA

        self.brower.click((By.ID, 'menu_hidden_dd_a'), 100)  # 点击更多链接
        self.brower.click((By.ID, 'menu_innermail'))  # 点击邮件链接
        self.brower.move_to_element((By.ID, 'dd_menu_null'))  # 移动鼠标移除遮罩
        self.brower.driver.switch_to.frame(self.frame())  # 切换到emailFrame

    def frame(self):
        """根据邮件主体框架
        """
        return self.brower.find_element((By.ID, 'mainFrame'),
                                        100)  # 查找mainFrame

    def search(self,
               search_name='',
               start_date=str(datetime.date.today()),
               end_date=str(datetime.date.today())):
        """查找邮件

        Args:
            search_name (str, optional): 发件人. Defaults to ''.
            start_date (str, optional): 起始日期. Defaults to str(datetime.date.today()).
            end_date (str, optional): 结束日期. Defaults to str(datetime.date.today()).
        """

        if search_name:
            self.brower.send_keys((By.ID, 'searchuser'), search_name)  # 发件人
        if start_date:
            self.brower.send_keys((By.ID, 'searchsendtime_s'),
                                  start_date)  # 发送起始时间
        if end_date:
            self.brower.send_keys((By.ID, 'searchsendtime_e'),
                                  end_date)  # 发送结束时间
        self.brower.click((By.CSS_SELECTOR, "input[value='立即查找']"))  # 立即查找邮件
        sleep(10)  # 必要，否则无法读取到邮件列表

    def list(self):
        """获取邮件列表

        Returns:
            list: []
        """
        itemContainer = self.brower.find_element((By.ID, 'itemContainer'))
        html = itemContainer.get_attribute('innerHTML')
        doc = pq(html)

        emails = []
        table = doc('tr').items()
        for tr in table:
            d = {}
            for td in tr('td').items():
                cls = td.attr('class')
                if cls == 'mailuserid':
                    d['mailuserid'] = td('input').attr('mailuserid')  # 选择框内ID
                if cls == 'notRead':
                    d['notRead'] = td('img').attr('title')  # 状态:已读、未读
                if cls == 'mailpostername':
                    d['mailpostername'] = td.text()  # 发件人姓名
                if cls == 'mailsubject':
                    d['mailsubject'] = bool(td('img'))  # 是否含有附件
                    d['title'] = td('a').text()  # 邮件主题、标题
                    d['onclick'] = td('a').attr('onclick')  # 点击函数
                if cls == 'mailposttime':
                    d['mailposttime'] = td.text()  # 邮件发送时间
            if d:
                emails.append(d)
        return emails

    def download(self, emails, read=['已读邮件', '未读邮件']):
        """下载指定邮件附件

        Args:
            emails (list): list
            read (list): ['已读邮件','未读邮件']
        """

        x = 0  # 统计已下载附件个数
        main_handle = self.brower.driver.current_window_handle  # 当前主窗口句柄

        for email in emails:
            if email['notRead'] in read and email['mailsubject']:
                link = f"//input[@mailuserid={email['mailuserid']}]/../../td[@class='mailsubject']/a"
                link_exist = self.brower.element_is_exist((By.XPATH, link))
                if link_exist:
                    self.brower.execute_script((By.XPATH, link),
                                               email['onclick'])  # 点击邮件主题

                new_handle = [
                    handle for handle in self.brower.driver.window_handles
                    if handle != main_handle
                ]  # 判断是否打开新的窗口--邮件详情

                if new_handle:
                    self.brower.driver.switch_to.window(
                        new_handle[0])  # 跳转到新窗口

                    if self.brower.element_is_exist(
                        (By.XPATH,
                         "//td[@id='file_name']/a")):  # 通过td/a判断是否存在附件链接

                        doc = pq(self.brower.driver.page_source)  # 获取网页html
                        links = doc('#file_name a').items()  # 附件列表
                        fs = file_counts(downloads)  # 下载目录文件数

                        for link in links:
                            x += 1
                            logger.info(f'开始下载附件 ——> {x}. {link.text()}')

                            self.brower.execute_script(
                                (By.LINK_TEXT, link.text()),
                                link.attr('onclick'))  # 点击附件链接
                            while file_counts(
                                    downloads) > fs:  # 循环休眠1秒，直到文件下载完成
                                sleep(1)
                            fs += 1
                            sleep(5)  # 必要，否则有可能无法继续到下一个链接

                    self.brower.driver.close()  # 关闭当前窗口
                    self.brower.driver.switch_to.window(main_handle)  # 切换到主窗口
                    self.brower.driver.switch_to.frame(
                        self.frame())  # 切换到emailframe


if __name__ == '__main__':  # 郭轶 姚智
    try:
        oa_email = Oa_email()
        oa_email.search('郭轶', '2022-1-1')
        emails = oa_email.list()
        oa_email.download(emails)
    except Exception:
        logger.error(traceback.format_exc())
    else:
        oa_email.brower.driver.quit()
    finally:
        logger.info('退出OA，关闭浏览器。')
