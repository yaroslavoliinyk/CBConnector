import csv
import os
from tkinter import *  # noqa F403
from tkinter import E, W
from tkinter.ttk import Combobox


class Setup:

    __beam = dict()
    __default_settings = dict()
    __path = ""

    def __init__(self, beam_type, build_ele):

        self.__beam_type = beam_type
        self.__build_ele = build_ele

        if self.__build_ele.CBeamSettingsName.value == "":
            self.__build_ele.CBeamSettingsName.value = Setup.__beam[1][
                self.__build_ele.CBeamSettingsUnit.value
            ][Setup.__default_settings[1]]

        if self.__build_ele.HBeamSettingsName.value == "":
            self.__build_ele.HBeamSettingsName.value = Setup.__beam[2][
                self.__build_ele.HBeamSettingsUnit.value
            ][Setup.__default_settings[2]]

    @staticmethod
    def upload_data():
        # beam 1 = CBeam, beam 2 = HBeam
        Setup.__beam[1] = {"imperial": [], "metric": []}
        Setup.__beam[2] = {"imperial": [], "metric": []}
        Setup.__default_settings[1] = 9
        Setup.__default_settings[2] = 121

        Setup.__path = os.path.dirname(os.path.abspath(__file__))

        data = dict()
        data["imperial_C_type.csv"] = []
        data["metric_C_type.csv"] = []
        data["imperial_W_type.csv"] = []
        data["metric_W_type.csv"] = []

        for filename in data.keys():
            with open(Setup.__path + "\\" + filename, encoding="utf-8") as file:
                first = True
                reader = csv.reader(file, delimiter=",")
                for row in reader:
                    if first:
                        first = False
                        continue
                    data[filename].append(row[0])

        Setup.__beam[1]["imperial"].extend(data["imperial_C_type.csv"])
        Setup.__beam[1]["metric"].extend(data["metric_C_type.csv"])
        Setup.__beam[2]["imperial"].extend(data["imperial_W_type.csv"])
        Setup.__beam[2]["metric"].extend(data["metric_W_type.csv"])

    def launch(self):
        self.__window = Tk()  # noqa F405
        self.__interface(self.__beam_type)
        self.__window.mainloop()

    def cbeam_data(self, settings, unit):
        found = False
        data = dict()
        multiplier = 1
        if unit == "imperial":
            multiplier = 25.4

        with open(Setup.__path + "\\" + unit + "_C_type.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                if row[0] == settings:
                    found = True
                    data["d"] = self.__convert_to_decimal(row[1]) * multiplier
                    data["bf"] = self.__convert_to_decimal(row[2]) * multiplier
                    data["tf"] = self.__convert_to_decimal(row[3]) * multiplier
                    data["tw"] = self.__convert_to_decimal(row[4]) * multiplier
                    data["xb"] = self.__convert_to_decimal(row[7]) * multiplier
                    data["k"] = self.__convert_to_decimal(row[11]) * multiplier
                    data["W"] = self.__convert_to_decimal(row[12])
                    break
        if not found:
            raise Exception("Could not found such settings!")
        return data

    def hbeam_data(self, settings, unit):
        found = False
        data = dict()
        multiplier = 1
        if unit == "imperial":
            multiplier = 25.4

        with open(Setup.__path + "\\" + unit + "_W_type.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                if row[0] == settings:
                    found = True
                    data["d"] = self.__convert_to_decimal(row[1]) * multiplier
                    data["bf"] = self.__convert_to_decimal(row[2]) * multiplier
                    data["tf"] = self.__convert_to_decimal(row[3]) * multiplier
                    data["tw"] = self.__convert_to_decimal(row[4]) * multiplier
                    data["k1"] = self.__convert_to_decimal(row[10]) * multiplier
                    data["W"] = self.__convert_to_decimal(row[11])
                    break
        if not found:
            raise Exception("Could not found such settings!")
        return data

    def __interface(self, beam_type):
        self.__window.title("Select cross section")
        self.__window.geometry("300x125")
        # self.grid(sticky=W, pady=10)

        self.__selected_unit = StringVar(value="imperial")  # noqa F405
        imperial_rb = Radiobutton(  # noqa F405
            self.__window,
            text="Imperial values",
            value="imperial",
            variable=self.__selected_unit,
            command=self.__selected,
        )
        metric_rb = Radiobutton(  # noqa F405
            self.__window,
            text="Metric values",
            value="metric",
            variable=self.__selected_unit,
            command=self.__selected,
        )
        imperial_rb.grid(column=0, row=0, padx=10, sticky=W)
        metric_rb.grid(column=0, row=1, padx=10, sticky=W)

        lbl = Label(self.__window, text="Choose size from list:")  # noqa F405
        lbl.grid(column=0, row=3, padx=10, sticky=W)

        self.__combo = Combobox(self.__window)  # noqa F405
        current, self.__combo["values"] = self.__get_combo_values(
            beam_type, self.__selected_unit
        )
        self.__combo.grid(column=1, row=3, padx=10)
        self.__combo.current(current)

        btn = Button(  # noqa F405
            self.__window, text="Save & quit", command=self.__clicked
        )
        btn.grid(column=1, row=5, padx=10, pady=10, sticky=E)

    def __get_combo_values(self, beam_type, selected_unit):
        if beam_type == 1:
            current_name = self.__build_ele.CBeamSettingsName.value
            current_unit = self.__build_ele.CBeamSettingsUnit.value
        elif beam_type == 2:
            current_name = self.__build_ele.HBeamSettingsName.value
            current_unit = self.__build_ele.HBeamSettingsUnit.value
        else:
            raise Exception("No such beam type")

        current_index = Setup.__beam[beam_type][current_unit].index(current_name)
        return current_index, Setup.__beam[beam_type][selected_unit.get()]

    def __convert_to_decimal(self, str_number):
        # print("\nstr_number: ", str_number)
        if len(str_number.split("/")) == 1:
            return float(str_number)
        else:
            if " " in str_number.strip():
                integer_part, decimal_part = list(filter(None, str_number.split(" ")))
                numerator, denominator = decimal_part.split("/")
            elif "-" in str_number:
                integer_part, decimal_part = list(filter(None, str_number.split("-")))
                numerator, denominator = decimal_part.split("/")
            else:
                integer_part = 0
                numerator, denominator = str_number.split("/")

            return float(numerator) / float(denominator) + float(integer_part)

    def __selected(self):
        current, self.__combo["values"] = self.__get_combo_values(
            self.__beam_type, self.__selected_unit
        )
        self.__combo.grid(column=1, row=3)
        self.__combo.current(current)
        # if self.__beam_type == 1:
        #   self.__build_ele.CBeamSettingsUnit.value = self.__selected_unit.get()
        # elif self.__beam_type == 2:
        #   self.__build_ele.HBeamSettingsUnit.value = self.__selected_unit.get()

    def __clicked(self):
        if self.__beam_type == 1:
            self.__build_ele.CBeamSettingsName.value = self.__combo.get()
            self.__build_ele.CBeamSettingsUnit.value = self.__selected_unit.get()
        elif self.__beam_type == 2:
            self.__build_ele.HBeamSettingsName.value = self.__combo.get()
            self.__build_ele.HBeamSettingsUnit.value = self.__selected_unit.get()

        self.__window.destroy()
