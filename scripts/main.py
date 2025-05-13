from class_requests import Api

conta = input('Digite o nome da empresa que deseja verificar as linguagens mais usadas: ')

consulta_dados = Api(conta)
consulta_df = consulta_dados.criar_dataframe()
if len(consulta_df) > 1:
    print(consulta_df)
