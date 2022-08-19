import os
import shutil
import pandas as pd
from config import *
from utils import *


def read_input():
    return pd.read_excel(INPUT_FILE, sheet_name=INPUT_SHEET, header=EXCEL_HEADER, usecols=input_cols)


def contains(file, target):
    file.seek(0)
    for line in file:
        if target in line:
            return True

    return False


def check_existance(row_data):
    with open(SAVED_NIS) as nis:
        for field in InputMapping:
            value = row_data[field["Excel colname"]]
            type = field["Novinsoft Field"]["type"]
            if type == INPUT_FIELD and not contains(file=nis, target=str(value)):
                name = field["Novinsoft Field"]["field"]
                tag = field["Novinsoft Field"]["field"]
                print(f"NIS Assertion Failed: {tag} > {name} value {value} not found")
                return False

    print("NIS Assertion Passed")
    return True


def isFolderEmpty(i):
    folder = os.path.join(WORKSPACE, PREFIX + str(i))
    if not os.path.exists(folder):
        os.makedirs(folder)
    files = os.listdir(folder)
    if files:
        return False
    return True


def copyToWorkSpace(i):
    folder = os.path.join(WORKSPACE, PREFIX+str(i))
    shutil.copyfile(SAVED_NIS, os.path.join(folder, f"{PREFIX}{i}.NIS"))
    shutil.copyfile(EXPORTED_EXCEL, os.path.join(folder, f"{PREFIX}{i}.xls"))

