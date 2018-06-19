import os
import sys
import threading
import shutil
import json
import time

import colorama
import pyautogui

class DownloadControl():
    def __init__(self, path_to_work_dir):
        """Конструктор"""
        self.update_work_dir_data()

    def check_new_files(self, path_to_dir):
        """Функция проверки появления новых файлов в директории."""
        current_files_in_work_directory = list(filter(lambda file: os.path.isfile(os.path.join(path_to_work_dir, file)), os.listdir(path_to_work_dir)))
        new_files_in_work_directory = [file for file in current_files_in_work_directory if file not in self.files_in_work_directory]

    def check_new_dirs(self, path_to_dir):
        """Функция проверки появления новых папок в директории."""
        current_dirs_in_work_directory = list(filter(lambda dir: os.path.isdir(os.path.join(path_to_work_dir, dir)), os.listdir(path_to_work_dir)))
        new_dirs_in_word_directory = [dir for dir in current_dirs_in_work_directory if dir not in self.dirs_in_work_directory]

    def update_work_dir_data(self):
        self.files_in_work_directory = list(filter(lambda file: os.path.isfile(os.path.join(path_to_work_dir, file)), os.listdir(path_to_work_dir)))
        self.dirs_in_work_directory = list(filter(lambda dir: os.path.isdir(os.path.join(path_to_work_dir, dir)), os.listdir(path_to_work_dir)))
    
    def save_work_dir_data(self):
        with open('work_data.json', 'w') as file:



def main():
    args = tuple(sys.argv)
    input()

if __name__ == '__main__':
    main()
