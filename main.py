"""Запускает приложение"""
from log_scanner import LogScanner
from preproccessor import Preprocessor
from predictor import Predictor


if __name__ == '__main__':

    scanner = LogScanner()
    scanner.scan()

    preproccessor = Preprocessor()

    predictor = Predictor(scanner=scanner, preproccessor=preproccessor)
    predictor.start()
