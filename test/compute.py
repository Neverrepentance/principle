import os
import pandas as pd
from avg_compute import Compute_Avg

class stock_compute:
    file_name = ""

    # 初始现金
    cash_number = 100000

    # 持有股票, 单位 1手 = 100股
    stock_number = 0

    # 下一个交易日动作，0 - 不做任何动作，1 - 最大买入，2 - 清仓
    next_action = 0

    pre_max = 0.0

    max_drop = 0.0


    def __init__(self, stock_histry_file) -> None:
        self.file_name = stock_histry_file
        self.avg_5 = Compute_Avg(5)
        self.avg_10 = Compute_Avg(10)
        self.avg_20 = Compute_Avg(20)

    def compute(self):
        self.data = pd.read_csv(self.file_name, sep=',', header='infer',usecols=[0,2,3,5,7])
        datalen = len(self.data)
        self.idx = 0
        for self.idx  in range(datalen):
            volume = int(self.data['volume'][self.idx])
            if volume < 1 :
                continue
            close_price = float(self.data['close'][self.idx])
            open_price = float(self.data['open'][self.idx])
            self.compute_average(close_price)
            # 10天以内均线值还不正常
            if self.idx < 20:
                continue

            # 执行交易动作后，根据当天收盘价还可以计算下一个交易日的交易动作    
            ## 交易量超过1万股才有交易机会
            if volume > 10000:
                self.compute_income(self.data['date'][self.idx],open_price)

            # 计算买点、卖点后，只有下一个交易日才能动作
            if self.stock_number > 0 :
                self.compute_sale_point(close_price)
            else:
                self.compute_buy_point()

    def get_result(self):
        ## 获取最后数据
        income = (self.cash_number - 100000)/100000
        return income, self.max_drop

    
    def compute_income(self, action_date, price):
        ## 计算最后收益，计算最大回撤
        # 买入、卖出交易动作均按当天的开盘价进行
        if self.next_action == 1:
            assert self.stock_number == 0
            # 1手的价格
            price_100 = price* 100
            self.stock_number =  int(self.cash_number / price_100)
            # 手续费
            charge = self.stock_number * price_100 * 0.001
            if charge < 5:
                charge = 5
            self.cash_number = self.cash_number  - self.stock_number * price_100 - charge
            print("%s Avg5 %.2f > Avg10 %.2f,  买入 %d 手，价格：%.2f"%(action_date, self.avg_5.history[2], \
                                                                self.avg_10.history[2], self.stock_number, price))
        elif self.next_action == 2: 
            assert self.stock_number > 0
            price_100 = price* 100
            charge = self.stock_number * price_100 * 0.001
            if charge < 5:
                charge = 5
            self.cash_number = self.cash_number  + self.stock_number * price_100 - charge
            print("%s Avg5 %.2f < Avg10 %.2f,  卖出 %d 手，价格：%.2f, 总资产：%.2f"%(action_date, self.avg_5.history[2], \
                                                                self.avg_10.history[2], self.stock_number, price, self.cash_number))
            self.stock_number = 0            

        self.next_action = 0
        
        ## 最高收益
        if self.cash_number > self.pre_max:
            self.pre_max = self.cash_number

        ## 最高回撤
        if (self.pre_max - self.cash_number) / self.pre_max * 100 > self.max_drop :
            self.max_drop = (self.pre_max - self.cash_number) / self.pre_max * 100


    def compute_buy_point(self):
        ## 计算买点

        # MA5 必须大于 MA20
        if(self.avg_5.history[2] < self.avg_20.history[2]):
            return
        
        # MA10 必须上行
        if(self.avg_10.history[1] > self.avg_10.history[2]):
            return

        # MA5 必须上穿 MA10
        if ((self.avg_5.history[0] < self.avg_10.history[0]) or (self.avg_5.history[1] < self.avg_10.history[1]))  \
            and (self.avg_5.history[2] > self.avg_10.history[2]) :
            self.next_action = 1

    def compute_sale_point(self, close_price):
        ## 计算卖点
        if ((self.avg_5.history[0] > self.avg_20.history[0]) or (self.avg_5.history[1] > self.avg_20.history[1]))  \
            and (self.avg_5.history[2] < self.avg_20.history[2]) :
            self.next_action = 2
            return
        
        
        # max_in_3days = float(self.data['high'][self.idx-2])  if float(self.data['high'][self.idx-2]) > float(self.data['high'][self.idx-1]) else float(self.data['high'][self.idx-1])
        # max_in_3days = max_in_3days if max_in_3days > float(self.data['high'][self.idx]) else float(self.data['high'][self.idx])
        
        # if (max_in_3days * 0.97 > close_price) and (close_price < self.data["close"][self.idx -1]):
        #     self.next_action = 2

    def compute_average(self, close_price):
        ## 计算均线        
        self.avg_5.new_value(close_price)
        self.avg_10.new_value(close_price)
        self.avg_20.new_value(close_price)