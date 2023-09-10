"""Запускает приложение"""
from log_scanner import LogScanner
from preproccessor import Preprocessor
from predictor import Predictor

scanner = LogScanner()
scanner.scan()
print(scanner.get_models())
print(scanner.get_min_bounds())
print(scanner.get_log_files())

preproccessor = Preprocessor()

predictor = Predictor(scanner=scanner, preproccessor=preproccessor)
predictor.start()
