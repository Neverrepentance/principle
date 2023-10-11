import requests
import urllib3

### 记录： 文件命名不能也包里的关键字相同，否则会报循环引用

urllib3.disable_warnings()
resp = requests.get("https://danjuanfunds.com/valuation-table/jiucai?channel=2500000074", verify=False)

print(resp.status_code)
print(resp.headers)