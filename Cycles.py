import numpy as np


def get_ping_pong(dataframe, thresh=30):
    ping_pong_edges = set(())
    ping_dict = {}
    df = dataframe
    index = list(dataframe.columns).index('concept:name')
    for i in range(df.shape[0] - 2):
        if df.iloc[i, index] == df.iloc[i + 2, index]:
            key = df.iloc[i, index] + df.iloc[i + 1, index]
            key_two = df.iloc[i + 1, index] + df.iloc[i, index]
            if key in ping_dict.keys():
                ping_dict[key][0] += 1
            elif key_two in ping_dict.keys():
                ping_dict[key_two][0] += 1
            else:
                ping_dict[key] = [1, (df.iloc[i, index], df.iloc[i + 1, index]), (df.iloc[i + 1, index], df.iloc[i, index])]
    for key in ping_dict.keys():
        if ping_dict[key][0] > thresh:
            ping_pong_edges.add(ping_dict[key][1])
            ping_pong_edges.add(ping_dict[key][2])
    return list(ping_pong_edges)


def find_cycles(dataframe, thresh=30):
    temp_cycle = {}
    cycle_edges = []
    cases = np.unique(dataframe[:]['case:concept:name'].tolist())
    index = list(dataframe.columns).index('concept:name')
    for i in range(len(cases)):
        df = dataframe[dataframe[:]['case:concept:name'] == cases[i]]
        j = 0
        while j < df.shape[0]:
            searching_name = df.iloc[j, index]
            temp_edges = []
            for k in range(0, df.shape[0] - 1 - j):
                temp_edges.append((df.iloc[j + k, index], df.iloc[j + k + 1, index]))
                if df.iloc[j + k + 1, index] == searching_name and k > 2:
                    if (df.iloc[j, index] + df.iloc[j + k, index]) not in temp_cycle.keys():
                        temp_cycle[df.iloc[j, index] + df.iloc[j + k, index]] = [1, temp_edges]
                    else:
                        temp_cycle[df.iloc[j, index] + df.iloc[j + k, index]][0] += 1
                    break
            j += 1
        for key in temp_cycle.keys():
            cycle_edges.append(temp_cycle[key][1])
    return list(cycle_edges)
