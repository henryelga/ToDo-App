from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(300), nullable = False)

    def __repr__(self):
        return 'Item ' + str(self.id)

@app.route('/')

def home():
    return render_template('index.html')




@app.route('/items', methods = ['GET', 'POST'])

def items():

    if request.method == 'POST':
        item = request.form['item']
        new = Items(title = item)
        db.session.add(new)
        db.session.commit()
        return redirect ('/items')

    else:
        all_items = Items.query.order_by(Items.id).all()
        return render_template('items.html', raw = all_items)



@app.route('/items/new', methods = ['GET', 'POST'])

def new_items():

    if request.method == 'POST':
        item = request.form['item']
        new = Items(item = item)
        db.session.add(new)
        db.session.commit()
        return redirect ('/items')

    else:
        return render_template('items.html')



@app.route('/items/delete/<int:id>')

def delete(id):
    del_item = Items.query.get_or_404(id)
    db.session.delete(del_item)
    db.session.commit()
    return redirect ('/items')



if __name__ == '__main__':
    app.run(debug = True)