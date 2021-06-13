import os
import shutil
import textract
import subprocess
import tkinter as tk
import yaml


# читает yaml. возвращает словарь/список
def read_yaml():
    with open('data.yaml') as f:
        dataset = yaml.safe_load(f)
        return dataset

data = read_yaml()

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
    for type, value in data.items():
        make_folder(output_dir, type)
        if "subtypes" in value:
            for subtype in value["subtypes"]:
                subtype_name = type + "/" + subtype
                make_folder(output_dir, subtype_name)
            make_folder(output_dir + "/" + type, "Other")
    make_folder(output_dir, "Other")

    # буфер для конвертированных файлов
    tempStorage = make_folder(output_dir, "tempStorage")
    # для файлов с неподдерживаемым конвертером расширением
    FailedToRead = make_folder(output_dir, "FailedToRead")
    # счетчик ошибок
    counter = 1

    # определяет предмет и сортирует в соотв папки
    def sort(content, item_name):
        from detext import Doc
        document = Doc(content)
        subject_name = document.subject()
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
            corrupted_file = "Этот файл не удалось сконвертировать:\n {}. \n".format(item_path)
            text.insert(tk.END, str(counter) + ". " + corrupted_file + "\n")
            shutil.move(item_path, os.path.join(FailedToRead, item))
            counter += 1
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

# GUI
window = tk.Tk()
window.title('SlyWorker')
window.attributes("-alpha", 0.97)
window.configure(bg='#043353')
window.geometry("520x830")
# ширина столбцов
window.columnconfigure([0, 2], weight=1, minsize=45)

# для кнопки "Сортировать"
def sort_btn_fn():
    sort_docs(entry1.get(), entry2.get())

# надписи
lbl_source = tk.Label(text="""Адрес папки с документами для сортировки""", height=3, width=38,
                      bg="#043353", fg="#e3dfd1", font=("Montserrat", 18), anchor="w")
lbl_source.grid(row=0, column=1, sticky="nsew")
lbl_output = tk.Label(text="В какую папку сохранить результат?", height=3, width=38, bg="#043353", fg="#e3dfd1",
                      font=("Montserrat", 18), anchor="w")
lbl_output.grid(row=2, column=1, sticky="nsew")
# lbl_app_name = tk.Label(text="Blue", width=40, bg="#043353", fg="#e3dfd1", font=("Montserrat", 20), anchor="n")
# lbl_app_name.grid(row=0, column=2, sticky="nsw")

# поля для ввода текста
entry1 = tk.Entry(width=38, fg="#e3dfd1", highlightbackground="#0a3758", font=("Montserrat", 13))
entry1.insert(tk.END, "/Users/stanislavmakov/Desktop/SortingMachine")
entry1.grid(row=1, column=1, sticky="nsew")
entry2 = tk.Entry(width=38, fg="#e3dfd1", highlightbackground="#0a3758", font=("Montserrat", 13))
entry2.insert(tk.END, "/Users/stanislavmakov/Desktop/SortingMachine/Sorted")
entry2.grid(row=3, column=1, sticky="nsew")

# кнопка
btn_sort = tk.Button(text="Сортировать документы", font=("Montserrat", 15),
                     command=sort_btn_fn, width=20, height=3)
btn_sort.grid(row=4, column=1, pady=30, sticky="nsew")

# текст с названиями проблемных файлов
text = tk.Text(window, width=20, height=39, font=("Montserrat", 10), state = "disabled")
text.grid(row=5, column=1, pady=1, sticky="nsew")


if __name__ == "__main__":
    window.mainloop()
