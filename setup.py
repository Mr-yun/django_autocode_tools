# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django_autocode_tools',
    version='0.0.4',
    description=('Automatic Generation Interface and Database Operation tool based on django'),
    author='yunshao',
    author_email='yunshao1992@gmail.com',
    url='https://github.com/Mr-yun/django_autocode_tools',
    packages =['django_autocode_tools',
	'django_autocode_tools.management',
	'django_autocode_tools.management.commands',
	'django_autocode_tools.wrapper'],
    install_requires=['Django>=1.8','jinja2','djangorestframework'],
    include_package_data = True
)
