from flask import Flask, render_template, request
import pymysql

# 只创建一个 app，原来这里重复写了两次 app = Flask(__name__)，第一个 app 上的路由会失效
app = Flask(__name__)


#这个@用来添加新功能
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    un = request.form['un']
    pd = request.form['pd']
   
   #这里直接插入了一段pycharm链接数据库的程序
    # 1.Connection Open
    conn = pymysql.connect(user='root', password='root', database='login')

    # 2.Cursor Creating:
    cursor = conn.cursor()

    # 3.SQL Execution 这里注意把数据库里的量改成上面定义的变量“un”
    sqlstr = 'select * from customer where customer_name="'+un+'" and customer_pwd="'+pd+'"'

    # 4.Cursor Moving
    cursor.execute(sqlstr)
    numrows = len(cursor.fetchall())
    conn.commit()

    # 5.Connection Close
    cursor.close()
    conn.close()

    # get data from request：
    if numrows > 0:
        return('Hello, '+un+'! ')  #这里也改一下变量
    else:
        return('Hi!You are wrong! ')

############################################


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''    # msg用来传给前端显示，用这个功能可以实现注册完之后显示注册成功之类的

    if request.method == 'POST':
        un1 = request.form['un1']
        pd1 = request.form['pd1']
        pd2 = request.form['pd2']

        if not un1 or not pd1:
            msg = 'Username and password cannot be empty!'
        elif pd1 != pd2:
            msg = 'Two passwords do not match!'
        else:
            conn = pymysql.connect(user='root', password='root', database='login')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM customer WHERE customer_name=%s', (un1,))
            if cursor.fetchone():
                msg = 'Username already exists!'
            else:
                cursor.execute(
                    'INSERT INTO customer (customer_name, customer_pwd) VALUES (%s, %s)',
                    (un1, pd1)   # 原来写成 pwd_hash(pd1)，但 pwd_hash 根本没定义，会报 NameError
                )
                conn.commit()
                msg = 'Register success!'
            cursor.close()
            conn.close()

    # 原来写的是 render_template('register.html', msg=msg)，
    # 但 templates 目录里没有 register.html，会报 TemplateNotFound（页面显示找不到/未知页面）
    # index.html 里已经有注册表单和 msg 显示位置，直接渲染 index.html 即可
    return render_template('index.html', msg=msg)

if __name__=='__main__':
    app.run()
