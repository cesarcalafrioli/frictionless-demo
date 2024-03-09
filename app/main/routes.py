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
        #self.datasets = []
        self.datasets2 = []

        response_package = requests.get('http://{}/api/action/package_list'.format(url)).json()
        self.qtd_datasets = len(response_package["result"])

        print(self.qtd_datasets)
        for dataset in range(len(response_package["result"])):
            print(dataset)
            #self.datasets.append(response_package["result"][dataset]) # Aqui salva apenas o id do conjunto de dados para posterior busca
            self.datasets2.append(Dataset(self.url, response_package["result"][dataset]))

        
        # TESTE - DATASETS
        #print("Lista dos conjuntos de dados aos quais pertencem a este portal: "+str(self.datasets))
        #print("Informação do primeiro conjunto de dados instanciado")
        #print("----------------------------------------------------")
        #print("Título: "+self.datasets2[0].titulo)
        #print("Quantidade de resources: "+str(self.datasets2[0].qtd_resource))
        

# Extrai as informações do Conjunto de dados
class Dataset():
    
    @property
    def dataset_resources_id(self):
        """ Lista os resources de uma determinada Package"""
        """ OBS: Os nomes de cada resource estão em Package, não em Resource"""
        #dataset_resources =[self.__dataset_response["result"]["resources"] for resource_id in range(self.__qtd_resources)]
        dataset_resources = self.__dataset_response["result"]["resources"]
        print("------------------------------------------------------------------")
        #dataset_resources_id = [self.__dataset_response["result"]["resources"][resource_id]["id"] for resource_id in range(self.__qtd_resources)]
        #dataset_resources_name = [self.__dataset_response["result"]["resources"][resource_id]["name"] for resource_id in range(self.__qtd_resources)]
        #print(dataset_resources_name)
        #return 
        return dataset_resources

    def __init__(self, url, dataset_id):
        """ Construtor da classe Dataset """
        self.__url = url
        self.__dataset_id = dataset_id
        self.__dataset_response = requests.get('https://{}/api/3/action/package_show?id={}'.format(url, dataset_id)).json()
        self.__dataset_title = self.__dataset_response["result"]["title"]
        self.__qtd_resources = len(self.__dataset_response["result"]["resources"])
        # REMOVER DEPOIS - TRECHO ABAIXO JÁ APLICADO ACIMA
        #print("Lista de id de resources")
        #for resource_id in range(self.__qtd_resources):
        #    print(self.__dataset_response["result"]["resources"][resource_id]["id"]+"-"+self.__dataset_response["result"]["resources"][resource_id]["name"])

    @property
    def url(self):
        return self.__url
    
    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def dataset_id(self):
        return self.__dataset_id
    
    @dataset_id.setter
    def dataset_id(self, dataset_id):
        self.__dataset_id = dataset_id

    @property
    def dataset_response(self):
        return self.__dataset_response
    
    @dataset_response.setter
    def dataset_response(self, dataset_response):
        self.__dataset_response = dataset_response

    @property
    def dataset_title(self):
        return self.__dataset_title
    
    @dataset_title.setter
    def dataset_title(self, dataset_title):
        self.__dataset_title = dataset_title

    @property
    def qtd_resources(self):
        return self.__qtd_resources

    @qtd_resources.setter
    def qtd_resources(self, qtd_resources):
        self.__qtd_resources = qtd_resources
        

# Extrai as informações do resource do conjunto de dados
class Resource(Package):
    def __init__(self, url, resource_id):
        """ Construtor de um resource de um determinado conjunto de dados"""
        super().__init__(self)
        self.__url = url
        self.__resource_id = resource_id
        self.__resource_response = requests.get('https://{}/api/3/action/datastore_search?resource_id={}'.format(self.__url, self.__resource_id)).json()
        #self.__resource_fields = self.__resource_response["result"]["fields"]
        self.__resource_result = self.__resource_response
        print("HELP: {}".format(self.__resource_result['help']))
        print("Resource de id: {}".format(self.__resource_response["result"]["resource_id"]))
        #print("Campos deste resource: {}".format(self.__resource_fields))

    @property
    def resource_response(self):
        return self.__resource_response
    
    @resource_response.setter
    def resource_response(self, response):
        self.__resource_response = response

    @property
    def resource_fields(self):
        return self.__resource_fields
    
    @resource_fields.setter
    def resource_name(self, resource_fields):
        self.__resource_fields = resource_fields
        
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
    
    #dataset = Dataset('www.tesourotransparente.gov.br/ckan','cauc')

    #print("URL:"+dataset.url)
    #print("Dataset ID:"+dataset.dataset_id)
    #print("Response URL: {}".format(dataset.dataset_response))
    #print("Nome do conjunto de dados: {}".format(dataset.dataset_title))
    #print("Quantidade de resources neste conjunto de dados: {}".format(dataset.qtd_resources))
    #print("Lista de resources deste conjunto de dados: {}".format(dataset.dataset_resources_id))
    #return render_template('test.html')
    
    
# Exibindo informações de um dataset
@bp.route('/<string:dataset_id>/', methods=('GET','POST'))
def dataset(dataset_id):
    header = "Frictionless - Demo"


    dataset = Dataset('dados.ufpe.br',dataset_id)

    resources = dataset.dataset_resources_id

    return render_template('dataset.html', resources=resources, dataset=dataset)   