import importlib
import sys

def load_app():
    # Replace 'ain' with the name of your main script
    module = importlib.import_module('main')
    module.main()

if __name__ == '__main__':
    load_app()