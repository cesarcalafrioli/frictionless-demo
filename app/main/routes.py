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
            self.datasets2.append(Dataset(url, response_package["result"][dataset]))

        print("Lista dos conjuntos de dados aos quais pertencem a este portal: "+str(self.datasets))
        print("Informação do primeiro conjunto de dados instanciado")
        print("----------------------------------------------------")
        print("Título: "+self.datasets2[0].titulo)
        print("Quantidade de resources: "+str(self.datasets2[0].qtd_resource))
        #print("Id das resources:"+str(self.datasets2.))

# Extrai as informações do Conjunto de dados
class Dataset:
    def __init__(self, url, dataset_id):
        self.url = url
        self.dataset_id = dataset_id
        self.dataset_resources = []
        
        full_url = 'https://{}/dataset/'.format(url)

        ckan_control = CkanControl()
        package = Package(full_url+dataset_id, control=ckan_control)

        self.titulo = package.title
        self.qtd_resource = len(package.resources)
                
        # Lista todas as resources contidas no dataset


# Extrai as informações do resource do conjunto de dados
class Resource:
    def __init__(self, url, resource_id):
        self.url = url
        self.resource_id = resource_id

        full_url = 'https://{}/api/3/action/datastore_search?resource_id={}'.format(url,resource_id)



    
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

    url = requests.get('https://dados.ufpe.br/api/3/action/datastore_search?resource_id=cd9e4b1b-b1bc-47a5-9055-7ccdf31a072a')
    response = url.json()
    print(response["help"])
    print("Fields:")
    print(response["result"]["resource_id"])

    return render_template('index.html', titulo='Frictionless demo', datasets=ds_list, header=header, portal=portal)
