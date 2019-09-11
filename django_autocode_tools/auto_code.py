# -*- coding:utf-8 -*-
from imp import load_source
from os import path, getcwd, makedirs, remove as file_remove

from django.conf import settings
from django_autocode_tools.app_settings import Settings
from jinja2 import FileSystemLoader, Environment


class AutoCode(object):
    def __find_oper_table(self):
        '''根据APP列表(倒叙)，自动查找操作的表'''
        attribute = []
        for z in settings.INSTALLED_APPS[::-1]:
            self.app = z
            attribute = self.get_attribute()

            if len(attribute) > 0:
                break
        return attribute

    def __check_folder(self):

        for dir_path in [self.settings.AUTO_CODE_VIEW_SAVE_PATH,
                         self.settings.AUTO_CODE_ORM_SAVE_PATH,
                         self.settings.AUTO_CODE_SER_SAVE_PATH]:
            if not path.exists(dir_path):
                makedirs(dir_path)

    def __init__(self, **options):
        self.view_name = options.get('jobhash')
        self.file_name = self.view_name.lower()

        self.old_template_path = path.join(path.abspath(path.dirname(__file__)), 'templates')
        self.settings = Settings(settings)
        self.base_dir = getcwd()

        if self.settings.AUTO_CODE_ROOT_APP is None:
            self.attribute = self.__find_oper_table()
        else:
            self.app = self.settings.AUTO_CODE_ROOT_APP
            self.attribute = self.get_attribute()

    def get_attribute(self):
        begin_bit = False
        attribute = []
        app_path = path.join(self.base_dir, self.app)
        models_path = path.join(app_path, 'models.py')
        if path.exists(models_path):
            module_models = __import__(self.app + '.models', self.app)
            cls_table = getattr(module_models.models, self.view_name, None)
            if cls_table is not None:
                with open(models_path, 'r') as f:
                    for line in f:
                        if line.strip().startswith('#'):
                            continue
                        else:
                            if line.startswith("class {0}(models.Model)".format(self.view_name)):
                                begin_bit = True
                                continue
                            if 'class' in line:
                                begin_bit = False
                            if begin_bit and not line.startswith('#'):
                                if '=' in line:
                                    attribute.append({
                                        'value': line.split('=')[0].strip(),
                                        'ForeignKey': False,
                                        'null': False
                                    })
                                if 'ForeignKey' in line:
                                    attribute[-1]['ForeignKey'] = True

                                if 'null' in line:
                                    attribute[-1]['null'] = True
                if getattr(cls_table, '_meta', None):
                    self.file_name = getattr(getattr(cls_table, '_meta', None), 'db_table', None)
            else:
                pass
        else:
            pass

        return attribute

    def __get_templates(self, filename):
        if path.exists(path.join(self.settings.AUTO_CODE_TEMPLATES_VIEW, filename)):
            templateLoader = FileSystemLoader(self.settings.AUTO_CODE_TEMPLATES_VIEW)
            env = Environment(loader=templateLoader)
        else:
            templateLoader = FileSystemLoader(self.old_template_path)
            env = Environment(loader=templateLoader)

        return env.get_template(filename)

    def add(self):
        self.__check_folder()

        self.__create_view()
        self.__ceare_orm()
        self.__create_ser()

    def refresh(self):
        self.__create_ser()

    def remove(self):
        for files in [
            path.join(self.settings.AUTO_CODE_VIEW_SAVE_PATH, 'view_{}.py'.format(self.file_name)),
            path.join(self.settings.AUTO_CODE_ORM_SAVE_PATH, 'orm_{}.py'.format(self.file_name)),
            path.join(self.settings.AUTO_CODE_SER_SAVE_PATH, 'ser_{}.py'.format(self.file_name)),

        ]:

            if path.exists(files):
                file_remove(files)

    def __create_view(self):
        template = self.__get_templates('view')

        with open(path.join(self.settings.AUTO_CODE_VIEW_SAVE_PATH,
                            'view_{}.py'.format(self.file_name)),
                  'w') as f:
            f.write(template.render(view_name=self.view_name, file_name=self.file_name))

    def __ceare_orm(self):
        template = self.__get_templates('orm')
        str_template = template.render(app=self.app, view_name=self.view_name, file_name=self.file_name)
        str_create = '''
def create_{1}(req):
    return {0}.objects.create({2})
        '''

        str_select = '''
def select_{1}_{2}(obj_{2}):
    return {0}.objects.filter({2}=obj_{2})
        '''
        template_create = ''

        for i in self.attribute:
            if not i['null']:
                template_create += "{0}=req['{0}'],".format(i['value'])
            if i['ForeignKey']:
                str_template += '\n\n' + str_select.format(self.view_name, self.file_name, i['value'])
        str_template += '\n\n' + str_create.format(self.view_name, self.file_name, template_create)

        with open(path.join(self.settings.AUTO_CODE_ORM_SAVE_PATH, 'orm_{}.py'.format(self.file_name)), 'w') as f:
            f.write(str_template)

    def __create_ser(self):
        template = self.__get_templates('ser')
        fields = ""
        for z in filter(lambda x: x['ForeignKey'] == False, self.attribute):
            fields += "'{}',".format(z['value'])

        update = ''
        for i in self.attribute:
            update += "instance.{0} = validated_data.get('{0}', instance.{0})\n        ".format(i['value'])
        str_template = template.render(app=self.app, view_name=self.view_name, file_name=self.file_name,
                                       fields=fields[:-1], update=update)
        with open(path.join(self.settings.AUTO_CODE_SER_SAVE_PATH, 'ser_{}.py'.format(self.file_name)), 'w') as f:
            f.write(str_template)

    def zdy(self):
        py_file = path.join(self.settings.AUTO_CODE_TEMPLATES_VIEW, 'zdy.py')
        if path.exists(py_file):
            obj_zdy = load_source('auto_zdy', py_file).Zdy(self)
            obj_zdy.run()
        else:
            print('unfind zdy.py files')
