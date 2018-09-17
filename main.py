import os
import sys
import threading
import shutil
import json
import time
import zipfile
import collections

import colorama
import progressbar
import pyautogui

import settings

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
        print("Обновление...")
        data = os.listdir(self.work_dir)
        self.files_in_work_dir.extend(list(filter(self.lmb_is_file, data)))
        self.directories_in_work_dir.extend(list(filter(self.lmb_is_dir, data)))
        time.sleep(1)
        print("Обновление данных завершёно.")

    def group_files(self):
        while len(self.files_in_work_dir) > 0:
            try:
                print("Группировка...")
                file = self.files_in_work_dir.pop()
                file_extension = file.split('.')[-1]
                path_for_file = self.extensions_path.get(file_extension.lower(), self.data_dir)
                os.makedirs(path_for_file, exist_ok=True)
                from_ = os.path.join(self.work_dir, file)
                to = os.path.join(path_for_file, file)
                response = shutil.copy(from_, to)
                if response == to:
                    os.remove(from_)
            except Exception as e:
                print("Вызвано исключение: ", e.__class__)
            
                
def main():
    config = settings.Settings(os.path.join('config', 'config.json'))
    control = DownloadControl(config.configurational_dict)

    while KeyboardInterrupt:
        control.update_work_dir_data()
        if len(control.files_in_work_dir) > 0:
            control.group_files()
        print('<->' * 20)
        time.sleep(1)


if __name__ == '__main__':
    main()
