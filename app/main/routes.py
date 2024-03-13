from flask import render_template, request
from app.main import bp

from frictionless.portals import CkanControl
from frictionless import Package

import requests
import json

from app.main.forms import SearchForm

OPEN_DATA_PORTAL = 'https://dados.ufpe.br/dataset/'

# Extrai as informações do portal de dados abertos
class Portal:
    def __init__(self, url):
        self.url = url
        self.datasets_list = []

        response_package = requests.get('http://{}/api/action/package_list'.format(url)).json()
        self.qtd_datasets = len(response_package["result"])

        #print(self.qtd_datasets)
        for dataset in range(len(response_package["result"])):
         #   print(dataset)
            self.datasets_list.append(Dataset(self.url, response_package["result"][dataset]))
   

# Extrai as informações do Conjunto de dados
class Dataset():
    
    @property
    def dataset_resources_id(self):
        """ Lista os resources de uma determinada Package"""
        """ OBS: Os nomes de cada resource estão em Package, não em Resource"""
        dataset_resources = self.__dataset_response["result"]["resources"]
        return dataset_resources

    def __init__(self, url, dataset_id):
        """ Construtor da classe Dataset """
        self.__url = url
        self.__dataset_id = dataset_id
        self.__dataset_response = requests.get('https://{}/api/3/action/package_show?id={}'.format(url, dataset_id)).json()
        #self.__dataset_response = requests.get('https://dados.ufpe.br/api/3/action/package_show?id=boletim-oficial').json()
        self.__dataset_title = self.__dataset_response["result"]["title"]
        self.__qtd_resources = len(self.__dataset_response["result"]["resources"])

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
        
@bp.route('/', methods=('GET','POST'))
def index():
    header = "CKAN - Demo"
    
    form = SearchForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        
        portal = Portal(form.url.data.replace('https://',""))
        ds_list = portal.datasets_list
    
        return render_template('index.html', titulo=header, form=form, datasets=ds_list, portal=portal)
        
    return render_template('index.html', titulo=header, form=form)


# Exibindo informações de um dataset
@bp.route('/<string:url>/<string:dataset_id>/', methods=('GET','POST'))
def dataset(dataset_id, url):
    header = "CKAN - Demo"

    dataset = Dataset(url,dataset_id)
    resources = dataset.dataset_resources_id
    print(dataset.dataset_resources_id)

    return render_template('dataset.html', resources=resources, dataset=dataset, header=header)   