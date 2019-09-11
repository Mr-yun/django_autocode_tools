# django_autocode_tools
	django_autocode_tools是一款根据表名自动生成视图、表的基本orm操作、以及序列化操作代码文件,
	同时该工具拥有自定义功能,只要稍微修改,你就打造一款适合你的自动化工具
	tests提供了可以试用样例,可以试用一下。

## 安装方法
	1. pip install django_autocode_tools

## 使用说明
### 基本用法
	1. 将'django_autocode_tools'加到settings.py中的INSTALL_APPS中
		*例 INSTALLED_APPS = (
		  	''''
		    'django.contrib.staticfiles',
		    'django_autocode_tools',
		    '''',
		)
	2. python manage.py auto_code add 操作表名
	3. 在manage.py同级目录下会生成auto_code文件夹
		*例 	├── auto_code
			│   ├── orms
			│   │   └── orm_books.py
			│   ├── sers
			│   │   └── ser_books.py
			│   └── views
			│       └── view_books.py
### 自定义用法
	1. 在django项目中创建一个包,并添加一个zdy.py文件(除zdy.py外,其他文件为非必须)
	  *例 :├── auto_template
			├── oper
			├── orm
			├── ser
			├── view
			└── zdy.py
	2. zdy.py 采用一下模板(默认)
		class Zdy(object):
		    def __init__(self, auto_code):
		        self.auto_code = auto_code
		        self.run()

		    def run(self):
		    	此处填写自定义方法
	3. 将刚才创建的包路径添加到 setting.py中添加AUTO_CODE_TEMPLATES_VIEW配置
		AUTO_CODE_TEMPLATES_VIEW = 'auto_template'
	4. python manage.py auto_code zdy 操作表名
### 命令
	add: 添加视图,表orm,表序列化代码
	refresh: 更新表序列化代码
	remove: 移除视图,表orm,表序列化代码
	zdy: 自定义操作
### 配置
	AUTO_CODE_VIEW_SAVE_PATH = 'mes/dj_views' # 视图.py存放位置
	AUTO_CODE_ORM_SAVE_PATH = 'mes/orms/' # 表orm.py存放位置
	AUTO_CODE_SER_SAVE_PATH = 'mes/orms/serializer' # 表序列化.py存放位置
	AUTO_CODE_TEMPLATES_VIEW = 'auto_template' # 模板以及zdy.py存放位置
