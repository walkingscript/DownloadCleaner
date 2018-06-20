import os
import sys
import threading
import shutil
import json
import time

import colorama
import pyautogui

class DownloadControl():
    count = 0

    def __init__(self, work_dir, data_dir):
        """Инициализация параметров"""
        DownloadControl.count += 1

        self.work_dir = work_dir
        self.data_dir = data_dir

        self.json_config_dir_path = os.path.join(self.work_dir, 'config')
        self.json_config_file_path = os.path.join(self.work_dir, 'config', 'config_{}.json'.format(str(DownloadControl.count)))

        self.files_in_work_dir = []
        self.dirs_in_work_directory = []

        self.lmb_is_file = lambda file: os.path.isfile(os.path.join(self.work_dir, file))
        self.lmb_is_dir = lambda dir: os.path.isdir(os.path.join(self.work_dir, dir))

        self.update_work_dir_data()

    def check_new_files(self, path_to_dir):
        """Функция проверки появления новых файлов в директории."""
        work_dir_items = os.listdir(self.work_dir)
        current_files_in_work_dir = list(filter(self.lmb_is_file, work_dir_items))
        new_files_in_work_dir = [file for file in current_files_in_work_dir if file not in self.files_in_work_dir]
        return new_files_in_work_dir

    def check_new_dirs(self, path_to_dir):
        """Функция проверки появления новых папок в директории."""
        data = os.listdir(self.work_dir)
        current_dirs_in_work_dir = list(filter(self.lmb_is_dir, data))
        new_dirs_in_word_dir = [dir for dir in current_dirs_in_work_dir if dir not in self.dirs_in_work_directory]
        return new_dirs_in_word_dir

    def update_work_dir_data(self):
        """Инициализация и обновление списков файлов и папок"""
        data = os.listdir(self.work_dir)
        self.files_in_work_dir = list(filter(self.lmb_is_file, data))
        self.dirs_in_work_directory = list(filter(self.lmb_is_dir, data))
    
    def save_work_dir_data(self):
        if not os.path.exists(self.json_config_dir_path):
            os.mkdir(self.json_config_dir_path)
        filename = ''
        with open('work_data.json', 'w') as file:
            

def main():
    work_dir_pathes = (r'C:\Users\ocean\Desktop\DownloadManager\nn_rep\test_dir',)
    data_dir_pathes = (r'C:\Users\ocean\Desktop\DownloadManager\nn_rep\data_dir',)
    args = tuple(sys.argv)
    input()

if __name__ == '__main__':
    main()
