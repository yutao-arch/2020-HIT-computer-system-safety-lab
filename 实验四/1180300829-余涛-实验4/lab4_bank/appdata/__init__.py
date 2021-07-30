# 固定写法
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)   # 指定版本
pymysql.install_as_MySQLdb()  # 告诉django用pymysql代替mysqldb连接数据库