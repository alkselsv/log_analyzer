"""Запускает приложение"""
import argparse
from log_scanner import LogScanner
from preproccessor import Preprocessor
from predictor import Predictor


if __name__ == '__main__':

    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Log monitoring and processing')
    parser.add_argument('--root_dir', type=str, default="users",
                        help='Path to the root dir')
    parser.add_argument('--models_dir', type=str, default="models",
                        help='Path to the classification models')
    args = parser.parse_args()

    # Установка путей
    root_dir = args.root_dir
    models_dir = args.models_dir

    scanner = LogScanner(root_dir)
    scanner.scan()

    preproccessor = Preprocessor()

    predictor = Predictor(
        scanner=scanner, preproccessor=preproccessor, models_dir=models_dir)
    predictor.start()
