# Игнорировать предупреждение из-за PyInstaller
import warnings
warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)

import os
import sys
from generate_plots import generate_plots
from shutil import copy
from glob import glob
from sys import exit
import pandas as pd
from xhtml2pdf import pisa

BUILD_DIR = 'build'
TEMPLATE_DIR = 'template'
OUTPUT_FILENAME = 'output'

def eprint(err, *args, **kwargs):
    print(err, *args, file=sys.stderr, **kwargs)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def read_signal(filename):
    data = pd.read_csv(filename, header=None)
    return data[0].values

def create_pdf(input_filename, output_filename):
    with open(input_filename, 'r', encoding="utf-8") as input_file:
        html = input_file.read()

    with open(output_filename, 'w+b') as result_file:
        pisa_status = pisa.CreatePDF(
                html,
                encoding='UTF-8',
                dest=result_file, path=input_filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        eprint(f"Использование: {sys.argv[0]} <имя файла.csv>")
        exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        eprint(f"Файл по пути '{filename}' не найден")
        exit(1)

    print('Чтение сигнала из файла...')
    try:
        signal = read_signal(filename)
    except:
        eprint("Файл содержит данные неверного формата")
        exit(1)

    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)

    generate_plots(signal, BUILD_DIR, filename)

    copy(resource_path(TEMPLATE_DIR + os.sep + 'template.html'), BUILD_DIR)
    copy(resource_path(TEMPLATE_DIR + os.sep + 'NotoSans-Regular.ttf'), BUILD_DIR)

    output_filename = OUTPUT_FILENAME + '.pdf'
    create_pdf(BUILD_DIR + os.sep + 'template.html', output_filename)
    print(f'Результат сохранён в файл {output_filename}')
