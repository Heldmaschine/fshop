from flask import Flask, render_template, flash, request, url_for, redirect, session, jsonify
from passlib.hash import sha256_crypt
from app import app,db
from .forms import RegistrationForm

import json
from .models import User, Flower, Category, Bill
from .mongo_models import Post, Comment
import datetime

@app.route('/')
def index():
    flowers = Flower.query.filter_by(category=1).limit(5)
    #fix
    posts_unsolved = Post.query.filter(Post.category == 0).all()
    posts_solved = Post.query.filter(Post.category == 1).all()
    posts_news = Post.query.filter(Post.category == 2).all()
    return render_template("index.html", flowers=flowers,
                           houseplants=Flower.query.filter_by(category=2).limit(5),
                           bouquets=Flower.query.filter_by(category=3).limit(5), posts_unsolved=posts_unsolved,
                           posts_solved=posts_solved, posts_news=posts_news)

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            name = form.name.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            if User.query.filter_by(username=username).first():
                return render_template('register.html', form=form)
            else:
                db.session.add(User(username, email, name, password))
                db.session.commit()
                #gc.collect() garbage collect
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
        return render_template("register.html", form=form)
    except Exception as e:
        return (str(e))


@app.route('/login/', methods=["GET", "POST"])
def login_page():
    error = ''
    if request.method == "POST":
        if User.query.filter_by(username=request.form['username']).first() and \
                sha256_crypt.verify(request.form['password'], User.query.filter_by(
                    username=request.form['username']).first().password):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error = 'Логин или пароль введен неверно, повторите попытку'
    return render_template("login.html", error=error)

@app.route('/<category>/', methods=["GET", "POST"])
def flowers(category):
    title = Category.query.filter_by(url=category).first()
    if title == None:
        return redirect(url_for('index'))
    minprice = 0
    maxprice = 150
    orderby = 'asc'
    flowers_query = Flower.query.with_entities(Flower.name, Flower.price, Flower.url).filter_by(
        category=Category.query.filter_by(url=category).first().id).order_by(Flower.price.asc()).all()
    if request.method == 'POST':
        minprice = request.form['minprice']
        maxprice = request.form['maxprice']
        orderby = request.form['ord']
        if orderby == 'desc':
            flowers_query = Flower.query.with_entities(Flower.name, Flower.price, Flower.url).filter_by(
                category=Category.query.filter_by(url=category).first().id).filter(
                Flower.price >= minprice,Flower.price <= maxprice).order_by(Flower.price.desc()).all()
        else:
            flowers_query = Flower.query.with_entities(Flower.name, Flower.price, Flower.url).filter_by(
                category=Category.query.filter_by(url=category).first().id).filter(Flower.price >= minprice,
                                                                                   Flower.price <= maxprice).order_by(
                Flower.price.asc()).all()
    return render_template("flowers.html", title=title.name,flowers=flowers_query,minprice=minprice, maxprice=maxprice,
                           orderby=orderby)

@app.route('/<category>/item/<flower>', methods=["GET", "POST"])
def flower_view(category, flower):
    flower = Flower.query.with_entities(Flower.name, Flower.price, Flower.url, Flower.id).filter_by(
        url=flower).first()
    if request.method == 'POST':
        flower_dict = {
            'id': flower[3],
            'amount': request.form['amount']
        }
        if request.cookies.get('list_to_buy') == None:
            resp = app.make_response(redirect('/cart/'))
            resp.set_cookie('list_to_buy', value=json.dumps([flower_dict]))
            return resp
        else:
            flower_list = json.loads(request.cookies.get('list_to_buy'))
            flower_list.append(flower_dict)
            resp = app.make_response(redirect('/cart/'))
            resp.set_cookie('list_to_buy', value=json.dumps(flower_list))
            return resp
    return render_template("page.html", title=flower[0], flower=flower)

@app.route('/cart/', methods=["GET", "POST"])
def cart():
    if request.cookies.get('list_to_buy')==None:
        return render_template("cart.html", title="Корзина", message='Вы еще ничего не положили в корзину')
    else:
        flower_list = json.loads(request.cookies.get('list_to_buy'))
        for flower in flower_list:
            id_flower = flower['id']
            flower['id'] = Flower.query.with_entities(Flower.id, Flower.name, Flower.url,
                                                      Flower.price).filter_by(id=id_flower).first()
            flower.update({'price': int(flower['amount'])*flower['id'][3]})
        if request.method == 'POST':
            for product in json.loads(request.cookies.get('list_to_buy')):
                db.session.add(Bill(product_id=product['id'], username=session['username'], delivery_date=request.form['datepicker'],
                                    delivery_place=request.form['address'],bill_date=datetime.date.today(),
                                    amount=product['amount'], debit_card=request.form['debit']))
                db.session.commit()
            resp = app.make_response(render_template("buy_form.html"))
            resp.set_cookie('list_to_buy',  expires=0)
            return resp
    return render_template("cart.html", title="Корзина", items=flower_list)


@app.route('/user_page/')
def user_page():
    user_data = User.query.with_entities(User.name, User.email,
                                         User.username).filter_by(username=session['username']).first()
    user_bills = db.session.query(Bill,Flower).with_entities(Bill.amount, Bill.delivery_place, Flower.id,
                                                              Bill.delivery_date).filter_by(
        username=session['username']).filter_by(id=Flower.id).all()
    user_posts = Post.query.filter(Post.author == session['username']).all()
    print(user_posts)
    user_comments = Comment.query.filter(Comment.author == session['username']).all()
    #print(user_comments)
    return render_template("user.html", title=user_data[2], user_data=user_data,
                           user_bills=user_bills, posts=user_posts, comments=user_comments)

@app.route('/logout')
def logout():
    resp = app.make_response(redirect('/'))
    resp.set_cookie('item', expires=0)
    session.pop('logged_in', None)
    return resp

@app.route('/board/<category>', methods=["GET", "POST"])
def board(category):
    #posts = []
    if category == 'unsolved':
        posts = Post.query.filter(Post.category==0).all()
    elif category =='solved':
        posts = Post.query.filter(Post.category == 1).all()
    elif category == "news":
        posts = Post.query.filter(Post.category==2).all()
    elif category == "all":
        posts = Post.query.all()
    if request.method == 'POST':
        post = Post(title=request.form['title'], text=request.form['question'], author=session['username'], category=0)
        post.save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("board.html", title='Форум и поддержка', posts=posts)

@app.route('/board/post/<id>', methods=["GET", "POST"])
def post(id):
    post = Post.query.get(str(id))
    comments = Comment.query.filter(Comment.post.mongo_id==post.mongo_id).all()
    print(post.mongo_id)
    #post.remove()
    if request.method == 'POST':
        Comment(text=request.form['comment'], author=session['username'], post=post).save()
        return redirect(url_for('post', id=post.mongo_id))
    return render_template("post.html", title=post.title, post=post, comments=comments)

@app.route('/_add_numbers')
def add_numbers():
    storage = request.args.get('storage')
    phone = request.args.get('storage')
    return jsonify(result=True)

@app.route('/your_bouquet/')
def your_bouquet():
    return render_template("your_bouquet.html", title='Ваш букет')

