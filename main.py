from tkinter import *
from load_file import *
from scroll_image import CanvasImage
from DataHolder import DataHolder
data_holder = DataHolder()
path = ''
window = Tk()
file_holder = FileHolder()
window.title("ПК Бизнес-гид")
             # window.title("Добро пожаловать в приложение Бизнес-гид")
             # lbl = Label(window, text="Данное приложение позволяет производить\n автоматизированный анализ"
             #"логов ваших бизнес-процессов"
packframe = Frame(window)
button_load = Button(packframe,
                     text="Загрузить лог",  # текст кнопки
                     background="#555",  # фоновый цвет кнопки
                     foreground="#ccc",  # цвет текста
                     padx="88",  # отступ от границ до содержимого по горизонтали
                     pady="8",  # отступ от границ до содержимого по вертикали
                     font="16",  # высота шрифта
                     command=lambda: file_holder.get_file(holder=data_holder)
                     )
button_statistic = Button(packframe,
                          text="Статистический анализ",  # текст кнопки
                          background="#555",  # фоновый цвет кнопки
                          foreground="#ccc",  # цвет текста
                          padx="54",  # отступ от границ до содержимого по горизонтали
                          pady="8",  # отступ от границ до содержимого по вертикали
                          font="16",  # высота шрифта
                          #command=tmp_func()
                          )
button_recomend = Button(packframe,
                         text="Автоматические реккомендации",  # текст кнопки
                         background="#555",  # фоновый цвет кнопки
                         foreground="#ccc",  # цвет текста
                         padx="20",  # отступ от границ до содержимого по горизонтали
                         pady="8",  # отступ от границ до содержимого по вертикали
                         font="16",  # высота шрифта
                         #command=tmp_func()
                         )
button_show = Button(packframe,
                     text="Отобразить процесс",  # текст кнопки
                     background="#555",  # фоновый цвет кнопки
                     foreground="#ccc",  # цвет текста
                     padx="61",  # отступ от границ до содержимого по горизонтали
                     pady="8",  # отступ от границ до содержимого по вертикали
                     font="16",  # высота шрифта
                     #command=tmp_func()
                     )
button_filter = Button(packframe,
                       text="Отфильтровать процесс",  # текст кнопки
                       background="#555",  # фоновый цвет кнопки
                       foreground="#ccc",  # цвет текста
                       padx="46",  # отступ от границ до содержимого по горизонтали
                       pady="8",  # отступ от границ до содержимого по вертикали
                       font="16",
                       # высота шрифта
                       #command=tmp_func()
                       )

Grid.rowconfigure(window, 0, weight = 1)
Grid.rowconfigure(window, 1, weight = 1)
Grid.columnconfigure(window, 1, weight = 1)

canvas = CanvasImage(window, 'C:\\Users\Сергей\Downloads\maxresdefault.jpg')


canvas.grid(column = 1, row = 0, sticky = 'NSEW', columnspan = 4)
button_load.grid(row = 0, sticky = 'NSEW')
button_statistic.grid(row = 1, sticky = 'NSEW')
button_recomend.grid(row = 2, sticky = 'NSEW')
button_show.grid(row = 3, sticky = 'NSEW')
button_filter.grid(row = 4, sticky = 'NSEW')
packframe.grid(column =0, row = 0, sticky = 'NSEW')

window.geometry('500x200')
window.mainloop()
