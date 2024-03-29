'''
login.py
登录 注册
'''
import pymysql
class User:
    def __init__(self,database):
        self.db = pymysql.connect(
            user='root',
            password='123456',
            database=database,
            charset='utf8'
        )
        self.cur = self.db.cursor()

    def register(self,name,passwd):
        sql = "select*from user where name=%s"
        self.cur.execute(sql,[name])
        r = self.cur.fetchone()
        if  r:
            return False
        sql = "insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()

    def login(self,name,passwd):
        sql = "select * from user where name = %s and passwd = %s"
        self.cur.execute(sql,[name,passwd])
        r=self.cur.fetchone()
        if r:
            return True
        return False


if __name__ == '__main__':
    name = input('Name:')
    passwd = input('Password:')

    user = User('stu')

    # if user.register(name,passwd):
    #     print('注册成功')
    if user.login(name,passwd):
        print('登录成功')