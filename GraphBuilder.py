import tempfile
import numpy as np
from copy import copy
from graphviz import Digraph
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.discovery.dfg.utils import dfg_utils
from pm4py.objects.log.util import xes
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY
from pm4py.visualization.common.utils import *
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave
from pm4py.objects.conversion.log import converter as log_conv
from pm4py.objects.log.importer.xes import importer as xes_importer
from Transformer import Transformer


class GraphBuilder:

    def __init__(self, path_to_file, dfg=None):
        if type(path_to_file) != str or len(path_to_file) == 0:
            raise NameError('Wrong path to file')
        else:
            self.path = path_to_file
        self.__transformer = Transformer(self.path)
        self.__prepare_file()
        self.dfg = dfg

    def __prepare_file(self):
        if self.path.endswith('.xes'):
            self.log = xes_importer.apply(self.path)
            self.dataframe = self.__transformer.get_PD_from_xes()
        else:
            self.dataframe = self.__transformer.get_PD_from_log()
            self.log = log_conv.apply(self.dataframe)

    def apply2(self, dfg, log=None, activities_count=None, parameters=None, variant="frequency"):
        FREQUENCY = "frequency"
        PERFORMANCE = "performancAXe"
        FREQUENCY_GREEDY = "frequency_greedy"
        PERFORMANCE_GREEDY = "performance_greedy"

        VERSIONS = {FREQUENCY: self.__apply_frequency, PERFORMANCE: self.__apply_performance,
                    FREQUENCY_GREEDY: self.__apply_frequency, PERFORMANCE_GREEDY: self.__apply_performance}

        return VERSIONS[variant](dfg, log=log, activities_count=activities_count, parameters=parameters)

    def save(self, gviz, output_file_path):
        """
        Save the diagram

        Parameters
        -----------
        gviz
            GraphViz diagram
        output_file_path
            Path where the GraphViz output should be saved
        """
        gsave.save(gviz, output_file_path)

    def view(self, gviz):
        """
        View the diagram

        Parameters
        -----------
        gviz
            GraphViz diagram
        """
        return gview.view(gviz)

    def __get_ping_pong(self, thresh=30):
        ping_pong_edges = set(())
        ping_dict = {}
        df = self.dataframe
        for i in range(df.shape[0] - 2):
            if df.iloc[i, 2] == df.iloc[i + 2, 2]:
                key = df.iloc[i, 2] + df.iloc[i + 1, 2]
                if key in ping_dict.keys():
                    ping_dict[key][0] += 1
                else:
                    ping_dict[key] = [1, (df.iloc[i, 2], df.iloc[i + 1, 2]), (df.iloc[i + 1, 2], df.iloc[i, 2])]
        for key in ping_dict.keys():
            if ping_dict[key][0] > thresh:
                ping_pong_edges.add(ping_dict[key][1])
                ping_pong_edges.add(ping_dict[key][2])
        return ping_pong_edges

    def __find_cycles(self, thresh=30):
        temp_cycle = {}
        cycle_edges = set()
        cases = np.unique(self.dataframe[:]['case:concept:name'].tolist())
        for i in range(len(cases)):
            df = self.dataframe[self.dataframe[:]['case:concept:name'] == cases[i]]
            j = 0
            while j < df.shape[0]:
                searching_name = df.iloc[j, 2]
                temp_edges = set()
                for k in range(0, df.shape[0] - 1 - j):
                    temp_edges.add((df.iloc[j + k, 2], df.iloc[j + k + 1, 2]))
                    if df.iloc[j + k, 2] == searching_name and k > 2:
                        if (df.iloc[j, 2] + df.iloc[j + k, 2]) not in temp_cycle.keys():
                            temp_cycle[df.iloc[j, 2] + df.iloc[j + k, 2]] = [1, temp_edges]
                        else:
                            temp_cycle[df.iloc[j, 2] + df.iloc[j + k, 2]][0] += 1
                        break
                j += 1
            for key in temp_cycle.keys():
                if temp_cycle[key][0] > thresh:
                    for el in temp_cycle[key][1]:
                        cycle_edges.add(el)
        return cycle_edges

    def __get_min_max_value(self, dfg):
        """
        Gets min and max value assigned to edges
        in DFG graph

        Parameters
        -----------
        dfg
            Directly follows graph

        Returns
        -----------
        min_value
            Minimum value in directly follows graph
        max_value
            Maximum value in directly follows graph
        """
        min_value = 9999999999
        max_value = -1

        for edge in dfg:
            if dfg[edge] < min_value:
                min_value = dfg[edge]
            if dfg[edge] > max_value:
                max_value = dfg[edge]
        return min_value, max_value

    def __assign_penwidth_edges(self, dfg):
        """
        Assign penwidth to edges in directly-follows graph

        Parameters
        -----------
        dfg
            Direcly follows graph

        Returns
        -----------
        penwidth
            Graph penwidth that edges should have in the direcly follows graph
        """
        penwidth = {}
        min_value, max_value = self.__get_min_max_value(dfg)
        for edge in dfg:
            v0 = dfg[edge]
            v1 = get_arc_penwidth(v0, min_value, max_value)
            penwidth[edge] = str(v1)

        return penwidth

    def __get_activities_color(self, activities_count):
        """
        Get frequency color for attributes

        Parameters
        -----------
        activities_count
            Count of attributes in the log

        Returns
        -----------
        activities_color
            Color assigned to attributes in the graph
        """
        activities_color = {}

        min_value, max_value = self.__get_min_max_value(activities_count)

        for ac in activities_count:
            v0 = activities_count[ac]

            v1 = get_trans_freq_color(v0, min_value, max_value)

            activities_color[ac] = v1

        return activities_color

    def __apply_frequency(self, dfg, log=None, activities_count=None, parameters=None):
        """
        Apply method (to be called from the factory method; calls the graphviz_visualization method)

        Parameters
        -----------
        dfg
            DFG graph
        log
            Event log
        activities_count
            (If provided) Dictionary that associates to each activity its count
        parameters
            Parameters passed to the algorithm (may include the format,
            the replay measure and the maximum number of edges
            in the diagram)
        """

        return self.__apply(dfg, log=log, parameters=parameters, activities_count=activities_count, measure="frequency")

    def __apply_performance(self, dfg, log=None, activities_count=None, parameters=None):
        """
        Apply method (to be called from the factory method; calls the graphviz_visualization method)

        Parameters
        -----------
        dfg
            DFG graph
        log
            Event log
        activities_count
            (If provided) Dictionary that associates to each activity its count
        parameters
            Parameters passed to the algorithm (may include the format,
            the replay measure and the maximum number of edges
            in the diagram)
        """

        return self.__apply(dfg, log=log, parameters=parameters,
                            activities_count=activities_count, measure="performance")

    def __graphviz_visualization(self, activities_count, dfg, ping_pong_thresh, cycle_thresh, image_format="png",
                                 measure="frequency",
                                 max_no_of_edges_in_diagram=170, start_activities=None, end_activities=None):
        """
        Do GraphViz visualization of a DFG graph

        Parameters
        -----------
        activities_count
            Count of attributes in the log (may include attributes that are not in the DFG graph)
        dfg
            DFG graph
        image_format
            GraphViz should be represented in this format
        measure
            Describes which measure is assigned to edges in direcly follows graph (frequency/performance)
        max_no_of_edges_in_diagram
            Maximum number of edges in the diagram allowed for visualization

        Returns
        -----------
        viz
            Digraph object
        """
        if start_activities is None:
            start_activities = []
        if end_activities is None:
            end_activities = []

        ping_pong_edges = self.__get_ping_pong(thresh=ping_pong_thresh)
        cycle_edges = self.__find_cycles(thresh=cycle_thresh)
        filename = tempfile.NamedTemporaryFile(suffix='.gv')
        viz = Digraph("", filename=filename.name, engine='dot', graph_attr={'bgcolor': 'transparent'})

        # first, remove edges in diagram that exceeds the maximum number of edges in the diagram
        dfg_key_value_list = []
        for edge in dfg:
            dfg_key_value_list.append([edge, dfg[edge]])
        dfg_key_value_list = sorted(dfg_key_value_list, key=lambda x: x[1], reverse=True)
        dfg_key_value_list = dfg_key_value_list[0:min(len(dfg_key_value_list), max_no_of_edges_in_diagram)]
        dfg_allowed_keys = [x[0] for x in dfg_key_value_list]
        dfg_keys = list(dfg.keys())
        for edge in dfg_keys:
            if edge not in dfg_allowed_keys:
                del dfg[edge]

        # calculate edges penwidth
        penwidth = self.__assign_penwidth_edges(dfg)
        activities_in_dfg = set()
        activities_count_int = copy(activities_count)
        ackeys = copy(list(activities_count_int.keys()))

        for edge in dfg:
            activities_in_dfg.add(edge[0])
            activities_in_dfg.add(edge[1])

        """for act in ackeys:
            if act not in activities_in_dfg:
                del activities_count_int[act]"""

        # assign attributes color
        activities_color = self.__get_activities_color(activities_count_int)

        # represent nodes
        viz.attr('node', shape='box')

        if len(activities_in_dfg) == 0:
            activities_to_include = set(activities_count_int)
        else:
            activities_to_include = set(activities_in_dfg)

        activities_map = {}

        for act in activities_to_include:
            if "frequency" in measure and act in activities_count_int:
                viz.node(str(hash(act)), act + " (" + str(activities_count_int[act]) + ")", style='filled',
                         fillcolor=activities_color[act])
                activities_map[act] = str(hash(act))
            else:
                viz.node(str(hash(act)), act)
                activities_map[act] = str(hash(act))

        ##############################################################################################
        ##############################################################################################
        # General changes

        # represent edges
        for edge in dfg:
            if "frequency" in measure:
                label = str(dfg[edge])
            else:
                label = human_readable_stat(dfg[edge])

            if edge in ping_pong_edges and edge in cycle_edges:
                edge_color = '#AAF000'
            elif edge in ping_pong_edges:
                edge_color = '#FF0000'
            elif edge in cycle_edges:
                edge_color = '#F0FF00'
            else:
                edge_color = '#000000'
            viz.edge(str(hash(edge[0])), str(hash(edge[1])), label=label,
                     penwidth=str(penwidth[edge]), color=edge_color)

        ##############################################################################################
        ##############################################################################################

        start_activities_to_include = [act for act in start_activities if act in activities_map]
        end_activities_to_include = [act for act in end_activities if act in activities_map]

        if start_activities_to_include:
            viz.node("@@startnode", "@@S", style='filled', shape='circle', fillcolor="#32CD32", fontcolor="#32CD32")
            for act in start_activities_to_include:
                viz.edge("@@startnode", activities_map[act])

        if end_activities_to_include:
            viz.node("@@endnode", "@@E", style='filled', shape='circle', fillcolor="#FFA500", fontcolor="#FFA500")
            for act in end_activities_to_include:
                viz.edge(activities_map[act], "@@endnode")

        viz.attr(overlap='false')
        viz.attr(fontsize='11')

        viz.format = image_format

        return viz

    def __apply(self, dfg, log=None, parameters=None, activities_count=None, measure="frequency"):
        if parameters is None:
            parameters = {}

        activity_key = parameters[
            PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY

        image_format = "png"
        max_no_of_edges_in_diagram = 100

        if "format" in parameters:
            image_format = parameters["format"]
        if "maxNoOfEdgesInDiagram" in parameters:
            max_no_of_edges_in_diagram = parameters["maxNoOfEdgesInDiagram"]
        if "ping_pong_thresh" in parameters:
            ping_pong = parameters["ping_pong_thresh"]
        else:
            ping_pong = 100
        if "cycle_thresh" in parameters:
            cycle_thresh = parameters['cycle_thresh']
        else:
            cycle_thresh = 100

        start_activities = parameters["start_activities"] if "start_activities" in parameters else []
        end_activities = parameters["end_activities"] if "end_activities" in parameters else []

        if activities_count is None:
            if log is not None:
                activities_count = attributes_filter.get_attribute_values(log, activity_key, parameters=parameters)
            else:
                activities = dfg_utils.get_activities_from_dfg(dfg)
                activities_count = {key: 1 for key in activities}

        return self.__graphviz_visualization(activities_count, dfg, image_format=image_format, measure=measure,
                                             max_no_of_edges_in_diagram=max_no_of_edges_in_diagram,
                                             start_activities=start_activities, end_activities=end_activities,
                                             ping_pong_thresh=ping_pong, cycle_thresh=cycle_thresh)
