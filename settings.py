import json

class Settings():
    def __init__(self, config_path):
        self.load_settings(config_path)

    def load_settings(self, path_to_config_file):
        """Функция для загрузки пользовательских настроек."""
        with open(path_to_config_file, 'r', encoding='utf-8') as json_config_file:
            self.configurational_dict = dict(json.loads(json_config_file.read()))
        

if __name__ == "__main__":
    input('''Это модуль настроек. Он не является главным.
    Для запуска используйте main.py''')
