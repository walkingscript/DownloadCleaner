import os
import sys
import shutil
import json
import time
import zipfile
import collections

import colorama
import progressbar
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

        self.work_dir = self.params_dict.get('work_directory', None)
        self.data_dir = self.params_dict.get('data_directory', None)
        self.unpacked_zip_dir = self.params_dict.get('unpacked_zip', None)
        self.extensions_path = self.params_dict.get('extensions_path', None)
        
        self.files_in_work_dir = collections.deque()
        self.directories_in_work_dir = collections.deque()

        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
            
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        self.lmb_is_file = lambda file: os.path.isfile(os.path.join(self.work_dir, file))
        self.lmb_is_dir = lambda dir_: os.path.isdir(os.path.join(self.work_dir, dir_))

        self.update_work_dir_data()
        self.group_files()

    def update_work_dir_data(self):
        """Инициализация и обновление списков файлов и папок.
        Функция получает список файлов и папок в директории и 
        производит разбиение на файлы и папки для дальнейшей обработки."""
        print(colorama.Fore.BLUE, colorama.Style.BRIGHT, "Обновление...")
        data = os.listdir(self.work_dir)
        self.files_in_work_dir.extend(list(filter(self.lmb_is_file, data)))
        self.directories_in_work_dir.extend(list(filter(self.lmb_is_dir, data)))
        time.sleep(1)
        print(colorama.Fore.BLUE, colorama.Style.BRIGHT, "Обновление данных завершёно.")

    def group_files(self):
        file_count = len(self.files_in_work_dir)
        pb = progressbar.ProgressBar(min_value=0, max_value=file_count)
        while len(self.files_in_work_dir) > 0:
            #try:
            print(''.join((colorama.Fore.MAGENTA, colorama.Style.BRIGHT, "Группировка...")))
            file = self.files_in_work_dir.pop()
            devided = file.split('.')
            file_name = ''.join(devided[0:-1])
            file_extension = devided[-1]
            path_for_file = self.extensions_path.get(file_extension.lower(), self.data_dir)
            os.makedirs(path_for_file, exist_ok=True)
            from_ = os.path.join(self.work_dir, file)
            to = os.path.join(path_for_file, file)

            # является ли файл zip-архивом, если да - разархивируем
            if zipfile.is_zipfile(from_):
                destination_zip = os.path.join(self.unpacked_zip_dir, file_name)
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
            
            # изменение цвета
            print(colorama.Fore.CYAN, colorama.Style.BRIGHT)
            pb.value += 1
            #except Exception as e:
            #    print(''.join((colorama.Fore.RED, colorama.Style.BRIGHT, "Вызвано исключение: ")), e.__class__)
            
                
def main():
    colorama.init()

    config = settings.Settings(os.path.join('config', 'config.json'))
    control = DownloadControl(config.configurational_dict)

    while KeyboardInterrupt:
        control.update_work_dir_data()
        if len(control.files_in_work_dir) > 0:
            control.group_files()
        print(colorama.Fore.GREEN, '<->' * 20)
        time.sleep(1)
        os.system(clear_commands.get(sys.platform, ''))


if __name__ == '__main__':
    main()
