import json
import requests

# Interage com uma página ckan

url = "dados.ufpe.br"

print("Listando os pacotes existentes no portal de dados abertos")
response = requests.get('http://{}/api/action/package_list'.format(url))
print(response)
print(response.status_code)
print(response.content)
print("")
print("")
response_package = response.json()
print(response_package["help"])
print()
print("LISTA DE CONJUNTO DE DADOS. TODO SÃO {}.".format(len(response_package["result"])))
print(len(response_package["result"]))
for dataset in range(len(response_package["result"])):
    print(response_package["result"][dataset])

print()
print()
print("OBTENDO INFORMAÇÕES DO CONJUNTO DE DADOS {}.".format(response_package["result"][1]))