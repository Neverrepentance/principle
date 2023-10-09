import sys
from check import PositionCheck

def main(args):
    ## 仓位检查
    check=PositionCheck()
    check.Check()

    ## 持仓股票检测

    ## 股票筛选



if __name__ == '__main__':
    args=sys.argv
    main(args)