from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager
import uuid


app = Flask(
    __name__
)

# adicionado o cors para permitir que o aplicativo seja acessível pelo swagger e outras aplicações externas
CORS(app)


loginManager = LoginManager();

#Conexão com banco sqlite
app.config["SECRET_KEY"] = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

loginManager.init_app(app)
loginManager.login_view = "login"


# Definição de entidade de usuário no banco de dados
class User(db.Model, UserMixin):
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
# Definição de entidade de produtos no banco de dados 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)
    
# Definição de rota inicial do aplicativo
@app.route('/')
def hello_world(): 
    print('listening')

# * Rotas de usuários        
@app.route("/api/users/create", methods=["POST"])
def register_new_user():
    data = request.json
    if(data["username"] and data["password"]):
        
        # criando usuário
        user = User(
            username = data["username"],
            password = data["password"]
        )
        
        print(user)
        # Adicionando usuário na sessão
        db.session.add(user)
        
        # Salvar usuário no banco 
        db.session.commit()
        return jsonify({"message":"user successfully created"})
    return jsonify({"message": "Error on create user"}), 400



# Rota de login
@app.route("/login", methods=["POST"])
def authenticate_user():
    
    # Recebe dados do corpo de requisição
    data = request.json
    
    # Checa se todos os dados foram enviados
    if(data["username"] and data["password"]):
        
        # Procura usuário pelo "username"
        user = User.query.filter_by(username = data["username"]).first()
        
        # Checa se algum usuário foi encontrado
        
        if user == None:
            return jsonify({"message": "User not find"}), 404
            
            
        # Checa se as senhas coincidem
        if user.password == data["password"]:
            return jsonify({"message": "Logged successfully"})
        return jsonify({"message": "Unauthorized"}), 401
    
    return jsonify({"message": "Invalid data"}), 400


# * Rotas de produtos 
# Anotação para definir rota e métodos aceitos
@app.route('/api/products/add', methods=['POST'])
def add_new_product():
    # Resgata dados do corpo de requisição
    
    data = request.json
    
    # Checa se todos os dados obrigatórios foram enviados
    if(data['name'] and data['price']): 
        
        # Criação de novo objeto para gravação no banco de dados
        product = Product(
            name = data['name'],
            price = data['price'], 
            # A função get permite que seja procurado o campo com o nome igual ao primeiro parâmetro e 
            # define o segundo parâmetro como valor padrão
            description = data.get('description', ''))
        
        # Adiciona o produto a sessão criada 
        db.session.add(product)
        
        # Salva dados criados durante a sessão
        
        db.session.commit()
        
        # Retorna em formato json o dicionario que for oferecido como parâmetro
        return jsonify({"message":'successfully record'}) 
    else:
        return jsonify({"message":'invalid data'}), 400


# Rota de deleção
# Quando ha um parâmetro passado pela rota o mesmo deve ser passado como uma tag dentro da declaração
# e como parâmetro dentro da função
@app.route('/api/products/delete/<int:productId>', methods=['DELETE'])
def delete_product(productId):
    
    # Resgata produto existente pelo id dentro da query
    product = Product.query.get(productId)
    
    # Checa existência do produto
    if(product):
        # Delete a produto em sessão
        db.session.delete(product)
        
        # Salva as alterações
        db.session.commit()
        return ({"message":"Product deleted successfully"})
    return jsonify({"message":' product not found'}), 404
    

# Busca de produto por id
@app.route("/api/products/<int:productId>", methods=["GET"])
# Quando ha um parâmetro passado pela rota o mesmo deve ser passado como uma tag dentro da declaração
# e como parâmetro dentro da função
def get_product(productId):
    
    # Recupera produto existente
    product = Product.query.get(productId)
    
    # Checa existência do produto
    if(product):
        
        # retorna em json a entidade
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message":'product not found'}), 404



# Rota de seleção de lista de produtos 
@app.route("/api/products", methods=["GET"])
def list_products():
    #Recupera todos os produtos do banco de dados
    products = Product.query.all()
    
    # Cria um array para guardar todos os produtos
    productsList = []
    
    # Realiza a iteração de cada produto colocando-o dentro da lista
    for product in products:
        productsList.append({"name":product.name, "price":product.price, "description":product.description, "id":product.id})
        
    # Retorna a lista
    return jsonify({"products":productsList})
    
    
#Rota de atualização
@app.route('/api/products/update/<int:productId>', methods=['PUT'])
# Quando ha um parâmetro passado pela rota o mesmo deve ser passado como uma tag dentro da declaração
# e como parâmetro dentro da função
def update_product(productId):
    

    # Recupera dados do corpo de requisição e produto existente
    data = request.json
    product = Product.query.get(productId)
    
    
    # Checa se produto existe
    
    if not product:
        return jsonify({"message":'product not found'}), 404
 
    # Checa se campo "name" foi enviado pelo corpo de requisição e altera
    if "name" in data:
        product.name = data["name"]
    
    # Checa se campo "price" foi enviado pelo corpo de requisição e altera
    if "price" in data:
        product.price = data["price"]
    
    # Checa se campo "description" foi enviado pelo corpo de requisição e altera    
    if "description" in data:
        product.description = data["description"]
        
    
    # Salva as alterações
    db.session.commit()
        
    return jsonify({"message":"product update successfully" }),202


if(__name__ == '__main__'):
    app.run(debug=True)