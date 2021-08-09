from flask import Flask, render_template, request, redirect,url_for,jsonify
import pymysql,random,datetime,json
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    
    return render_template('index.html')




@app.route('/userlogin',methods=['GET','POST'])
def student():
    return render_template('userlogin.html')
@app.route('/userupdate',methods=['GET','POST'])
def userupdate():
    

    if request.method=="POST":
        who=request.values['who']
        
        conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='books',
                charset='utf8'
                )

        #亂數電話
        phone='09'
        for i in range(8):
            other=random.choice("1234567890")
            phone=phone+other

        conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='books',
                charset='utf8'
                )
        #模擬會員
        cur=conn.cursor()
        sql="insert into borrower(name,phone) values('"+who+"','"+phone+"');"
        cur.execute(sql)
        conn.commit()
        cur.close()     


        return redirect(url_for('select',who=who),code=307)
    else:    
        return render_template('userlogin.html')


    

@app.route('/userselect/<who>',methods=['GET','POST'])
def select(who):
    if request.method == "POST":
        conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='books',
                charset='utf8'            
                )
        cur=conn.cursor()
        sql="select * from books"
        cur.execute(sql)
        content=cur.fetchall()
        sql= "select id from borrower order by id desc;"
        cur.execute(sql)
        userid=cur.fetchone()
        cur.close()



        return render_template('userselect.html',who=who,content=content,userid=userid)
    else:
        return render_template('userlogin.html')



@app.route('/check',methods=['GET','POST'])
def check():
    if request.method == "POST":
        who=request.values['who']         
        check=request.form.getlist('check')

        conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='books',
                charset='utf8'
                )
        #取會員編號error
        cur=conn.cursor()
        sql= "select id from borrower order by id desc;"
        cur.execute(sql)
        content=cur.fetchone()
        userid=content
        cur.close()
        userid=str(userid[0])
        print(userid)

        #書本租借
        cur=conn.cursor()
        for i in range(len(check)):
            sql="update books set now='借出' where id='"+check[i]+"';"
            cur.execute(sql)
        cur.close()
        conn.commit()


        #借出去的書
        today=datetime.date.today()
        back=today+datetime.timedelta(days=10)
        back=str(back)
        print(type(back))
        
        cur=conn.cursor()
        for i in range(len(check)):
            sql="insert into borrowerbook(bookid,userid,back)values('"+check[i]+"','"+userid+"','"+back+"');"
            cur.execute(sql)
        cur.close()
        conn.commit()

        return redirect(url_for('ub',userid=userid),code=307)
    else:
        return render_template('userlogin.html')


@app.route('/userborrower/<userid>',methods=['GET','POST'])
def ub(userid):

    
    conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='books',
            charset='utf8'
            )
    cur=conn.cursor()
    sql= "select books.id, books.name, books.types, borrowerbook.back from borrowerbook join borrower on borrower.id=borrowerbook.userid join books on books.id=borrowerbook.bookid where borrowerbook.userid='"+userid+"';"
    cur.execute(sql)
    content=cur.fetchall()
    sql="select name from borrower where id ='"+userid+"';"
    cur.execute(sql)
    name=cur.fetchone()
    cur.close()












    return render_template('userborrower.html',content=content,name=name)

@app.route('/ajax',methods=['GET','POST'])
def ajax():
    data = request.get_json('data')
    print (data['chose'])
    if data['chose']=="":
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='books',
            charset='utf8'
            )
        cur=conn.cursor()
        sql="select * from books;"
        cur.execute(sql)
        content=cur.fetchall()
        sql= "select name from borrower order by id desc;"
        cur.execute(sql)
        b=cur.fetchone()
        cur.close()
        who=b[0]
        return render_template('ajax.html',content=content,who=who)

    else:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='books',
            charset='utf8'
            )
        cur=conn.cursor()
        sql="select * from books where types='"+data['chose']+"';"
        cur.execute(sql)
        content=cur.fetchall()
        sql= "select name from borrower order by id desc;"
        cur.execute(sql)
        b=cur.fetchone()
        cur.close()
        who=b[0]
        return render_template('ajax.html',content=content,who=who)
    

@app.route('/book', methods=['GET','POST'])
def book():

    return render_template('insertbook.html')


@app.route('/bookinsert',methods=['GET','POST'])
def bookinsert():
    bid=request.values['id']
    name=request.values['name']
    btype=request.values['type']

    conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='books',
            charset='utf8'
            )
    cur=conn.cursor()
    sql="insert into books(id,name,now,types)values('"+bid+"','"+name+"','未借','"+btype+"');"
    cur.execute(sql)
    cur.close()
    conn.commit()

    return bid+name+btype


if __name__ == '__main__':
    app.debug = True
    app.run()
