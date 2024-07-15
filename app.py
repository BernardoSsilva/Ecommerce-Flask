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
        return jsonify({"message":'successfully record'}) 
    else:
        return jsonify({"message":'invalid data'}), 400

@app.route('/api/products/delete/<int:productId>', methods=['DELETE'])
def delete_product(productId):
    product = Product.query.get(productId)
    if(product):
        db.session.delete(product)
        db.session.commit()
        return ({"message":"Product deleted successfully"})
    return jsonify({"message":' product not found'}), 404
    
@app.route("/api/products/<int:productId>", methods=["GET"])
def get_product(productId):
    product = Product.query.get(productId)
    if(product):
        
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message":'product not found'}), 404
    
if(__name__ == '__main__'):
    app.run(debug=True)