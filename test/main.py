import sys
from mybaostock import mybaostock
from compute import stock_compute

def main(args):
    ## 更新股票数据
    # mybs = mybaostock()
    # mybs.get_stock_list()
    # mybs.get_all_history()

    ## 计算收益
    cp = stock_compute('./stock/sh.600000_history.csv')
    cp.compute()
    income, max_drop = cp.get_result()
    print('收益率：%.2f, 最大回撤:%.2f'%(income, max_drop) )

if __name__ == '__main__':
    args=sys.argv
    main(args)