#-*- encoding: utf8 -*-
import os
import sys
import logging


logging.getLogger("requests.packages.urllib3").propagate = 0


class MyLogger(logging.Logger):
    def __init__(self,
                 name=None,
                 level=logging.INFO,
                 fmt=None,
                 datefmt=None,
                 logfile=None,
                 filemode='w',
                 stream=sys.stderr,
                 verbose=True,
                 colored=False,
                 **kwargs):

        if verbose:
            level = logging.DEBUG

        super(MyLogger, self).__init__(name, level)

        self.fmt = fmt or '[%(asctime)s %(funcName)s %(levelname)s] %(message)s'
        self.datefmt = datefmt or '%Y-%m-%d %H:%M:%S'
        self.formatter = logging.Formatter(self.fmt, self.datefmt)

        if logfile:
            self._addFilehandler(logfile, filemode)
        else:
            self._addStreamHandler(stream)
            if colored:
                import coloredlogs
                coloredlogs.install(fmt=self.fmt, level=level, logger=self)

    def _addFilehandler(self, filename, filemode):

        file_hdlr = logging.FileHandler(filename, filemode)
        file_hdlr.setFormatter(self.formatter)
        self.addHandler(file_hdlr)

    def _addStreamHandler(self, stream):

        stream_hdlr = logging.StreamHandler(stream)
        stream_hdlr.setFormatter(self.formatter)
        self.addHandler(stream_hdlr)


if __name__ == '__main__':

    # logger = MyLogger(colored=False)
    logger = MyLogger(name='TEST1')
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')

    logger2 = MyLogger(name='TEST2', colored=False, logfile='out.log')
    logger2.warn('warn message')
    logger2.warn('warn message')
