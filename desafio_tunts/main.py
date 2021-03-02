import os

from .sheet_funcs import decide_status, get_sheet, get_total_classes


def main():
    # base directory of the current file (project root)
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # credentials `creds.json` file is expected to be in the project root
    creds_file = os.path.join(base_dir, "creds.json")

    # name of the sheet to run the script
    sheet_name = (
        "Engenharia de Software - Desafio Luis Carlos Firmino Pinheiro"
    )

    sheet = get_sheet(creds_file, sheet_name)

    sheet_values = sheet.get()

    total_classes = get_total_classes(sheet_values)

    decide_status(sheet, sheet_values, total_classes)
