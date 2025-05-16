import requests
import re
import pandas as pd
import base64

class Api:
    def __init__(self, owner, username, repo):
        self.username = username
        self.repo = repo
        self.api_base_url = 'https://api.github.com'
        self.access_token = 'ghp_SEU TOKEN' # <---------- INCLUA SEU TOKEN AQUI
        self.api_version_call = 'X-Github-Api-Version'
        self.api_version_data = '2022-11-28'
        self.header = {'Authorization': 'Bearer ' + self.access_token,
                  self.api_version_call:self.api_version_data}
        self.owner = owner
        self.url = f'{self.api_base_url}/users/{self.owner}/repos'
    
    def total_pages(self):
        header_total_pages = {'Authorization': 'Bearer ' + self.access_token,
                              'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(self.url, headers=header_total_pages)

        link_header = response.headers.get('Link', '')

        pages = 1

        if 'rel="last"' in link_header:
            match = re.search(r'page=(\d+)>; rel="last"', link_header)
            if match:
                pages = int(match.group(1))

        return pages

    def listar_repositorios(self):
        repos_list = []
        pages = self.total_pages()
        for page in range(1,pages+1):
            try:
                url_page = f'{self.url}?page={page}'
                response = requests.get(url_page, headers=self.header)
                repos_list.append(response.json())
            except Exception as e:
                print(f"Erro ao acessar página {page}: {e}")
                repos_list.append([])

        return repos_list
    
    def criar_dataframe(self):
        dados = self.listar_repositorios()

        if len(dados) <= 1:
            print('\n\n===========================ERROR===========================\n')
            print("Nenhum dado encontrado. Verifique se o nome da empresa está correto.")
            print('Dica: O nome da empresa fica disponível no endereço do site da seguinte forma')
            print('https://github.com/orgs/NOME-DA-EMPRESA/repositories? \n\n')
            return []

        dados_names = extrair_nome(dados)
        dados_lang = extrair_lang(dados)

        df = pd.DataFrame({
            'Repositório': dados_names,
            'Linguagem': dados_lang
        })

        df.to_csv(f'{self.owner}.csv', index=False)

        self.salvar_dados()

        return df
    
    def salvar_dados(self):
        nome_arquivo = f'{self.owner}.csv'
        caminho_arquivo = f'/home/bruno/python_requests/{self.owner}.csv'

        with open(caminho_arquivo, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)

        url = f'{self.api_base_url}/repos/{self.username}/{self.repo}/contents/{nome_arquivo}'
        data = {
            "message": f"Adicionando o arquivo {nome_arquivo}",
            "content": encoded_content.decode("utf-8")
        }

        response = requests.put(url, json=data, headers=self.header)
        print(f'Status_code do upload do arquivo: {response.status_code}')
    
def extrair_nome(lista):
    repos_names = []
    for page in lista:
        for repo in page:
            try:
                repos_names.append(repo['name'])
            except:
                pass

    return repos_names

def extrair_lang(lista):
    repos_lang = []
    for page in lista:
        for repo in page:
            try:
                repos_lang.append(repo['language'])
            except:
                pass

    return repos_lang