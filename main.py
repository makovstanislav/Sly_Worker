import os
import shutil
import textract
import subprocess
import yaml


# parses yaml file. Yields a dict
def read_yaml():
    with open('data.yaml') as f:
        dataset = yaml.safe_load(f)
        return dataset


# the dictionary containing entries for a document`s type/subtype recognition
data = read_yaml()
# the counter of all sorted documents
counter_all = 0
# the counter of types and subtypes of sorted documents
counter_dict = {}
# variables containing paths to source and output directories
source_dir = ""
output_dir = ""


# returns text of MS Office file
def reader(file_path):
    text = textract.process(file_path)
    text = text.decode()
    return text


# creates a folder and returns the path to it
def make_folder(source_dir, name):
    new_folder = os.path.join(source_dir, name)
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)
    return os.path.join(source_dir, name)


# returns updated counter counter_dict
def update_counter(subject, dict):
    parent_name = subject.partition("/")[0]
    child_name = subject.partition("/")[2]
    if "/" not in subject:
        child_name = None

    if not parent_name in dict:
        dict.update({parent_name: {"num": 1}})
        if child_name:
            dict[parent_name].update({"subtypes": {child_name: 1}})
        return dict

    dict[parent_name]["num"] = dict[parent_name]["num"] + 1

    if "subtypes" in dict.get(parent_name):
        if child_name in dict[parent_name]["subtypes"]:
            dict[parent_name]["subtypes"][child_name] = dict[parent_name]["subtypes"][child_name] + 1
        else:
            dict[parent_name]["subtypes"].update({child_name: 1})
    return dict


# sorts files by type/subtype
def sort_docs(source_dir, output_dir):
    # creates a folder for each type and subtype
    for type, value in data.items():
        make_folder(output_dir, type)
        if "subtypes" in value:
            for subtype in value["subtypes"]:
                subtype_name = type + "/" + subtype
                make_folder(output_dir, subtype_name)
            make_folder(output_dir + "/" + type, "Other")
    make_folder(output_dir, "Other")

    # temporary storage for converted files
    tempStorage = make_folder(output_dir, "tempStorage")
    # for corrupted files storage
    FailedToRead = make_folder(output_dir, "FailedToRead")

    # detects type/subtype, moves into respective folders, updates counters
    def sort(content, item_name):
        global counter_dict, counter_all
        from detext import Doc
        document = Doc(content)
        subject_name = document.subject()
        shutil.move(item_path, os.path.join(output_dir + "/" + subject_name, item_name))
        counter_dict = update_counter(subject_name, counter_dict)
        counter_all += 1

    # looking into the directory containing files and iterates
    dir_items = os.listdir(source_dir)
    for item in dir_items:
        item_path = os.path.join(source_dir, item)
        if os.path.isdir(item_path):
            continue

        # converts .doc/.docm into readable format via LibreOffice and moves into temp storage
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

        # document reading
        try:
            content = reader(item_path)
        # error --> moves to a folder for corrupted files
        except Exception as e:
            shutil.move(item_path, os.path.join(FailedToRead, item))
            current_text = lbl_errors.cget("text")
            new_text = item + "\n" + current_text
            lbl_errors.config(text=new_text)
            continue

        sort(content, item)

    # scanning files from the folder with converted files (temp storage)
    # if temp storage is empty, it will be deleted
    if len(os.listdir(tempStorage)) == 0:
        os.rmdir(tempStorage)
    else:
        for item in os.listdir(tempStorage):
            item_path = os.path.join(tempStorage, item)
            content = reader(item_path)
            sort(content, item)

    if os.path.isdir(tempStorage):
        os.rmdir(tempStorage)


# converts counter_dict into human-readable string. Looks as follows:
# Contract: __
#   Rent: __

def str_stats():
    stats = ""
    for key, value in counter_dict.items():
        stats += key + ": " + str(value.get("num")) + "\n"
        if "subtypes" in value:
            for subtype, num in value["subtypes"].items():
                stats += "   " + subtype + ": " + str(num) + "\n"
    return stats


# GUI
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

window = tk.Tk()
window.geometry("822x477")
style = ttk.Style(window)
# using custom theme "azure"
window.tk.call('source', 'azure.tcl')
ttk.Style().theme_use('azure')
window.title('SlyWorker')
window.attributes("-alpha", 0.99)


# functions for GUI

# opens dialogue window which allows users to choose a folder containing documents for sorting
def select_source():
    application_window = tk.Tk()
    global source_dir, lbl_selected_source
    answer = filedialog.askdirectory(parent=application_window,
                                     initialdir=os.getcwd(),
                                     title="Please select a folder:")
    source_dir = answer
    lbl_selected_source["text"] = answer
    lbl_waiting.config(text="Waiting for sorting: " + str(files_num(answer)))
    application_window.withdraw()
    return answer


# opens a dialogue window which allows users to choose a folder which will keep sorted documents in
def select_output():
    application_window = tk.Tk()
    global output_dir, lbl_selected_output
    answer = filedialog.askdirectory(parent=application_window,
                                     initialdir=os.getcwd(),
                                     title="Please select a folder:")
    output_dir = answer
    lbl_selected_output["text"] = answer
    application_window.withdraw()
    return answer


# yields number of files in a folder
def files_num(path):
    num = 0
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            continue
        else:
            num += 1
    return num


# launches "Sort" button
def sort_btn_fn():
    global lbl_selected_output
    messagebox.askokcancel("askokcancel",
                           """The app may not respond during the sorting \n\n We recommend to wait until the process ends""")
    sort_docs(source_dir, output_dir)
    x = str_stats()
    lbl_by_subject["text"] = "\n" + x
    lbl_all_sorted["text"] = "SORTED TOTAL: " + str(counter_all)
    lbl_waiting.config(text="Waiting for sorting: " + str(files_num(lbl_selected_output.cget("text"))))


# widgets

# frames
frm_1 = ttk.LabelFrame(window, width=150, height=300, text="SETTINGS", labelanchor="n")
frm_1.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
frm_2 = ttk.LabelFrame(window, width=500, height=300, text="RESULTS", labelanchor="n")
frm_2.grid(row=0, column=1, rowspan=2, pady=10, padx=10, sticky="nsew")

# labels in frame 1
lbl_source = ttk.Label(frm_1, text="""Select the folder which contains documents""", anchor="w")
lbl_source.grid(row=1, column=0, pady=10, padx=12, sticky="nsew")

lbl_output = ttk.Label(frm_1, text="Which folder will you save the result to?", anchor="w")
lbl_output.grid(row=4, column=0, pady=15, padx=12, sticky="nsew")

lbl_selected_source = ttk.Label(frm_1, width=38, text="not selected", foreground="#808080")
lbl_selected_source.grid(row=3, column=0, padx=12, sticky="nsew")

lbl_selected_output = ttk.Label(frm_1, width=38, text="not selected", foreground="#808080")
lbl_selected_output.grid(row=6, column=0, pady=5, padx=12, sticky="nsew")

lbl_waiting = ttk.Label(frm_1, text="Waiting for sorting: 0")
lbl_waiting.grid(row=7, column=0, pady=60, padx=12, sticky="nsew")

# separators in frame 1
separator1 = ttk.Separator(frm_1, orient='horizontal')
separator1.place(relx=0.0, x=0, y=115, relwidth=4)
separator2 = ttk.Separator(frm_1, orient='horizontal')
separator2.place(relx=0.0, x=0, y=240, relwidth=4)

# tabs in frame 2
tab_control = ttk.Notebook(frm_2, width=400, height=400)
tab1 = ttk.Frame(tab_control, width=400)
tab2 = ttk.Frame(tab_control, width=400)
tab_control.add(tab1, text="Statistics", sticky="nsew")
tab_control.add(tab2, text="Errors", sticky="nsew")
tab_control.grid(row=0, column=0, rowspan=8, sticky="nsew")

# labels в frame 2
lbl_by_subject = ttk.Label(tab1, text="")
lbl_by_subject.grid(row=0, column=0, rowspan=4, sticky="nw")

lbl_all_sorted = ttk.Label(tab1, text="Sorted overall: 0")
lbl_all_sorted.grid(row=5, column=0, rowspan=4, sticky="nw")

lbl_err_title = ttk.Label(tab2, width=30, text="These files have not been converted:")
lbl_err_title.grid(row=0, column=0, sticky="nw")

# labels with corrupted files
lbl_errors = ttk.Label(tab2, text="")
lbl_errors.grid(row=1, column=0, pady=5, sticky="nsew")

# buttons
btn_dial_1 = ttk.Button(frm_1, text="Select source foulder...", command=lambda: select_source())
btn_dial_1.grid(row=2, column=0, pady=10, padx=10, sticky="new")
btn_dial_2 = ttk.Button(frm_1, text="Select output foulder...", command=lambda: select_output())
btn_dial_2.grid(row=5, column=0, pady=5, padx=10, sticky="new")
btn_sort = ttk.Button(window, text="Sort documents", command=sort_btn_fn)
btn_sort.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

if __name__ == "__main__":
    window.mainloop()
