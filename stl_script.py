import os
from classfigure import Figure
from classresin import waterwash

""""Функция, которая составляет список адресов всех stl файлов в указанной папке"""


def find_stl_files(directory):
    stl_files = []
    for root, dirs, fs in os.walk(directory):
        for f in fs:
            if f.lower().endswith('.stl'):
                full_path = os.path.join(root, f)
                stl_files.append(full_path)
    return stl_files


def stl_script(directory_number, newsize):
    """назначаем папку и спрашиваем доп. параметры"""
    newsize = float(newsize)
    target_dir = os.path.join("example_stlfiles", str(directory_number))
    files = find_stl_files(target_dir)


    """читаем входной файл"""
    file_path = os.path.join(target_dir, "soprfile")
    with open(file_path, "r") as file:
        name = str(file.readline().strip())
        figure_id = str(file.readline().strip())
        coeff = float(file.readline())
        notes = str(file.readline())
        proc = float(file.readline())
        margin = float(file.readline())
        height = float(file.readline())
        if newsize == 0:
            newsize = height

    """создаём объект фигурки, и методами класса Figure считаем объём и цену"""
    TheFigure = Figure(name, figure_id, notes, coeff, files, proc, margin, height)
    TheFigure.wanted_height = newsize
    TheFigure.calculate_volume()
    Figure.calculate_price(TheFigure, waterwash)
    print(TheFigure.stl_files)
    print(TheFigure.get_model_info())

    """записываем инфу в output"""
    with open(os.path.join(target_dir, "output"), "w") as file:
        for i in TheFigure.get_model_info():
            file.write(i + "\n")
    """в аутпуте порядок такой: имя, id, цена, объём без поддержек, объем с поддержками, заметки"""

    return TheFigure.price