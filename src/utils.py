from mapping import *


def initial(string):
    return string[0]


def isZero(amount):
    return amount > 0


checkbox_determain = {
    "20 YRCT": isZero
}


def convert(name, ftype, value):

    if ftype == INPUT_FIELD:
        return str(value)

    if ftype == DROPDOWN_LIST:
        return initial(value)

    if ftype == CHECKBOX:
        return checkbox_determain[name](value)
