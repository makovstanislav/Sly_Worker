import os
import shutil
import chardet
import textract
import subprocess
from detext import Doc, ContractDoc

# определитель юникода (походу не всегда верно)
def unicode_detect(path_to_file):
    file = open(path_to_file, "rb").read()
    result = chardet.detect(file)
    print(result['encoding'])


# возращает текст файла MS Office
def reader(file_path):
    text = textract.process(file_path)
    text = text.decode()
    return text


# создает папку, если не было
def make_folder(source_dir, name):
    new_folder = os.path.join(source_dir, name)
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)
    return os.path.join(source_dir, name)


# сортирует файлы MS Office по папкам по критерию "Предмет"
def sort_docs(source_dir, output_dir):

    # создание папок
    # по предмету документа
    for subject in Doc.subjects:
        make_folder(output_dir, subject)
    # по предмету контракта
    for subject in ContractDoc.subjects:
        make_folder(output_dir+"/Contract", subject)
    # буфер для конвертированных файлов
    tempStorage = make_folder(output_dir, "tempStorage")
    # для файлов с неподдерживаемым конвертером расширением
    FailedToRead = make_folder(output_dir, "FailedToRead")

    # определяет предмет и сортирует в соотв папки
    def sort(content, item_name):
        document = Doc(content)
        subject_name = document.subject()
        if subject_name == "Contract":
            document = ContractDoc(content)
            subject_name = document.subject()
            shutil.move(item_path, os.path.join(output_dir + "/Contract/" + subject_name, item_name))
        elif subject_name == "Letter":
            shutil.move(item_path, os.path.join(output_dir + "/" + subject_name, item_name))
        else:
            shutil.move(item_path, os.path.join(output_dir + "/" + subject_name, item_name))

    # итерация по каждому файлу в source_dir и сортировка
    dir_items = os.listdir(source_dir)
    for item in dir_items:
        item_path = os.path.join(source_dir, item)
        if os.path.isdir(item_path):
            continue

        # .doc/.docm файл конвертируется и перемещается в отдельную временную папку
        if item.endswith(".doc"):
            subprocess.call(
                ['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', "docx",
                 "--outdir", tempStorage, item_path])
            os.remove(item_path)
            continue

        if item.endswith(".docm"):
            subprocess.call(
                ['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--convert-to', "docx",
                 "--outdir", tempStorage, item_path])
            os.remove(item_path)
            continue

        # чтение документа
        try:
            content = reader(item_path)
        # ошибка --> в отдельную папку
        except Exception as e:
            print("Вот этот файл проблемный {}. Ошибка {}.".format(item_path, e))
            shutil.move(item_path, os.path.join(FailedToRead, item))
            continue

        sort(content, item)

    # скан файлов из буфера с конвертированными в docx файлами
    # если в буфере ничего нет изначально или он почищен, то он удаляется
    if len(os.listdir(tempStorage)) == 0:
        os.rmdir(tempStorage)
    else:
        for item in os.listdir(tempStorage):
            item_path = os.path.join(tempStorage, item)
            content = reader(item_path)
            sort(content, item)

    if os.path.isdir(tempStorage):
        os.rmdir(tempStorage)


sort_docs("/Users/stanislavmakov/Desktop/SortingMachine", "/Users/stanislavmakov/Desktop/SortingMachine/Sorted")




