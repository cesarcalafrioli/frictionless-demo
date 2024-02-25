from flask import render_template, request
from app.main import bp

from frictionless.portals import CkanControl
from frictionless import Package

import requests
import json

OPEN_DATA_PORTAL = 'https://dados.ufpe.br/dataset/'

# Extrai as informações do portal de dados abertos
class Portal:
    def __init__(self, url):
        self.url = url
        self.datasets = []
        self.datasets2 = []

        response_package = requests.get('http://{}/api/action/package_list'.format(url)).json()
        self.qtd_datasets = len(response_package["result"])

        for dataset in range(len(response_package["result"])):
            self.datasets.append(response_package["result"][dataset])
            self.datasets2.append(Dataset(response_package["result"][dataset]))

        print("Lista dos conjuntos de dados aos quais pertencem a este portal: "+str(self.datasets))
        print("Informação do primeiro conjunto de dados instanciado")
        print("----------------------------------------------------")
        print("Título: "+self.datasets2[0].titulo)
        print("Quantidade de resources: "+str(self.datasets2[0].qtd_resource))

# Extrai as informações do Conjunto de dados
class Dataset:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        
        ckan_control = CkanControl()
        package = Package(OPEN_DATA_PORTAL+resource_id, control=ckan_control)

        self.titulo = package.title
        self.qtd_resource = len(package.resources)
     
# Extrai as informações do resource do conjunto de dados
class Resource:
    pass
    
@bp.route('/', methods=['GET'])
def index():
    header = "Frictionless - Demo"

    #dataset1 = Dataset('boletim-oficial')
    #dataset2 = Dataset('cursos-de-graduacao')

    #ds_list = [dataset1, dataset2]
    #print("Info das datasets")
    #print(ds_list[0].titulo)

    portal = Portal('dados.ufpe.br')

    ds_list = portal.datasets2

    return render_template('index.html', titulo='Frictionless demo', datasets=ds_list, header=header, portal=portal)
