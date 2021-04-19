from tkinter import filedialog as fd
from GraphBuilder import GraphBuilder
from pm4py.algo.discovery.dfg import algorithm as dfg_fac


class FileHolder:
    def __init__(self):
        self.file_dialog = fd
        self.file = ''

    def get_file(self, holder, extension=None):
        if extension is None:
            extension = ['*.log', '*.xes', '*.csv', '*.xlsx']
        path = self.file_dialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("csv files", r" ".join(extension)),))
        dfg = dfg_fac.apply(path)
        holder.source_data = GraphBuilder(path, dfg)
        picture = holder.source_data.apply2(dfg, holder.source_data.log)
        GraphBuilder().save(picture, 'C:\\Users\Сергей\PycharmProjects\BFQW')
