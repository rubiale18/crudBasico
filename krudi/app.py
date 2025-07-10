#BIBLIOTECAS
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Aqui você cria o seu site/sistema.
#app vai controlar todas as páginas e ações.
app = Flask(__name__)

# Dados de acesso ao banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rubialef18@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conexão com o banco
db = SQLAlchemy(app)

# Criação da Tabela
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        novoUsuario = Usuario(nome=nome, email=email)
        db.session.add(novoUsuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', usuario=None)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuarioP = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuarioP.nome = request.form['nome']
        usuarioP.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', usuario=usuarioP)

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    usuarioP = Usuario.query.get_or_404(id)
    db.session.delete(usuarioP)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
