from Bottleneck import Bottleneck
from Cycles import get_ping_pong, find_cycles
from Depth import Depth


class Analyzer:
    def __init__(self, parent, value=5):
        self.value = value
        self.parent = parent

    def analyze(self, data):
        res = []
        tmp = Bottleneck(data)
        depth = Depth(self.parent, self)
        depth.wait_window()
        print(self.value)
        print('ok')
        print(type(tmp))
        try:
            res.append(tmp[:int(self.value)])
        except:
            res.append(tmp)
        tmp = get_ping_pong(data)
        try:
            res.append(tmp[:int(self.value)])
        except:
            res.append(tmp)
        tmp = find_cycles(data)
        try:
            res.append(tmp[:int(self.value)])
        except:
            res.append(tmp)
        print(res)
