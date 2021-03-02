import sys

import gspread
from gspread.models import Worksheet


def decide_status(sheet: Worksheet, sheet_values: list, total_classes: int):
    """Goes through sheet data to decide student's situation.

    Args:
        sheet (Worksheet): worksheet to write the results to.
        sheet_values (list): sheet values (using Worksheet.get() method).
        total_classes (int): number of total classes in that course.
    """
    for i, row in enumerate(sheet_values[3:]):
        absences = int(row[2])
        average = round((int(row[3]) + int(row[4]) + int(row[5])) / 3)

        if absences / total_classes > 0.25:
            msg = "Reprovado por Falta"
            write_status(sheet, row, i + 4, msg, 0)

        elif average < 50:
            msg = "Reprovado"
            write_status(sheet, row, i + 4, msg, 0)

        elif average >= 50 and average < 70:
            msg = "Exame Final"
            write_status(sheet, row, i + 4, msg, calc_final(average))

        else:
            msg = "Aprovado"
            write_status(sheet, row, i + 4, msg, 0)


def write_status(
    sheet: Worksheet, row: list, row_n: int, message: str, needed_grade: int
):
    """Writes a student status to the worksheet

    Args:
        sheet (Worksheet): worksheet to write to.
        row (list): list containing student's information.
        row_n (int): row number to write to.
        message (str): message with student's status
        needed_grade (int): student's needed grade in the final exam.
    """

    sheet.update_cell(row_n, 7, message)
    sheet.update_cell(row_n, 8, needed_grade)
    print(
        f"Student_ID: {row[0]}, Student_name: {row[1]}, Student_status: {message}"
    )


def get_total_classes(sheet_values: list) -> int:
    """Given sheet data, returns total number of classes, assuming the value is
    in range 'A2' of the sheet.

    Args:
        sheet_values (list): list returned by sheet.get() method

    Returns:
        int: total classes
    """
    try:
        n_classes = int("".join(sheet_values[1]).split(": ")[1])
        print(f"Total classes: {n_classes}")
        return n_classes
    except IndexError:
        print("Could not find total classes in sheet range: 'A2'")
        sys.exit(1)


def calc_final(avg: int) -> int:
    """
    Calcultates a student's needed grade in the final exam to pass a class.

    Args:
        avg (int): student average grade

    Returns:
        int: student's needed grade.
    """
    return 100 - avg


def get_sheet(credentials_path: str, sheet_name: str):
    """
    Gets the first sheet with the name specified

    Args:
        credentials_path (str): path to credentials file.
        sheet_name (str): name of the sheet to be accessed.

    Returns:
        [Worksheet]: returns the first sheet object
    """
    gc = gspread.service_account(credentials_path)
    try:
        sheet = gc.open(sheet_name).sheet1
        print(f"Successfully got sheet {sheet_name} ")
        return sheet

    except (gspread.SpreadsheetNotFound, AttributeError):
        print(f"Could not find sheet: {sheet_name}.")
        sys.exit(1)
