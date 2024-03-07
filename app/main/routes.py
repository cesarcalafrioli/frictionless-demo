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
            self.datasets2.append(Dataset(self.url, response_package["result"][dataset]))

        
        # TESTE - DATASETS
        #print("Lista dos conjuntos de dados aos quais pertencem a este portal: "+str(self.datasets))
        #print("Informação do primeiro conjunto de dados instanciado")
        #print("----------------------------------------------------")
        #print("Título: "+self.datasets2[0].titulo)
        #print("Quantidade de resources: "+str(self.datasets2[0].qtd_resource))
        

# Extrai as informações do Conjunto de dados
class Dataset:
    def __init__(self, url, dataset_id):
        self.url = url
        self.dataset_id = dataset_id
        self.dataset_resources = []
        
        #full_url = 'https://{}/dataset/'.format(self.url)

        #ckan_control = CkanControl()
        #package = Package(full_url+self.dataset_id, control=ckan_control)

        #self.titulo = package.title
        #self.qtd_resource = len(package.resources)

        # Listando todos os resources
        #for resource in range(self.qtd_resource):
            #self.dataset_resources.append(Resource(self.url, ))
            #pass

        self.full_url = requests.get('https://{}/api/3/action/package_show?id={}'.format(self.url, self.dataset_id))
        self.response = self.full_url.json()

        self.qtd_resources = len(self.response["result"]["resources"])
        print("Resources do conjunto de dados {}: ".format(self.response["result"]["title"]))
        for resource in range(self.qtd_resources):
            self.dataset_resources.append(Resource(self.url, self.dataset_id))
            

# Extrai as informações do resource do conjunto de dados
class Resource:
    def __init__(self, url, resource_id):
        self.url = url
        self.resource_id = resource_id

        resource_url = requests.get('https://{}/api/3/action/datastore_search?resource_id={}'.format(self.url, self.resource_id))
        response = resource_url.json()

        
@bp.route('/', methods=['GET'])
def index():
    header = "Frictionless - Demo"

    portal = Portal('dados.ufpe.br')

    ds_list = portal.datasets2

    # TESTE - ANALISANDO UM RESOURCE EM PARTICULAR ###

    """
    url = requests.get('https://dados.ufpe.br/api/3/action/datastore_search?resource_id=cd9e4b1b-b1bc-47a5-9055-7ccdf31a072a')
    response = url.json()
    print(response["help"])
    print("Fields:")
    print("Resource de id:"+response["result"]["resource_id"])
    print("Quantidade de campos que esta resoure tem:"+str(len(response["result"]["fields"])-1))
    print("Dicionário de dados desta resource")
    for field in range(1, len(response["result"]["fields"])): # Começa a contar a partir de um para pular um item do dicionário
        print("Campos desta resource:"+str(response["result"]["fields"][field]["id"]))
        print("Campos desta resource:"+str(response["result"]["fields"][field]))
        print("Descrição:"+str(response["result"]["fields"][field]["info"]['notes']))
    ###################################################
        """

    return render_template('index.html', titulo='Frictionless demo', datasets=ds_list, header=header, portal=portal)

# Exibindo informações de um dataset
@bp.route('/<string:dataset_id>/', methods=('GET','POST'))
def dataset(dataset_id):
    dataset = Dataset('dados.ufpe.br', dataset_id)

    return render_template('dataset.html', dataset=dataset)    