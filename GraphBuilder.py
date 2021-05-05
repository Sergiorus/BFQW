import pandas as pd
import pm4py
from pm4py.algo.discovery.dfg import algorithm as dfg_fac
from pm4py.objects.conversion.log import converter as log_converter
from Transformer import Transformer
from pm4py.objects.log.util import dataframe_utils
from pm4py.statistics.start_activities.log import get as start_activities
from pm4py.statistics.end_activities.log import get as end_activities
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery


class GraphBuilder:

    def __init__(self, path_to_file):
        if type(path_to_file) != str or len(path_to_file) == 0:
            raise NameError('Wrong path to file')
        else:
            self.path = path_to_file
        self.__transformer = Transformer(self.path)
        self.__prepare_file()

    def __prepare_file(self):
        if self.path.endswith('.xes'):
            self.log = xes_importer.apply(self.path)
            self.dataframe = log_converter.apply(self.log, variant=log_converter.Variants.TO_DATA_FRAME)
            self.dfg = dfg_fac.apply(self.log)
        elif self.path.endswith('.log'):
            self.dataframe = self.__transformer.get_PD_from_log()
            self.log = log_converter.apply(self.log, variant=log_converter.Variants.TO_EVENT_LOG)
            self.dfg = dfg_fac.apply(self.log)
        elif self.path.endswith('.csv'):
            self.dataframe = pd.read_csv(self.path)
            self.dataframe = dataframe_utils.convert_timestamp_columns_in_df(self.dataframe)
            self.log = log_converter.apply(self.dataframe)
            self.dfg = dfg_discovery.apply(self.log, variant=dfg_discovery.Variants.NATIVE)

    def save(self):
        sa = start_activities.get_start_activities(self.dfg)
        ea = end_activities.get_end_activities(self.dfg)
        pm4py.save_vis_dfg(self.dfg, sa, ea, file_path='C:\\Users\\Сергей\\PycharmProjects\\BFQW\\tmp.png')
