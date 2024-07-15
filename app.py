from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eccomerce.db"
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float,nullable=False)
    description = db.Column(db.Text, nullable=True)
     
    

@app.route("/")
def helloWorld(): 
    print("listening")
    
    

if(__name__ == "__main__"):
    app.run(debug=True)