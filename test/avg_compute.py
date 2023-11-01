# 计算均值
class Compute_Avg:
    # 周期
    size = 0
    # 当前索引位置
    idx = 0
    # 
    total_sum = 0.0

    avg = 0.0

    def __init__(self, size) -> None:
        self.size = size
        # 不在__init__ 中定义的数组将成为公共数组
        # 最近3天的均值
        self.history = [0] * 3
        # 最近的数据
        self.last = []
        for i in range(size):
            self.last.append(0.0)

    def new_value(self, value):
        self.total_sum = self.total_sum - self.last[self.idx] + value
        self.avg = self.total_sum / self.size
        self.last[self.idx] = value
        self.idx = (self.idx + 1) % self.size
        self.history[0] = self.history[1]
        self.history[1] = self.history[2]
        self.history[2] = self.avg

    # 前复权
    def reduce_history(self, vlaue):
        for i in range(self.size):
            self.last[i] = self.last[i] - vlaue

        for i in range(3):
            self.history[i] = self.history[i] - vlaue
