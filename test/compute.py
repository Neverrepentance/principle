import os
import pandas as pd

class stock_compute:
    file_name = ""

    def __init__(self, stock_histry_file) -> None:
        self.file_name = stock_histry_file

    def compute(self):
        data = pd.read_csv(self.file_name, sep=',', header='infer',usecols=[1,2])
l
    
    def compute_income(self):
        ## 计算最后收益，计算最大回撤

    def compute_buy_point(self):
        ## 计算买点

    def compute_sale_point(self):
        ## 计算卖点

    def compute_average(self):
        ## 计算均线