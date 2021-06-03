from re import L
from flask import Flask , render_template , redirect, request, session
from data import Articles, Users
from passlib.hash import sha256_crypt
from pymongo import MongoClient
from functools import wraps
import datetime as dt

connect = MongoClient("mongodb+srv://1234:1234@cluster0.j8pke.mongodb.net/gangnam?retryWrites=true&w=majority")

db = connect.gangnam

col = db.users

art = db.article

app = Flask(__name__)
app.debug = True

def enur():
    a = art.find()
    a_e = list(enumerate(a))
    return a_e



def is_loged_in(f):
    @wraps(f)
    def _wraps(*args,**kwargs):
        if 'is_loged' in session:
            return f(*args,**kwargs)
        else:
            return redirect('/login')
    return _wraps

def is_admined(e):
    @wraps(e)
    def _wraps(*args,**kwargs):
        if session['username'] == 'admin':
            return e(*args,**kwargs)
        else:
            return redirect('/login')
    return _wraps    

@app.route('/admin/<index>/edit', methods=['GET','POST'])
@is_admined
@is_loged_in
def edit_user(index):
    if request.method == 'POST':
        query = col.find()
        users = list(enumerate(query))
        id=int(index)
        user = users[id][1]
        id = user['_id']
        name = request.form['name']
        username = request.form['username']
        user = {"$set" : {"name":name},"$set" : {"username":username}}
        col.update({"_id":id},{"$set":{"name":name,"username":username}})
        return redirect('/admin')
    else:
        query = col.find()
        users = list(enumerate(query))
        id=int(index)
        user = users[id][1]
        return render_template("edit_users.html", user = user, id=id)


@app.route('/admin/<index>/delete')
@is_admined
@is_loged_in
def delete_user(index):
    query = col.find()
    users = list(enumerate(query))
    id=int(index)
    user = users[id][1]
    id = user['_id']
    if user != None:
        col.delete_one({"_id" : id})

    return redirect('/admin')        

@app.route('/admin', methods=['GET','POST'])
@is_admined
@is_loged_in
def admin():
    query = col.find()
    users = list(enumerate(query))
    return render_template('/admin.html', users = users)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password = sha256_crypt.encrypt(password)

        user = list(col.find({"email":email}))
        if (name==""):
            print("name is blank")
            return redirect('/register')
        if (email==""):
            print("email is blank")
            return redirect('/register')
        if (username==""):
            print("username is blank")
            return redirect('/register')
        if (password==""):
            print("password is blank")
            return redirect('/register')

        if bool(user) == False:
            users = Users(name, email, username, password)
            col.insert_one(users)
            return render_template('login.html')
        else:
            return redirect('/register')
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = list(col.find({"email":email}))
        if bool(user) == False:
            print("email does not exist")
            return redirect('/login')
        else:
            if sha256_crypt.verify(password,user[0]['password']):
                session['is_loged']=True
                session['username']=user[0]['username']
                session['email']=user[0]['email']
                return redirect('/')
            else:
                print('fail to login')
                return redirect('/login')
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/', methods=['GET' , 'POST'])
def hello_world():
    return render_template('home.html')

@app.route('/about', methods=['GET' , 'POST'])
@is_loged_in
def about():
    return render_template("about.html")


@app.route('/articles', methods=['GET' , 'POST'])
@is_loged_in
def articles():
    articles = enur()
    return render_template("articles.html" , articles = articles )


@app.route('/article/<index>', methods=['GET'])
@is_loged_in
def article(index):
    articles = enur()
    id=int(index)
    article = articles[id][1]
    if article == None:
        return redirect('/articles')
    else:
        return render_template("article.html" , article = article, index = index )

@app.route('/add_article', methods=['GET','POST'])
@is_loged_in
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        author = session['username']
        edit = dt.datetime.now()
        article = Articles(title = title,description=description,author=author,edit=edit)
        art.insert(article)
        articles = enur()
        index = len(articles)
        return redirect(f'/article/{index-1}')
    else:
        return render_template("add_article.html")


@app.route('/article/<index>/delete', methods=['GET'])
@is_loged_in
def delete_article(index):
    articles = enur()
    id=int(index)
    article = articles[id][1]
    id = article['_id']
    
    if (session['username'] != article['author']) and (session['username'] != 'admin'):
        return redirect('/articles')
    if article != None:
        art.delete_one({"_id" : id})
    return redirect('/articles')

@app.route('/article/<index>/edit', methods=['GET','POST'])
@is_loged_in
def edit_article(index):
    if request.method == 'POST':
        articles = enur()
        id=int(index)
        article = articles[id][1]
        id = article['_id']
        title = request.form['title']
        description = request.form['description']
        author = session['username']
        edit = dt.datetime.now()
        article = Articles(title = title,description=description,author=author,edit=edit)
        art.update({"_id":id},article)
        return redirect(f'/article/{index}')

    else:
        articles = enur()
        id=int(index)
        article = articles[id][1]
        id = article['_id']
        if (session['username'] != article['author']) and (session['username'] != 'admin'):
            return redirect('/articles')
        if article == None:
            return redirect('/articles')
        else:
            return render_template("edit_article.html", article = article, index=index)

if __name__ == '__main__':
    app.secret_key = 'gangnamStyle'
    app.run(port=5000)