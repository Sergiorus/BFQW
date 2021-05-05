from tkinter import filedialog as fd
from GraphBuilder import GraphBuilder
from scroll_image import CanvasImage


class FileHolder:
    def __init__(self):
        self.file_dialog = fd
        self.file = ''

    def get_file(self, extension=None):
        if extension is None:
            extension = ['*.log', '*.xes', '*.csv', '*.xlsx']
        self.file = self.file_dialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("csv files", r" ".join(extension)),))

    def show_file(self, holder, root, window):
        self.get_file()
        # dfg = dfg_fac.apply(self.file)
        holder.source_data = GraphBuilder(self.file)
        holder.source_data.save()
        holder.current_data = holder.source_data
        window.destroy()
        window = CanvasImage(root, 'C:\\Users\\Сергей\\PycharmProjects\\BFQW\\tmp.png')
        window.grid(column=1, row=0, sticky='NSEW', columnspan=4)
