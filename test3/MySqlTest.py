import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )


# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO Video(NAME,IMAGEURL, DOWNLOADURL)  VALUES ('享受硬屌用力抽插的美人妻', 'https://www.fcww11.com/contents/videos_screenshots/38000/38886/180x135/5.jpg',  'https://www.fcww11.com/videos/38886/24d462b8558d399a6da183512812aa04/')"
try:
    # 执行sql语句
    cursor.execute(sql)
    # 执行sql语句
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

# 关闭数据库连接
db.close()


