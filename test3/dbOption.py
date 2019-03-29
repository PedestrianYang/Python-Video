import pymysql
class DBManager():
    def __init__(self):
        #打开数据库连接
        self.db = pymysql.connect("localhost","root","root","test" )
    def close(self):
        self.db.close()

class Dao():
    def __init__(self):
        self.dbm = DBManager()

    def selectAllData(self):
        cursor = self.dbm.db.cursor()
        selectSql = "select * from user_t"
        dataArr = []
        try:
            cursor.execute(selectSql)
            result = cursor.fetchall()
            for row in result:
                dic = {'id':row[0], 'name':row[1], 'pwd':row[2], 'age':row[3]}
                dataArr.append(dic)
        except:
            print ("Error: unable to fetch data")

        return dataArr

    def insertPerson(self, person):
        cursor = self.dbm.db.cursor()
        insertSql = "insert into user_t (id, user_name, password, age) values (%s, %s, %s, %s)" % (person['id'], person['name'],person['pwd'],person['age'])
        try:
            cursor.execute(insertSql)
            self.dbm.db.commit()
        except:
            print('插入失败')



if __name__ == '__main__':
    dao = Dao()
    data = dao.selectAllData()
    print(data)