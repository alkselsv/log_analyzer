"""Определение класса Scanner"""
import os
import json


class LogScanner:
    """Сканер логов"""

    def __init__(self, root_dir="users", logger=None):
        self.root_dir = root_dir
        self.logger = logger
        self.models = []
        self.min_bounds = []
        self.log_files = []
        self.logger = logger

    def scan(self):
        """Выполняет поиск файлов settings.json и загружет из них настройки"""

        for user_id in os.listdir(self.root_dir):
            user_dir = os.path.join(self.root_dir, user_id)
            if os.path.isdir(user_dir):
                for site_id in os.listdir(user_dir):
                    site_dir = os.path.join(user_dir, site_id)
                    if os.path.isdir(site_dir):
                        settings_file = os.path.join(site_dir, "settings.json")
                        if os.path.isfile(settings_file):
                            with open(settings_file, 'r', encoding="utf8") as file:
                                settings = json.load(file)
                                self.models.append(settings.get("model"))
                                self.min_bounds.append(
                                    settings.get("min_bound_per") / 100)
                        log_file = os.path.join(site_dir, "logs", "sp.csv.log")
                        if os.path.isfile(log_file):
                            self.log_files.append(log_file)
        self.logger.info(f"Found log files: {self.log_files}")
        self.logger.info(f"Found model files: {self.models}")

    def get_models(self):
        """Возвращает список моделей"""

        return self.models

    def get_min_bounds(self):
        """Возвращает пороговых значений"""

        return self.min_bounds

    def get_log_files(self):
        """Возвращает список путей к файлам"""

        return self.log_files
