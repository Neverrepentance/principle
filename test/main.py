import sys
from mybaostock import mybaostock

def main(args):
    mybs = mybaostock()
    mybs.get_stock_list()
    mybs.get_all_history()


if __name__ == '__main__':
    args=sys.argv
    main(args)