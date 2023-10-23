import baostock as bs
import pandas as pd
import os
import datetime

class mybaostock:
    stock_list = "./stock/hs300_stocks.csv"

    def __init__(self) -> None:
        try:
            self.lg = bs.login()
            # 显示登陆返回信息
            print('login respond error_code:'+ self.lg.error_code)
            print('login respond  error_msg:'+ self.lg.error_msg)
        except Exception as e:
            print("baostack exception")
            print(e)
    
    def get_stock_list(self):
        now_time = datetime.datetime.now()
        days_befor_7 = now_time - datetime.timedelta(days=7)

        ## 沪深300成分股更新时间
        t = os.path.getmtime(self.stock_list)
        file_time = datetime.datetime.fromtimestamp(t)
        if(file_time > days_befor_7):
            print("not need to update, last get on "+ str(file_time))
            return

        # 获取沪深300成分股
        rs = bs.query_hs300_stocks()
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            hs300_stocks.append(rs.get_row_data())
        result = pd.DataFrame(hs300_stocks, columns=rs.fields)
        # 结果集输出到csv文件
        result.to_csv(self.stock_list, encoding="utf-8", index=False)


    def get_all_history(self):
        try:
            now_str = datetime.date.today().isoformat()
            start_str = datetime.date(year=2015,month=1,day=1).isoformat()
            data = pd.read_csv(self.stock_list, sep=',', header='infer',usecols=[1,2])
            for i in range(len(data)):
                file_exists = False
                code = str(data['code'][i])
                file_name = './stock/'+ code +"_history.csv"
                if os.path.exists(file_name):
                    t = os.path.getmtime(file_name)
                    file_time = datetime.date.fromtimestamp(t)
                    if file_time >= datetime.date.today():
                        continue
                    start_str = file_time.isoformat()
                    file_exists = True

                #### 获取沪深A股历史K线数据 ####
                # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
                # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
                # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
                rs = bs.query_history_k_data_plus(code,
                    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                    start_date=start_str, end_date=now_str,
                    frequency="d", adjustflag="3")
            

                #### 打印结果集 ####
                data_list = []
                while (rs.error_code == '0') & rs.next():
                    # 获取一条记录，将记录合并在一起
                    data_list.append(rs.get_row_data())
                result = pd.DataFrame(data_list, columns=rs.fields)

                #### 结果集输出到csv文件 ####   
                if file_exists:
                    result.to_csv(file_name, mode='a', header=False, index=False)
                else:
                    result.to_csv(file_name, index=False)
        except Exception as e:
            print("baostack exception")
            print(e)