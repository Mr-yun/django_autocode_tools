# -*- coding:utf-8 -*-
from __future__ import print_function

from os import path, getcwd


class Settings():
    def __init__(self, settings):
        self.AUTO_CODE_ROOT_APP = getattr(settings, 'AUTO_CODE_ROOT_APP', None)
        self.AUTO_CODE_TEMPLATES_VIEW = getattr(settings, 'AUTO_CODE_TEMPLATES_VIEW',
                                                path.join(path.abspath(path.dirname(__file__)), 'templates'))
        self.AUTO_CODE_VIEW_SAVE_PATH = getattr(settings, 'AUTO_CODE_VIEW_SAVE_PATH',
                                                path.join(getcwd(), 'auto_code/views'))
        self.AUTO_CODE_ORM_SAVE_PATH = getattr(settings, 'AUTO_CODE_ORM_SAVE_PATH',
                                               path.join(getcwd(), 'auto_code/orms'))
        self.AUTO_CODE_SER_SAVE_PATH = getattr(settings, 'AUTO_CODE_SER_SAVE_PATH',
                                               path.join(getcwd(), 'auto_code/sers'))
