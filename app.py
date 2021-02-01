from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/udacity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager=Manager(app)
manager.add_command('db', MigrateCommand)

"""
many to many 
Orders and Products
order_item=db.Table('order_item', 
    db.Column('order_id', db.Integer, dbForeignKey('orders.id) primary_key=True)
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class Order(db.Model):
    __tablename__='orders'
    id=db.Column(db.Integer, primary_key=True)
    status=Column(db.String(), nullable=False)
    products=db.relationship('Product', secondary=order_items, backref=db.backef('orders', lazy=True))

class Product(db.Model):
    __tablename__'products'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(), nullable=False)


"""

class Post(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(250), nullable=False)
    description=db.Column(db.String(), nullable=False)
    completed=db.Column(db.Boolean, nullable=False, default=False)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    comment=db.relationship('Comment', lazy=True)

    def __repr__(self):
        return '<Post %r>' % self.id

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer, primary_key=True)
    comment=db.Column(db.String(), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at=db.Column(db.DateTime, server_default=db.func.now())
    updated_at=db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    post=db.relationship('Post', backref='list', lazy=True)



@app.route("/")
def index():
    return render_template("index.html", posts=Post.query.order_by('id').all())

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/store', methods=['POST'])
def store():
    content = request.form.get('content', '')
    description = request.form.get('description', '')
    # content = request.form['content']
    # description = request.form['description']
    post = Post(content = content, description = description)

    try:
        db.session.add(post)
        db.session.commit()
        posts = Post.query.all()
        return render_template('index.html', success="Post Added!!", posts=posts)
    except:
        return 'The error not insert data'


@app.route('/create_js', methods=['POST'])
def create_js():
    content = request.get_json()['content']
    description = request.get_json()['description']
    post = Post(content=content, description=description)
    db.session.add(post)
    db.session.commit()
    return jsonify({
        'content':post.content,
        'description':post.description
    })

@app.route('/update/<int:id>')
def update(id):
    post = Post.query.get(id)
    return render_template('update.html', post=post)    

@app.route('/update-post/<int:id>', methods=['POST'])
def update_post(id):
    content = request.form['content']
    description = request.form['description']
    post = Post.query.get(id)
    post.content = content
    post.description = description
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return render_template('update.html', error="Database Error!!!")
    finally:
        db.session.close()
    
    return render_template('index.html', success="Update Data!!!", posts = Post.query.all())

@app.route('/update-completed/<int:id>', methods=['POST'])
def completed(id):
    try:
        completed = request.get_json()['completed']
        post = Post.query.get(id)
        post.completed = completed
        db.session.commit()
        return jsonify({
            'completed' :post.completed
        })
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/delete-ajax/<int:id>', methods=['DELETE'])
def delete_ajax(id):
    try:
        Post.query.filter_by(id=id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    post = Post.query.get(id)
    try:
        db.session.delete(post)
        db.session.commit()
        posts = Post.query.all()
        success = "Post deleted !!!"
        return render_template('index.html', success=success, posts=posts)
    except:
        error = "Oops! Database error! "
        return render_template('index.html', error=error, posts = posts)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)