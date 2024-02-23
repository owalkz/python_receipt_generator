# references:
# https://pynative.com/python-random-shuffle/#:~:text=Shuffling%20a%20dictionary%20is%20not,dictionary%20values%20using%20shuffled%20keys.
# https://github.com/ccnmtl/fdfgen/blob/master/README.md
# https://stackoverflow.com/questions/3730964/python-script-execute-commands-in-terminal
# https://pynative.com/python-get-month-name-from-number/#:~:text=We%20can%20use%20two%20ways,Python%20using%20the%20calendar%20module.&text=Calendar%20is%20a%20built%2Din%20module%20available%20in%20Python.

from fdfgen import forge_fdf
import sys
import csv
import re
import random
import os
import calendar


def main():
    fill_pdf(file_access(input("File: ")),input("Date (DD-MM-YYYY): "))


def file_access(csv_file_name):
    try:
        with open(csv_file_name) as content_file:
            initial_dictionary = dict()
            shuffled_dictionary = dict()
            reader = csv.DictReader(content_file)
            for line in reader:
                initial_dictionary.update(
                    {
                        line["description"]: {
                            "quantity": line["quantity"],
                            "unit_price": line["unit_price"],
                        }
                    }
                )

            dictionary_keys_list = list(initial_dictionary.keys())
            random.shuffle(dictionary_keys_list)

            for key in dictionary_keys_list:
                shuffled_dictionary.update({key: initial_dictionary[key]})
            return shuffled_dictionary
    except FileNotFoundError:
        sys.exit("File not Found")


def fill_pdf(shuffled, date):
    invoice_number = random.randint(100, 999)
    i = 1
    total = 0
    unit_total = 0
    while True:
        try:
            if matches := re.match(
                r"^([0-9][0-9])\-([0-9][0-9])\-([0-9][0-9][0-9][0-9])$", date
            ):
                if int(matches.group(1)) > 31 or int(matches.group(1)) < 1:
                    raise ValueError
                if int(matches.group(2)) > 12 or int(matches.group(2)) < 1:
                    raise ValueError
                file_name = (
                    "ReceiptFor"
                    + calendar.month_name[int(matches.group(2))]
                    + matches.group(3)
                    + ".pdf"
                )
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid date")
            date = input("Date (DD-MM-YYYY): ")

    fields = [("invoice_number", invoice_number), ("invoice_date", date)]
    for item in shuffled:
        description = item
        price = shuffled[item]["unit_price"]
        quantity = shuffled[item]["quantity"]
        unit_total = int(price) * int(quantity)
        total += unit_total
        i = str(i)
        fields.append(("item_" + i + "_description", description))
        fields.append(("item_" + i + "_price", price))
        fields.append(("item_" + i + "_quantity", quantity))
        fields.append(("item_" + i + "_total", unit_total))
        i = int(i)
        i += 1
    fields.append(("subtotal", total))
    fields.append(("total", total))

    fdf = forge_fdf("", fields, [], [], [])

    with open("data.fdf", "wb") as fdf_file:
        fdf_file.write(fdf)

    os.system(
        "pdftk fillable_pdf.pdf fill_form data.fdf output " + file_name + " flatten"
    )

    check_exists(file_name)


def check_exists(name):
    try:
        with open(name) as file:
            ...
    except FileNotFoundError:
        sys.exit("File not Found")


if __name__ == "__main__":
    main()
