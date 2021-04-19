from pm4py.objects.conversion.log.converter import to_data_frame
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_import_factory


class Transformer:
    def __init__(self, path_to_file):
        self.path = path_to_file

    def get_PMlog_from_xes(self):
        log = xes_import_factory.apply(self.path)
        return log

    def get_PD_from_xes(self):
        log = self.get_PMlog_from_xes()
        df = to_data_frame.apply(log)
        return df

    def get_PD_from_log(self):
        df = pd.read_fwf(self.path)
        cols = df.columns.tolist()
        cols=cols[-1:] + cols[:-1]
        df = df[cols]
        return df