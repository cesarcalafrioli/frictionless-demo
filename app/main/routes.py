from flask import render_template
from app.main import bp

from frictionless.portals import CkanControl
from frictionless import Package

OPEN_DATA_PORTAL = 'https://dados.ufpe.br/dataset/'

# Extrai as informações do Conjunto de dados
class Dataset:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        
        ckan_control = CkanControl()
        package = Package(OPEN_DATA_PORTAL+resource_id, control=ckan_control)

        self.titulo = package.title
        self.qtd_resource = len(package.resources)
        

@bp.route('/')
def index():
    header = "Frictionless - Demo"

    dataset1 = Dataset('boletim-oficial')
    dataset2 = Dataset('cursos-de-graduacao')

    ds_list = [dataset1, dataset2]    

    return render_template('index.html', titulo='Frictionless demo', datasets=ds_list)
