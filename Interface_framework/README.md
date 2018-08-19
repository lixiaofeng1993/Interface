
```
Interface_framework 目录
requests + ddt + unittest 框架

case
    test_api
        数据驱动,测试用例;
common  公共函数
    base_api
        requests请求,结果写入excel;
    connectDB
        连接数据库,返回 dict 和str;
    HTMLTestRunner
        美化report报告;
    logger
        日志模块;
    readConfig
        读取配置文件;
    readExcel
        读取excel数据,返回 多个 dict 组成的 list ;
    readJson
        读取json数据;
    writeExcel
        复制excel 写入excel 加样式;
config
    cfg.ini
        配置文件;
data
    data.json
        请求需要的参数,支持数据库查询;
    demo_api.xlsx
        存放请求url等信息;
logs
    存放 log 日志;
report
    存放结果报告和excel;
run_this
    生成报告,发送 email;


2018.05.15  去掉配置文件中固定的case路径，使用os模块，适用更多场景;
            修改 connectDB.py execute_sql()方法支持删除操作;
2018.05.16  增加上下文依赖，判断接口返回参数，写入对应的json文件中，做下次请求使用；processingJson.py analysis_json() write_body()
2018.06.02  body参数为dict时，使用sql替换参数值;
            body参数支持类型为list时，使用sql替换参数为值;

2018.08.05  签到小程序接口更新，执行时需要修改配置文件中的 unionid 值；

2018.08.19  添加 content_id 随机值;
            新增过期日志删除机制;

```
