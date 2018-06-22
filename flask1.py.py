#encoding:utf-8
#python3不需要
#从flask框架中导入Flask这个类
from flask import Flask,redirect,request,url_for
#导入重定向函数redirect,和url_for反转视图函数
#导入render_template,用于渲染html页面
from flask import render_template
# 导入数据库模块中的函数 mongo1注册,mongo2登录
from mongo1 import mongo1,mongo2
#导入爬虫模块-->火车票查询
import pacong
#导入爬虫模块-->天气查询
import weather
#初始化一个Flask对象
#需要传递一个参数__name__
#参数__name__的作用,1.方便flask框架去寻找资源,2.方便flask插件出现错误的时候,好去寻找问题所在位置
app = Flask(__name__)
#是一个装饰器
#装饰器的作用,是做一个url与视图函数的映射
#ip:port  ->>去请求index函数,然后吧结果返回给浏览器
#首页
@app.route('/')
def index():
    print('>>>>>>>>>>>>>首页')
    print('这是表单', request.form)
    # 调用render_template函数,跳转到index.html页面
    return render_template('index.html')
#注册函数
@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        print('>>>>>>>>>>>>>注册')
        username = request.form['username']
        psname = request.form['psname']
        psname1 = request.form['psname1']
        # 判断二次输入的密码是否相同
        if psname == psname1:
            # a=='T'成功 a=='F'失败  注册函数
            a = mongo1(username,psname)
            if a=='T':
                # 调用重定向函数redirect,作用是,用url_for反转函数并传入login视图函数,表示注册成功跳转到登录页面
                return redirect(url_for('login'))
            elif a=='F':
                # 注册失败,保留在注册页面
                return redirect(url_for('regist'))
        else:
            print('二次密码不相同')
            return redirect(url_for('regist'))
    return render_template('regist.html')
#登录函数
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print('>>>>>>>>>>>>>登录')
        #为了把用户名传到查询页面
        global username
        username = request.form['username']
        psname = request.form['psname']
        # mongo2 是登录数据库函数
        a = mongo2(username, psname)
        print(a)
        if a == 'T':
            # 跳转到inquire函数进行查询
            return redirect(url_for('inquire'))
        elif a == 'F':
            return redirect(url_for('login'))

    return render_template('login.html')
# 查询函数
@app.route('/inquire/',methods=['GET','POST'])
def inquire():
    if request.method == 'POST':
        #从页面通过表单form接收参数
        start = request.form['start']
        end = request.form['end']
        date = request.form['date']
        print(start,end,date)
        print(type(start), type(end),type(date))
        # 调用weather天气模块
        tianqi = weather.main(end,date)
        # 调用爬虫模块
        result = str(pacong.mian(date,start,end))
        print(end,'天气',tianqi,type(tianqi))
        print('车票信息结果的类型:',type(eval(result)))
        print('车票结果:', eval(result))
        dic ={
            'end':end,
            'tianqi':tianqi,
            'result':eval(result),
            'username':username
        }
        print("********",username)
        # 调用render_template函数,它会直接找templates这个文件夹,然后跳转到inquire.html页面(查询页面),传入封装成字典之后的参数
        #查询之后的页面
        return render_template('inquire.html',**dic)
        #return render_template('inquire.html',end1=u'%s'%end,result1=u'%s'%tianqi,result2=u'%s'%result)
    #查询的时候的页面
    return render_template('inquire.html')

#如果当这个文件是作为入口主程序,那么执行app.run()
if __name__ == '__main__':
    #启动一个应用服务器,来接收用户的请求,相当于如下:
    #while true:
    #listen()
    #传入debug参数的作用:
    # 1.当程序出现问题的时候,可以在页面中看到错误信息和出错的位置
    #2.只要修改了python文件,程序会自动加载,不需要手动重新启动服务器
    # app.run( debug=True)
    app.run(host='0.0.0.0', debug=True, port=8888)
