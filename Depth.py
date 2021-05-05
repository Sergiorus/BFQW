import tkinter.messagebox as mb
import tkinter as tk


class Depth(tk.Toplevel):
    def __init__(self, parent, recom):
        super().__init__(master=parent)
        self.label = tk.Label(self, text="Сколько инсайдов показывать?")
        self.number = 0
        self.value = tk.Entry(self, textvariable = self.number)
        self.ok_btn = tk.Button(self, text='ОК',
                                command=lambda: self.control_type(recom))
        self.label.grid(row=0)
        self.value.grid(row=1)
        self.ok_btn.grid(row=2)


    def control_type(self, recom):
        """Проверяет вводимые данные"""

        data = self.value.get()
        if not data.isdigit() and data != '':
            self.value["bg"] = "red"
            mb.showerror(title="Ошибка", message="Неверный тип данных, ожидалось число")
        else:
            self.value["bg"] = "white"
            recom.value = data
            print(data)
            print(recom.value)
        self.destroy()

