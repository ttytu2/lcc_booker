## 1.8.1     - 2018-07-24 by zongzekun
* [Features]
  1. 无

* [Bugfixed]
  1. 修复等待元素问题

* [Configuration]
  1. 无


## 1.8.0     - 2018-07-24 by 李帅
* [Features]
  1. 9c增加跳价容错配置

* [Bugfixed]
  1. 无

* [Configuration]
  1. 新增跳价容错配置
  ```
    [carrier9C]
    jumpPrice=5
  ```


## 1.7.1     - 2018-07-24 by zongzekun
* [Features]
  1. 无

* [Bugfixed]
  1. 修复等待时间问题

* [Configuration]
  1. 无

## 1.7.0     - 2018-07-23 by chenhao/zongzekun
* [Features]
  1. 增加IT占座

* [Bugfixed]
  1. 无

* [Configuration]
  1. 无

## 1.6.3 - 2018-07-18 by lishuai
* [Features]
  1. 无

* [Bugfixed]
  1. 修复9C预订不可点击

* [Configuration]
  1. 无

## 1.6.2 - 2018-07-17 by lishuai
* [Features]
  1. 无

* [Bugfixed]
  1. 修复9C预订不可点击

* [Configuration]
  1. 无

## 1.6.1 - 2018-07-16 by lishuai
* [Features]
  1. 无

* [Bugfixed]
  1. 修复9C输入乘客信息时错误

* [Configuration]
  1. 无

## 1.6.0 - 2018-07-16 by lishuai
* [Features]
  1. 兼容官网新占坐流程

* [Bugfixed]
  1. 无

* [Configuration]
  1. 无

## 1.5.0 - 2018-07-12 by lishuai
* [Features]
  1. 1.5.0
  2. 分离帐号被封和乘客重复生单

* [Bugfixed]
  1. 修复根据价格选坐错误

* [Configuration]

## 1.4.0 - 2018-05-23 by wangxiaoyue
* [Features]
  1. 1.4.0
  2. 根据网页的改变修复下单

* [Bugfixed]
  1. 增加支付页面变更的逻辑判断
  2. 修复网页中js无法实现的问题
  3. 增加航空指南窗口的逻辑判断
  4. 修正选择最便宜价格的逻辑判断
  5. 写入乘客信息填写中的追加信息模块
  6. 规范代码
* [Configuration]

## 1.3.0 - 2018-05-17 by yuzhigang
* [Features]
  1. 增加9C的超时配置
  2. 增加刷新配置API：/lcc/booker/refresh

* [Bugfixed]

* [Configuration]

```
[carrier9C]
waitTimeout=60
```

## 1.2.0 - 2018-05-15 by yuzhigang
* [Features]
  1. 增加异常的打印

* [Bugfixed]
  
* [Configuration]


## 1.1.0 - 2018-05-03 by 宗泽坤
* [Features]
  1. 1.1.0
  2. 集成ZE下单

* [Bugfixed]
  1. 修改多人信息填写逻辑（修改本身容易出现儿童、成人信息填写反转错误）
  
* [Configuration]
  1. 配置文件 /data/config/lcc-booker/config.properties 新增加内容
  
  ```    
    [eastarjet]
    account=J18523400994
    password=zengjing!@#123
    # eastarjet填写信息前加载等待时间
    time=35
  ```

## 1.0.1 - 2018-04-28 by 宗泽坤
* [Features]
  1. 1.0.1

* [Bugfixed]
  1. 修复每次连接都新建数据库连接池BUG
  2. 谷歌浏览器兼容性问题（谷歌浏览器需要窗口最大化操作9C下单）
  
* [Configuration]

## V1.0.0 - 2018-04-27 by 宗泽坤
* [Features]
  1. 1.0.0

* [Bugfixed]
  1. 无

* [Configuration]
  1. 新增配置 /data/config/lcc-booker/config.properties

  ```
    [server]
    port=9001
    [browser]
    chromedriver=/opt/google/chrome/chromedriver
    [linkManInfo]
    name=JINGJING
    phone=18996166498
    email=lianfenghangbian@163.com
    [datasource]
    # 数据库信息
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DBNAME=lcc
    DB_USER=root
    DB_PASSWORD=
    
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

* [DB]

  1. 新建数据库表account_9c
  
  ```
  -- 9C账号表
    CREATE TABLE account_9c
    (
      id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(30) NULL COMMENT '9C账号',
      password VARCHAR(30) NULL COMMENT '密码',
      gmt_creat DATETIME NULL COMMENT '创建时间',
      gmt_modified DATETIME NULL COMMENT '更新时间',
      is_disabled  TINYINT UNSIGNED DEFAULT '0' NULL COMMENT '用户状态（1：封号、0：未封号）',
      CONSTRAINT account_9c_username_uindex UNIQUE (username)
    ) ENGINE = InnoDB;

  ```
