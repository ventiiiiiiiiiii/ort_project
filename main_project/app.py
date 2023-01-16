from flask import Flask, render_template, url_for, request, redirect, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
import datetime
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy import func
import paypalrestsdk
import logging

app = Flask(__name__)
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AdA907COJwyafA6LEH4nJ9WD5PVEd_Iy9M2eM7JcGUa3qbi1sMAWWTOEf1I6_RyfRG8VFKlikIcMrDV6",
  "client_secret": "EP8q3hhTUMctffivtseL1T6Qfr5LNAHNzB9IDmPdf8dfam31M-zTkECYKRNwTaMASDtMk6C2xtMUvhdF" 
  })

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db' 
}

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    deadline = db.Column(db.DateTime)
    progress = db.Column(db.String(200))
    list_type = db.Column(db.String(200))
    userid = db.Column(db.String(200), nullable=False)
    # username = db.Column(db.int)

class Users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    isadmin = db.Column(db.Boolean, default= False, nullable= False)

    def __repr__(self):
        return 'User %r' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
        return redirect('/login')

@app.route('/daily_list/<username>/<key>', methods=['POST', 'GET'])
def daily(username, key):
    if request.method == 'POST':
        task_content = request.form['content']
        task_notes = request.form['notes']
        task_progress = request.form['progress']
        formatt = "%Y-%m-%d"
        try:
            task_deadline = datetime.datetime.strptime(request.form['deadline'], formatt)
        except:
            task_deadline = datetime.datetime.strptime('9999-9-9', formatt)
            new_task = Todo(content = task_content, notes = task_notes, deadline = task_deadline, progress = task_progress, list_type = 'daily_list', userid = key)
            db.session.add(new_task)    
            db.session.commit()
        if str(new_task.deadline) == '9999-09-09 00:00:00':
            print(new_task.deadline)
        return redirect(url_for('daily',username = username, key = key))
    else:
        tasks = Todo.query.filter_by(list_type='daily_list').order_by(Todo.date_created).all()
        users = Users.query.order_by(Users.id).all()
        blah = [3,2,3];
        return render_template('index.html', tasks = tasks,username = username, key = key,users = users)




@app.route('/urgent_list/<username>/<key>', methods=['POST', 'GET'])
def urgent(username, key):
    if request.method == 'POST':
        task_content = request.form['urgent_content']
        task_notes = request.form['notes']
        task_progress = request.form['progress']
        formatt = "%Y-%m-%d"
        try:
            task_deadline = datetime.datetime.strptime(request.form['deadline'], formatt)
            print(task_deadline)
        except:
            task_deadline = datetime.datetime.strptime('9999-9-9', formatt)
        new_task = Todo(content = task_content, notes = task_notes, deadline = task_deadline, progress = task_progress, list_type = 'urgent_list', userid = key)
        db.session.add(new_task)
        print(key)
        db.session.commit()
        if str(new_task.deadline) == '9999-09-09 00:00:00':
            print(new_task.deadline)
        return redirect(url_for('urgent',username = username, key = key))
    else:
        tasks = Todo.query.filter_by(list_type="urgent_list").order_by(Todo.date_created).all()
        blah = [3,2,3];
        return render_template('urgent.html',tasks = tasks,username = username, key = key)



@app.route('/lazy_list/<username>/<key>', methods=['POST', 'GET'])
def lazy(username, key):
    if request.method == 'POST':
        task_content = request.form['lazy_content']
        task_notes = request.form['notes']
        task_progress = request.form['progress']
        formatt = "%Y-%m-%d"
        try:
            task_deadline = datetime.datetime.strptime(request.form['deadline'], formatt)
            print(task_deadline)
        except:
            task_deadline = datetime.datetime.strptime('9999-9-9', formatt)
        new_task = Todo(content = task_content, notes = task_notes, deadline = task_deadline, progress = task_progress, list_type = 'lazy_list', userid = key)
        db.session.add(new_task)
        db.session.commit()
        if str(new_task.deadline) == '9999-09-09 00:00:00':
            print(new_task.deadline)
        return redirect(url_for('lazy',username = username, key = key))
    else:
        tasks = Todo.query.filter_by(list_type="lazy_list").order_by(Todo.date_created).all()
        blah = [3,2,3];
        return render_template('lazy.html',tasks = tasks,username = username, key = key)



@app.route('/shopping_list/<username>/<key>', methods=['POST', 'GET'])
def shopping(username, key):
    if request.method == 'POST':
        task_content = request.form['shopping_content']
        task_notes = request.form['notes']
        task_progress = request.form['progress']
        formatt = "%Y-%m-%d"
        try:
            task_deadline = datetime.datetime.strptime(request.form['deadline'], formatt)
            print(task_deadline)
        except:
            task_deadline = datetime.datetime.strptime('9999-9-9', formatt)
        new_task = Todo(content = task_content, notes = task_notes, deadline = task_deadline, progress = task_progress, list_type = 'shopping_list', userid = key)
        db.session.add(new_task)
        db.session.commit()
        if str(new_task.deadline) == '9999-09-09 00:00:00':
            print(new_task.deadline)
        return redirect(url_for('shopping',username = username, key = key))
    else:
        tasks = Todo.query.filter_by(list_type="shopping_list").order_by(Todo.date_created).all()
        blah = [3,2,3];
        return render_template('shopping.html',tasks = tasks,username = username, key = key)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in Users.query.all():
            print(user.name, user.password)
            if username == user.name and password == user.password:
                aidi = user.id
                if user.isadmin == True:
                    return redirect(url_for('adminpage', username = username, key = aidi))
                return redirect(url_for('daily', username = username, key = aidi))
        return ' wrong username or password, please try again =)'
    return render_template('login.html')

@app.route('/adminpage/<username>/<key>')
def adminpage(username, key):
    users_list = Users.query.order_by(Users.date_created).all()
    return render_template('adminpage.html', users_list = users_list,username = username, key = key)

@app.route('/about/<username>/<key>')
def about(username,key):
    try:
        return render_template('about.html',username = username, key = key)
    except:
        return 'woops, you are a fishi'

@app.route('/importance/<username>/<key>')
def importance(username,key):
    try:
        return render_template('importance.html', username = username, key = key)
    except:
        return 'woops, you are a fishi'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass1']
        password_verify = request.form['pass2']
        admin = False
        print(password, password)
        if password == password_verify:
            new_account = Users(name = username, password = password, isadmin = admin)
            db.session.add(new_account)
            db.session.commit()
            return render_template('success.html')
        else:
            return 'wrong passwords, please try again'
    return render_template('register.html')

@app.route('/delete/<username>/<key>/<int:id>')
def delete(username,key, id):
    task_to_delete = Todo.query.get_or_404(id)
    source = task_to_delete.list_type
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/'  + source + '/' + username + '/'+ key)
    except:
        return 'woops, you are a fishi'

@app.route('/deleteuser/<username>/<key>/<int:id>')
def deleteuser(username, key,id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/adminpage/' + username + '/'+ key)
    except:
        return 'woops, you are a fishi'

@app.route('/update/<username>/<key>/<int:id>', methods=['GET', 'POST'])
def update(username,key,id):
    task = Todo.query.get_or_404(id)
    source = task.list_type
    if request.method == 'POST':
        task.content = request.form['content']
        if request.form['notes'] != '':
            task.notes = request.form['notes']
        formatt = "%Y-%m-%d"
        try:
            task.deadline = datetime.datetime.strptime(request.form['deadline'], formatt)
            print(task_deadline)
        except:
            task_deadline = datetime.datetime.strptime('9999-9-9', formatt)
        task.progress = request.form['progress']
        try:
            db.session.commit()
            return redirect('/' + source + '/' + username + '/'+ key)
        except:
            return 'woops, you are a fishi'
    else:
        return render_template('update.html',username = username, key = key, task = task)

from flask import Flask, render_template, jsonify, request
import paypalrestsdk

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/payment', methods=['POST'])
def payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "1.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "1.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})


# sql_engine = create_engine('sqlite:///Todo.db', echo = False)
# results = pd.read_sql_query('select * from Todo', sql_engine)
# results.to_csv('Todo.csv', index=False, sep=";")

# sql_engine = create_engine('sqlite:///users.db', echo = False)
# results = pd.read_sql_query('select * from Users', sql_engine)
# results.to_csv('Users.csv', index=False, sep=";")

if __name__ == "__main__":
    app.run(debug=True)

