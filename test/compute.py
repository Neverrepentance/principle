import os
import pandas as pd

class stock_compute:
    file_name = ""

    # 初始现金
    cash_number = 10000

    # 持有股票, 单位 1手 = 100股
    stock_number = 0

    # 下一个交易日动作，0 - 不做任何动作，1 - 最大买入，2 - 清仓
    next_action = 0

    last_5 = [0] * 5
    avg_5 = 0.0
    total_5 = 0.0
    last_5_idx = 0
    avg_5_history = [0] * 3

    last_10 = [0] * 10 
    avg_10 = 0.0
    total_10 = 0.0
    last_10_idx = 0
    avg_10_history = [0] * 3


    def __init__(self, stock_histry_file) -> None:
        self.file_name = stock_histry_file

    def compute(self):
        data = pd.read_csv(self.file_name, sep=',', header='infer',usecols=[1,2])
        for i in range(len(data)):
            price = float(data['close'][i])
            self.compute_average(price)
            # 10天以内均线值还不正常
            if i < 10:
                continue

            # 执行交易动作后，根据当天收盘价还可以计算下一个交易日的交易动作    
            self.compute_income(price)

            # 计算买点、卖点后，只有下一个交易日才能动作
            if self.stock_number > 0 :
                self.compute_sale_point()
            else:
                self.compute_buy_point()

            

    
    def compute_income(self, price):
        ## 计算最后收益，计算最大回撤
        # 买入、卖出交易动作均按当天的开盘价进行
        if self.next_action == 1:
            assert self.stock_number == 0
            # 1手的价格
            price_100 = price* 100
            self.stock_number =  int(self.cash_number / price_100)
            self.cash_number = self.cash_number  - self.stock_number * price_100
        elif self.next_action == 2: 
            assert self.stock_number > 0
            price_100 = price* 100
            self.cash_number = self.cash_number  + self.stock_number * price_100
            self.stock_number = 0



    def compute_buy_point(self):
        ## 计算买点
        if (self.avg_5_history[0] < self.avg_10_history[0] or self.avg_5_history[1] < self.avg_10_history[1])  \
            and self.avg_5_history[2] > self.avg_10_history[2] :
            self.next_action = 1

    def compute_sale_point(self):
        ## 计算卖点
        if (self.avg_5_history[0] > self.avg_10_history[0] or self.avg_5_history[1] > self.avg_10_history[1])  \
            and self.avg_5_history[2] < self.avg_10_history[2] :
            self.next_action = 2

    def compute_average(self, close_price):
        ## 计算均线        
        print('计算均线')
        self.total_5 = self.total_5 - self.last_5[self.last_5_idx] + close_price
        self.avg_5 = self.total_5 / 5
        self.last_5[self.last_5_idx] = close_price
        self.last_5_idx = (self.last_5_idx + 1) % 5
        self.avg_5_history[0] = self.avg_5_history[1]
        self.avg_5_history[1] = self.avg_5_history[2]
        self.avg_5_history[2] = self.avg_5

        
        self.total_10 = self.total_10 - self.last_10[self.last_10_idx] + close_price
        self.avg_10 = self.total_10 / 10
        self.last_10[self.last_10_idx] = close_price
        self.last_10_idx = (self.last_10_idx + 1) % 10
        self.avg_10_history[0] = self.avg_10_history[1]
        self.avg_10_history[1] = self.avg_10_history[2]
        self.avg_10_history[2] = self.avg_10