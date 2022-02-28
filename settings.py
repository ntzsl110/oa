from conf.config import settings
import os

os.environ['ENV_FOR_DYNACONF'] = 'development'

conf = settings

if __name__ == '__main__':
    print(conf.oa.url)
