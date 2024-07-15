from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)
     
    

@app.route('/')
def hello_world(): 
    print('listening')
    
    
@app.route('/api/products/add', methods=['POST'])
def add_new_product():
    data = request.json
    if(data['name'] and data['price']): 
        product = Product(name = data['name'], price = data['price'], description = data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        jsonify({"code":200, "message":'successfully record'}) 
    else:
        jsonify({"code":400, "message":'invalid data'}) 


    

if(__name__ == '__main__'):
    app.run(debug=True)