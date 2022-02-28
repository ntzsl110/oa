import logging
import logging.handlers
import os
import time

# log_path是存放日志的路径
log_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '.././logs'))

# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 修改log保存位置
timestamp = time.strftime("%Y-%m-%d", time.localtime())
logfile_name = '%s.log' % timestamp
logfile_path = os.path.join(log_path, logfile_name)


class Logger(logging.Logger):

    def __init__(self, name, level='DEBUG', file=None, encoding='utf-8'):
        super().__init__(name)
        self.encoding = encoding
        self.file = file
        self.level = level

        # 日志输出格式
        # # [2019-05-15 14:48:52,947] - test.py] - ERROR: this is error
        formatter = logging.Formatter(
            '[%(asctime)s] [%(filename)s] [%(levelname)s]: %(message)s')

        # 创建一个FileHandler，用于写到本地
        rotatingFileHandler = logging.handlers.RotatingFileHandler(
            filename=logfile_path, maxBytes=1024 * 1024 * 50, backupCount=5)
        rotatingFileHandler.setFormatter(formatter)
        rotatingFileHandler.setLevel(logging.DEBUG)
        self.addHandler(rotatingFileHandler)

        # 创建一个StreamHandler,用于输出到控制台
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)

        self.addHandler(console)
        self.setLevel(logging.DEBUG)


logger = Logger(name=logfile_path, file=logfile_path)

if __name__ == '__main__':
    logger.info("this is info")
    logger.debug("this is debug")
    logger.error("this is error")
    logger.warning("this is warning")
    logger.critical("critical")
