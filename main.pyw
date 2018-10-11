import os
import sys
import json
import time
import shutil
import zipfile
import datetime
import collections

import uuid

import settings

clear_commands = {'win32': 'cls', 'linux': 'clear'}

class NoParamsError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message
        
class DownloadControl():
    def __init__(self, params_dict):
        """Инициализация параметров"""
        if params_dict is None:
            raise NoParamsError('Словарь параметров пуст!')

        self.params_dict = params_dict

        self.WORK_DIR = self.params_dict.get('work_directory', None)
        self.DATA_DIR = self.params_dict.get('data_directory', None)
        self.UNPACKED_ZIP_DIR = self.params_dict.get('unpacked_zip', None)
        self.EXTENSIONS_PATH = self.params_dict.get('extensions_path', None)
        self.LOGGING = self.params_dict.get('logging', False)
        self.CONSOLE_OUT = self.params_dict.get('console_out', False)
        self.LOG_FILE = self.params_dict.get('log_file_path', 'log_file.txt')
        
        self.files_in_work_dir = collections.deque()
        self.directories_in_work_dir = collections.deque()

        if not os.path.exists(self.WORK_DIR):
            os.mkdir(self.WORK_DIR)
            
        if not os.path.exists(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

        self.lmb_is_file = lambda file: os.path.isfile(os.path.join(self.WORK_DIR, file))
        self.lmb_is_dir = lambda dir_: os.path.isdir(os.path.join(self.WORK_DIR, dir_))
        self.cut_file_name = lambda s: ''.join(('\n\t', s))

        self.universal_print("Старт программы. Инициализация параметров завершена успешно. \nВыполнение...")

        self.update_work_dir_data()
        self.group_files()

    def update_work_dir_data(self):
        """Инициализация и обновление списков файлов и папок.
        Функция получает список файлов и папок в директории и 
        производит разбиение на файлы и папки для дальнейшей обработки."""
        data = os.listdir(self.WORK_DIR)
        self.files_in_work_dir.extend(list(filter(self.lmb_is_file, data)))
        self.directories_in_work_dir.extend(list(filter(self.lmb_is_dir, data)))
        time.sleep(1)
        if len(self.files_in_work_dir) > 0:
            self.universal_print("Список файлов: ", *tuple(map(self.cut_file_name, list(self.files_in_work_dir))), '\n')

    def group_files(self):
        while len(self.files_in_work_dir) > 0:
            try:
                file = self.files_in_work_dir.pop()
                self.universal_print("Группировка файла:", file)
                devided = file.split('.')
                file_name = ''.join(devided[0:-1])
                file_extension = devided[-1]
                path_for_file = self.EXTENSIONS_PATH.get(file_extension.lower(), self.DATA_DIR)
                os.makedirs(path_for_file, exist_ok=True)
                from_ = os.path.join(self.WORK_DIR, file)
                to = os.path.join(path_for_file, file)

                # является ли файл zip-архивом, если да - разархивируем
                if zipfile.is_zipfile(from_):
                    destination_zip = os.path.join(self.UNPACKED_ZIP_DIR, file_name)
                    os.makedirs(destination_zip, exist_ok=True)
                    zf = zipfile.ZipFile(from_)
                    zf.extractall(destination_zip)
                    zf.close()

                while os.path.exists(to):
                    new_file_name = ''.join((file_name, '-', str(uuid.uuid4()), '.', file_extension))
                    to = os.path.join(path_for_file, new_file_name)

                response = shutil.copy(from_, to)
                if response == to:
                    os.remove(from_)

            except Exception as e:
               self.universal_print("Вызвано исключение ", str(e.__class__), "в функции group_files(self)")

    def universal_print(self, *args, **kwargs):
        """Функция выводит информацию в консоль и производит запись в log-файл.
            В конструкторе класса определены следующие константы:
            LOGGING - разрешает или запрещает логирование в файл.
            CONSOLE_OUT - разрешает или запрещает вывод в файл.
            LOG_FILE - задаёт путь к log-файлу."""
        message = ' '.join((str(datetime.datetime.now()).split('.')[0], *args))
        if self.LOGGING: 
            with open(self.LOG_FILE, 'a', encoding='utf-8') as log:
                print(message, file=log, **kwargs)
        if self.CONSOLE_OUT:
            print(message, **kwargs)

                     
def main():
    config = settings.Settings(os.path.join('config', 'config.json'))
    control = DownloadControl(config.configurational_dict)

    while KeyboardInterrupt:
        control.update_work_dir_data()
        if len(control.files_in_work_dir) > 0:
            control.group_files()
        time.sleep(1)
        #os.system(clear_commands.get(sys.platform, ''))

if __name__ == '__main__':
    main()
