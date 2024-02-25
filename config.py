# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# Continuar no passo "Creating the Questions Blueprint and Rendering its Templates"
import os

# Estabelecendo o diretório-base para atribui corretamente o caminho para o arquivo de banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
