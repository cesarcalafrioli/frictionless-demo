from flask import Flask # Importa a classe Flask do pacote flask

from config import Config # Importa a classe de configuração Config do arquivo config.py

def create_app(config_class=Config): # Função factory do aplicativo Flask. Cria uma instância de aplicação chamada app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'your secret key'


    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    return app