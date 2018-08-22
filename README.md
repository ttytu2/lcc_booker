![worthytrip](http://docs.worthytrip.com:4000/style/images/logo-liberxue.png)

###config

```
[server]
port=9001
[browser]
#chromedriver=/opt/google/chrome/chromedriver
chromedriver=/data/opt/python/chromedriver
[linkManInfo]
name=JINGJING
phone=18996166498
email=lianfenghangbian@163.com

[eastarjet]
account=J18523400994
password=zengjing!@#123
# eastarjet填写信息前加载等待时间
time=35

[carrier9C]
waitTimeout=60

[datasource]
# 数据库信息
#DB_HOST=
DB_HOST=
DB_PORT=3306
DB_DBNAME=
DB_USER=
DB_PASSWORD=



#DB_HOST=127.0.0.1
#DB_PORT=3306
#DB_DBNAME=lcc
#DB_USER=root
#DB_PASSWORD=

# 数据库连接编码
DB_CHARSET=utf8
# mincached : 启动时开启的闲置连接数量(缺省值 0 以为着开始时不创建连接)
DB_MIN_CACHED=10
# maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
DB_MAX_CACHED=10
# maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
DB_MAX_SHARED=20
# maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
DB_MAX_CONNECYIONS=100
# blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......> 其他代表阻塞直到连接数减少,连接被分配)
DB_BLOCKING=True
# maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
DB_MAX_USAGE=0
# setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
DB_SET_SESSION=None
```

## 初始版本 API- 2018-04-20 by 宗泽坤
### 接口请求地址
- port=9001 
- 127.0.0.1:9001/lcc/booker

### 说明

- ZE航司相对下单较慢（测试），具体时间在110秒左右

### 请求json格式

> fromSegments下最重要的信息flightNumber（航班号）

> 其中adultNumber以及childNumber数量要对应passengers下有多少条数据

> creditCardInfo为ZE航司需要付款的信用卡信息（其他航司不用提供） 

> 除了特殊说明 其他参数和生单接口一致

    {
      "adultNumber": "1",
      "adultPrice": 490,
      "adultTax": 144,
      "childNumber": "0",
      "childPrice": 0,
      "childTax": 0,
      "ds": "9C_F",
      "ipcc": "9C_F",
      "flightOption": "oneWay",   //单程（oneWay）和往返(roundTrip)
      "startTime": "2018-06-06",
      "endTime": "",
      "toCity": "HKG",
      "fromCity": "SHA",
      "creditCardInfo":{
        "cardNumber":"6226 8988 8888 8888",
        "cvv":"123",
  	    "name":"CHINA EASYTRAVEL",
        "validityPeriod":"02/2021"
      },
      "fromSegments": [
        {
          "arrAirport": "HKG",
          "arrTime": "2017-06-06 12:20:00",
          "cabin": "Q",
          "carrier": "LX",
          "codeShare": false,
          "depAirport": "SHA",
          "depTime": "2018-06-06 09:20:00",
          "flightNumber": "9C8921",
          "marriageGrp": "",
          "stopAirports": "",
          "stopCities": ""
        }
      ],
      "retSegments": [],
      "passengers": [
        {
          "ageType": 0,
          "birthday": "1992-05-28",
          "cardExpired": "2031-06-06",
          "cardIssuePlace": "CN",
          "cardNum": "E12345678",
          "cardType": "PP",
          "firstName": "JINGYI",
          "gender": "F",
          "lastName": "TIAN",
          "name": "TIAN/JINGYI",
          "nationality": "CN"
        }
      ]
    }

### 接口返回

> 状态码返回为0 代表生单成功 （9C包括应付金额 订单编号 以及下单成功的账号密码） 


    {
        "status": "0", 
        "message": "Order successfully created", 
        "orderNumber": "SDEAJX", 
        "orderPrice": "534", 
        "orderUsername": "123456@126.com", 
        "orderPassword": "123456"
    }
    
> 状态码返回为1 代表未找到匹配的航班号


    {
        "status": "1", 
        "message": "No flight number found"
    }
    
> 状态码返回为2 代表填写乘客信息出现错误


    {   
        "status": "2", 
        "message": "Passenger information is wrong"
    }
    
> 状态码返回为3 代表确认航班出现错误


    {
        "status": "3", 
        "message": "Confirm the order is wrong"
    } 
    
> 状态码返回为4 代表有重复订单或账号被封


    {
        "status": "4", 
        "message": "Account blocked"
    }
       
> 状态码返回为5 代表支付出现错误


    {
        "status": "5", 
        "message": "Payment exception"
    }
> 状态码返回为6 代表支付出现错误
    {
        "status": "6", 
        "message": "当前旅客不可预定当前航班"
    }