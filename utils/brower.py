import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.edge.service import Service


class Brower():

    def __init__(self, url, driver, downloads, headless=False):
        """初始化

        Args:
            url (string): 需要打开的网址
            downloads (string, optional): 下载文件夹
            headless (bool, optional): 是否显示窗口. Defaults to False
        """
        self.driver_path = os.path.abspath(driver)  # 驱动目录
        self.url = url
        self.downloads = downloads
        self.headless = headless
        self.driver = self.open()

    def open(self):
        """打开浏览器

        Returns:
            _type_: 返回driver
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.downloads:
            prefs = {
                'profile.default_content_settings.popups': 0,
                'download.default_directory': self.downloads,
                "profile.default_content_setting_values.automatic_downloads": 1
            }
            options.add_experimental_option('prefs', prefs)
        if self.headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(self.driver_path),
                                  options=options)
        driver.maximize_window()
        driver.get(self.url)
        return driver

    def find_element(self, locator, timeout=20):
        """查找单个元素

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
            timeout (int, optional): 最长超时时间. Defaults to 20.
        """
        element = WebDriverWait(self.driver, timeout,
                                0.5).until(lambda x: x.find_element(*locator))
        return element

    def find_elements(self, locator, timeout=20):
        """查找多个元素

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
            timeout (int, optional): 最长超时时间. Defaults to 20.
        """
        elements = WebDriverWait(
            self.driver, timeout,
            0.5).until(lambda x: x.find_elements(*locator))
        return elements

    def element_is_exist(self, locator, timeout=20):
        """判断元素是否存在,存在了返回True,不存在就返回False

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
            timeout (int, optional): 最长超时时间. Defaults to 20.
        """
        try:
            WebDriverWait(self.driver, timeout,
                          1).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def send_keys(self, locator, text, timeout=20):
        """封装一个send_keys

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
            text (string): 按键
        """
        self.find_element(locator, timeout).send_keys(text)

    def click(self, locator, timeout=20):
        """封装一个click

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
        """
        self.find_element(locator, timeout).click()

    def execute_script(self, locator, text="arguments[0].click();"):
        """封装一个click

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
            text (string): javascript
        """
        self.driver.execute_script(text, self.find_element(locator))

    def move_to_element(self, locator):
        """移动鼠标到某个元素

        Args:
            locator (tuple): 定位方式，如(By.ID, 'searchuser')
        """
        ActionChains(self.driver).move_to_element(
            self.find_element(locator)).perform()


if __name__ == '__main__':
    pass
