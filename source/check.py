import json
import os

class PositionCheck:
    def __init__(self) -> None:
        pass

    def Check(self):
        path=os.path.split(os.path.realpath(__file__))[0]
        with open(os.path.join(path, 'holding.json')) as f:
            totalValue=0
            currentHolding=json.load(f)
            for single in currentHolding['holding']:
                code = single['code']
                number= float(single['number'])
                price= float(single['price'])
                totalValue = totalValue+ number* price
            
            cash = float(currentHolding['cash'])
            totalValue= totalValue+ cash

            totalPosition=(totalValue-cash)*100/totalValue
            self.CheckTotalPosition(totalPosition)

            for single in currentHolding['holding']:
                code = single['code']
                number= float(single['number'])
                price= float(single['price'])

                singlePosition= number*price*100/totalValue
                self.CheckSinglePosition(code, singlePosition)
        return True
    
    ## 整体仓位检测
    def CheckTotalPosition(self,totalPosition):
        if self.GetBondSpread()-20 > totalPosition:
            print("警告：整体仓位过高，当前仓位：%d%%"%totalPosition)
        return True

    ## 个股持仓检测
    def CheckSinglePosition(self, code, singlePosition):
        if singlePosition > 30:
            print("警告：个股%s 仓位过高，当前仓位：%d%%"%(code,singlePosition))
        return True


    ## 获取股债利差百分位
    def GetBondSpread(self):
        return 80