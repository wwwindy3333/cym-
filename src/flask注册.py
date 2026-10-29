from flask import Flask, render_template
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask import request

app = Flask(__name__)
@app.route('/')
def hello_world():
    return '''
    <center><b><font color="red">Hello World!</font></b></center>
    <form action="/login" method="post">
    Name:<input type="text" name="un">
    Password:<input type="password" name="pd">
    <input type="submit" name="Submit">
    </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    un = request.form['un']
    pd = request.form['pd']
    # 1.Connection Open
    conn = pymysql.connect(user='root', password='root', database='login')

    # 2.Cursor Creating:
    cursor = conn.cursor()

    # 3.SQL Execution
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
        return('Hello, '+un+'! ')
    else:
        return('Hi!You are wrong! ')


if __name__=='__main__':
    app.run()
