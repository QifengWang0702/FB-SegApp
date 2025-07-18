# -*- coding: UTF-8 -*-
import logging
import time
import traceback
import os
from logging.handlers import TimedRotatingFileHandler
import inspect


class Logger:
    def __init__(self, log_path):
        self.logger = logging.getLogger(__name__)
        self.log_path = log_path
        os.makedirs(log_path, exist_ok=True)

        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO,
                                format='[%(levelname)s] %(asctime)s - %(name)s - [line:%(lineno)d] - %(levelname)s - '
                                       '%(message)s')
            # 控制台日志
            # console_handler = logging.StreamHandler(sys.stdout)
            log_formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s - [line:%(lineno)d] - %('
                                              'levelname)s - %(message)s')
            # console_handler.setFormatter(log_formatter)
            # info日志文件名
            info_file_name = 'info-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
            # info日志处理器
            # filename：日志文件名
            # when：日志文件按什么维度切分。'S'-秒；'M'-分钟；'H'-小时；'D'-天；'W'-周
            #       这里需要注意，如果选择 D-天，那么这个不是严格意义上的'天'，而是从你
            #       项目启动开始，过了24小时，才会从新创建一个新的日志文件，
            #       如果项目重启，这个时间就会重置。所以这里选择'MIDNIGHT'-是指过了午夜
            #       12点，就会创建新的日志。
            # interval：是指等待多少个单位 when 的时间后，Logger会自动重建文件。
            # backupCount：是保留日志个数。默认的0是不会自动删除掉日志。
            info_handler = TimedRotatingFileHandler(filename=os.path.join(self.log_path, info_file_name),
                                                    when='MIDNIGHT',
                                                    interval=1,
                                                    backupCount=7,
                                                    encoding='utf-8')
            info_handler.setFormatter(log_formatter)
            info_handler.setLevel(logging.INFO)
            # error日志文件名
            error_file_name = 'error-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
            # 错误日志处理器
            err_handler = TimedRotatingFileHandler(filename=os.path.join(self.log_path, error_file_name),
                                                   when='MIDNIGHT',
                                                   interval=1,
                                                   backupCount=7,
                                                   encoding='utf-8')
            err_handler.setFormatter(log_formatter)
            err_handler.setLevel(logging.ERROR)
            # 添加日志处理器
            self.logger.addHandler(info_handler)
            self.logger.addHandler(err_handler)
            # self.logger.addHandler(console_handler)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.logger = logging.getLogger(func.__name__)
            start = time.time()
            # 获取调用栈第二层的信息
            caller = inspect.stack()[1]
            line = caller.lineno
            try:
                self.logger.info(f"[line:{line}] Enter {func.__name__}")
                result = func(*args, **kwargs)
            except Exception as e:
                end = time.time()
                self.logger.error(f"[line:{line}] Exit {func.__name__} with exception. Time: {end - start}")
                self.logger.error(traceback.format_exc())
                raise
            else:
                end = time.time()
                self.logger.info(f"[line:{line}] Exit {func.__name__}. Time: {end - start}")
                return result

        return wrapper

    def info(self, *args):
        return self.logger.info(*args)

    def debug(self, *args):
        return self.logger.debug(*args)

    def error(self, *args):
        return self.logger.error(*args)


logger = Logger('log')
