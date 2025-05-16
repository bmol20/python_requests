from class_requests import Api

usuario = input('Digite seu nome de usuário: ')
conta = input('Digite o nome da empresa que deseja verificar as linguagens mais usadas: ')
repo = input('Digite o nome do repositório em que deseja salvar: ')

consulta_dados = Api(conta, usuario, repo)
consulta_df = consulta_dados.criar_dataframe()
if len(consulta_df) > 1:
    print(consulta_df)
