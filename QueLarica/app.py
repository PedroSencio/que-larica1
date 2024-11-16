from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
import secrets

app = Flask(__name__)

app.secret_key = 'chave_secreta_25'

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'delivery.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'check_same_thread': False}
}


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Restaurante(db.Model):
    __tablename__ = 'restaurantes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False, unique=True)
    endereco = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=True) 
    produtos = db.relationship('Produto', back_populates='restaurante', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(15), nullable=False, unique=True)
    endereco = db.Column(db.String(100), nullable=False)

class Entregador(db.Model):
    __tablename__ = 'entregadores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(15), nullable=False, unique=True)
    status = db.Column(db.Boolean, default=False)  # False para disponível, True para ocupado

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255), nullable=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    restaurante = db.relationship('Restaurante', back_populates='produtos')



# Comando para criar as tabelas no banco de dados
# with app.app_context():
#    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json  # Recebe os dados do JavaScript (JSON)
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('userType')  # 'cliente', 'restaurante' ou 'entregador'

        user = None
        if user_type == 'cliente':
            user = Cliente.query.filter_by(email=email, senha=password).first()
        elif user_type == 'restaurante':
            user = Restaurante.query.filter_by(email=email, senha=password).first()
        elif user_type == 'entregador':
            user = Entregador.query.filter_by(email=email, senha=password).first()

        if user:
            session['user_id'] = user.id
            session['user_type'] = user_type
            session['user_name'] = user.nome
        
        if user_type == 'cliente':
            return {"success": True, "redirect_url": "/dashboard_cliente"}, 200
        elif user_type == 'restaurante':
            return {"success": True, "redirect_url": "/dashboard_restaurante"}, 200
        elif user_type == 'entregador':
            return {"success": True, "redirect_url": "/dashboard_entregador"}, 200
        else:
            return {"success": False, "message": "Email ou senha incorretos."}, 401
    
    return render_template("home/home.html")

@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']
        endereco = request.form['endereco']

        if Cliente.query.filter_by(email=email).first() and Cliente.query.filter_by(cpf=cpf).first():
            return render_template('restaurante/cadastro.html', error_message="Email ou CPF já cadastrado. Tente outra vez.")
        
        novo_cliente = Cliente(
            nome=nome,
            email=email,
            senha=senha,
            cpf=cpf,
            endereco=endereco
        )

        try:
            db.session.add(novo_cliente)
            db.session.commit()
            return redirect(url_for('sucesso'))
        except IntegrityError:
            db.session.rollback()  # Reverte a transação se ocorrer erro
            return render_template('cliente/cadastro.html', error_message="Erro ao salvar: CPF ou Email já cadastrados.")

        return redirect(url_for('sucesso')) 
    
    return render_template('cliente/cadastro.html')

@app.route('/cadastro_restaurante', methods=['GET', 'POST'])
def cadastro_restaurante():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cnpj = request.form['cnpj']
        endereco = request.form['endereco']

        if Restaurante.query.filter_by(email=email).first() and Restaurante.query.filter_by(cnpj=cnpj).first():
            return render_template('restaurante/cadastro.html', error_message="Email ou CNPJ já cadastrado. Tente outra vez.")
        
        novo_restaurante = Restaurante(
            nome=nome,
            email=email,
            senha=senha,
            cnpj=cnpj,
            endereco=endereco
        )

        try:
            db.session.add(novo_restaurante)
            db.session.commit()
            return redirect(url_for('sucesso'))
        except IntegrityError:
            db.session.rollback()  
            return render_template('restaurante/cadastro.html', error_message="Erro ao salvar: CNPJ ou Email já cadastrados.")

        return redirect(url_for('sucesso')) 

    return render_template('restaurante/cadastro.html')

@app.route('/cadastro_entregador', methods=['GET', 'POST'])
def cadastro_entregador():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']

        if Entregador.query.filter_by(email=email).first() and Entregador.query.filter_by(cpf=cpf).first():
            return render_template('restaurante/cadastro.html', error_message="Email ou CPF já cadastrado. Tente outra vez.")
        
        novo_entregador = Entregador(
            nome=nome,
            email=email,
            senha=senha,
            cpf=cpf,
        )

        try:
            db.session.add(novo_entregador)
            db.session.commit()
            return redirect(url_for('sucesso'))
        except IntegrityError:
            db.session.rollback()  
            return render_template('entregador/cadastro.html', error_message="Erro ao salvar: CPF ou Email já cadastrados.")
        
        return redirect(url_for('sucesso')) 

    return render_template('entregador/cadastro.html')

@app.route('/sucesso')
def sucesso():
    return "Cadastro realizado com sucesso!"

@app.route('/dashboard_cliente')
def dashboard_cliente():
    # Verifica se o usuário está logado e é do tipo correto
    if 'user_id' not in session or session['user_type'] != 'cliente':
        return redirect(url_for('home'))

    # Busca o cliente no banco de dados
    cliente = Cliente.query.get(session['user_id'])

    if not cliente:
        return redirect(url_for('home'))

    # Renderiza o dashboard com os dados do cliente
    return render_template('cliente/dashboard.html', cliente=cliente)

@app.route('/dashboard_restaurante')
def dashboard_restaurante():
    if 'user_id' not in session or session['user_type'] != 'restaurante':
        return redirect(url_for('home'))

    restaurante = Restaurante.query.get(session['user_id'])
    itens_menu = Produto.query.filter_by(restaurante_id=restaurante.id).all()

    if not restaurante:
        return redirect(url_for('home'))

    return render_template('restaurante/dashboard.html', restaurante=restaurante, itens_menu=itens_menu)

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    if 'user_id' not in session or session['user_type'] != 'restaurante':
        return redirect(url_for('home'))

    restaurante = Restaurante.query.get(session['user_id'])

    if not restaurante:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        imagem = request.files['imagem']

        # Verifica se a imagem foi fornecida
        imagem = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imagem = filename

        if imagem == None:
            novo_produto = Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                restaurante_id=session['user_id']  # Obtém o id do restaurante logado
            )
        else:
            novo_produto = Produto(
                nome=nome,
                descricao=descricao,
                preco=preco,
                imagem=filename,
                restaurante_id=session['user_id']  # Obtém o id do restaurante logado
            )

        try:
            db.session.add(novo_produto)
            db.session.commit()
            return redirect(url_for('dashboard_restaurante'))
        except Exception as e:
            db.session.rollback()
            return f"Erro ao cadastrar produto: {e}"
        finally:
            db.session.remove() 

    return render_template('restaurante/cadastrar_item.html', restaurante=restaurante)

@app.route('/excluir_item/<int:item_id>', methods=['POST'])
def excluir_item(item_id):
    try:
        item = Produto.query.get(item_id)
        if not item:
            flash("Item não encontrado.", "error")
            return redirect(url_for('dashboard_restaurante'))

        restaurante_id = session.get('user_id')
        if item.restaurante_id != restaurante_id:
            flash("Você não tem permissão para excluir este item.", "error")
            return redirect(url_for('dashboard_restaurante'))

        db.session.delete(item)
        db.session.commit()
        flash("Item excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir item: {str(e)}", "error")

    return redirect(url_for('dashboard_restaurante'))


@app.route('/dashboard_entregador')
def dashboard_entregador():
    
    if 'user_id' not in session or session['user_type'] != 'entregador':
        return redirect(url_for('home'))

    entregador = Entregador.query.get(session['user_id'])

    if not entregador:
        return redirect(url_for('home'))

    return render_template('entregador/dashboard.html', entregador=entregador)


if __name__ == "__main__":
    app.run(debug=True)
