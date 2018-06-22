from pymongo import MongoClient
# 注册,传入用户名密码
def mongo1(name,passwd):
    # 创建数据库连接对象MongoClient 是pymongo库中的一个类
    conn = MongoClient('localhost',27017)
    # 生成数据库对象,生成集合对象
    db = conn['test']
    my_set = db['class0']
    # # 输入用户
    # name = input("请输入用户名:")
    # passwd = input("请输入密码:")

    # 查找某个域 查找用户是否存在
    # my_set = db.class0
    # cursor2 = my_set.find({'name':{'$size':0}},{'_id':0})
    # 返回name的游标
    cursor = my_set.find({},{"_id":0,'name':1})
    # cursor = my_set.find({},{"_id":0})
    #判断用户名密码是否存在的函数,如果不存在就执行插入函数
    def fun2():
        for i in cursor:
            if i['name'] == name:
                print(name,'已经存在,请直接登录')
                return 'F'
                # return 'F'
        else:
            fun1()
            print("注册成功")
            return 'T'
    #插入函数,插入新注册的用户名密码
    def fun1():
        insert_doc = dict()
        insert_doc['name']=name
        insert_doc['passwd']=passwd
        my_set.insert(insert_doc)
    return fun2()
    #删除所有文档
    # my_set.remove()
    conn.close()
# 登录,传入用户名密码
def mongo2(name,passwd):
    # 创建数据库连接对象MongoClient 是pymongo库中的一个类
    conn = MongoClient('localhost',27017)
    # 生成数据库对象,生成集合对象
    db = conn['test']
    my_set = db['class0']
    # 返回n游标
    cursor = my_set.find({},{"_id":0,'name':1,'passwd':1})

    def fun2():
        # 假如用户名为空,直接返回false
        if not name:
            return 'F'
        for i in cursor:
            # { "passwd" : "2", "name" : "c" }
            if i['name'] == name and i['passwd'] == passwd:
                print('登录成功')
                return 'T'
            elif i['name'] == name and i['passwd'] != passwd:
                print("登录失败,用户名存在，密码错误")
                return 'F'
        else:
            print("登录失败,用户名密码错误均不存在")
            return 'F'

    return fun2()

    conn.close()

if __name__ == '__main__':
    name = input("请输入用户名:")
    passwd = input("请输入密码:")
    mongo1(name,passwd)