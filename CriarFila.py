#mportação
import pandas as pd
import pymongo
from bson.codec_options import CodecOptions
import socket
from datetime import datetime

class FilaMongoDB:
    def __init__(self, var_strdbName, var_strColectionName):
        '''
        Aqui são feitas as inicializações do banco de dados, do nome do banco, nome da fila,
        o nome do computador. O banco de dados é selecionado ou criado, jundo a coleção.
        '''
        self.var_clienteConection = pymongo.MongoClient(
            "<String de Conexão")
        self.var_strdbName = var_strdbName
        self.var_strColectionName = var_strColectionName
        self.var_strHostname = socket.gethostname()
        self.var_dbMongoDB = self.var_clienteConection[var_strdbName]
        try:
            if var_strdbName in self.var_clienteConection.list_database_names():
                print(f"O banco de dados {var_strdbName} foi selecionado")
                var_dbMongoDB = self.var_clienteConection[var_strdbName]
                if var_strColectionName in var_dbMongoDB.list_collection_names():
                    print(
                        f"A fila Selecionada {self.var_strColectionName} foi setada")
                else:
                    var_dbMongoDB = self.var_clienteConection[var_strdbName]
                    codec_options = CodecOptions(tz_aware=True)
                    var_MGcol = var_dbMongoDB.create_collection(
                        var_strColectionName, codec_options=codec_options)
                    print(f"A fila Selecionada {var_strColectionName} foi criada")
            else:
                print(
                    f"O banco de dados {var_strdbName} não existe. Sera criado junto a fila {var_strColectionName}")
                var_dbMongoDB = self.var_clienteConection[var_strdbName]
                codec_options = CodecOptions(tz_aware=True)
                var_MGcol = var_dbMongoDB.create_collection(
                    var_strColectionName, codec_options=codec_options)
            print("Dados do Maestro configurados")
        except Exception as e:
            print(f"Error de conexão como banco de dados. ERRO: {e}")
    
    #Adiciona todas as linhas de uma dataframe para a coleção.    
    def Add_item(self, data_frame):
        '''
        Adiciona todas as linhas de um dataframe à coleção. 
        Para cada linha no dataframe, é adicionado um novo item na coleção. 
        É importante ressaltar que o item na fila possui alguns dados básicos padrões, 
        como status, hora de início, hora de atualização, máquina em execução, prioridade de execução, conteúdo e histórico.
        
        No item a estrutura é:
            Status: <status>,
            Inciado: <hora de inicio>,
            Atualizado: <hora de atualização>,
            Maquina: <Maquina em execução>,
            Prioridade: <Prioridade de execução>,
            Conteudo: { <Linha de dados> },
            Historico: {
                Ação: <Tipo de ação>,
                Autor: <Maquina em execução>,
                Status: <Nome da Alteração>,
                Revisor: <Maquina em execução>,
                Horas: <Tempo agora>
        '''
        try:
            var_dfData = data_frame.to_dict(orient='records')
            for row in var_dfData:
                historico = {
                    'Ação': 'Criado',
                    'Autor': self.var_strHostname,
                    'Status': '-',
                    'Revisor': None,
                    'Horas': datetime.now()
                }
                json_Linha = {
                    'Status': 'NOVO',
                    'Inciado': datetime.now(),
                    'Atualizado': '-',
                    'Maquina': self.var_strHostname,
                    'Prioridade': 'Normal',
                    'Conteudo': row,
                    'Historico': {
                        '0': historico
                    }
                }
                resultado = self.var_clienteConection[self.var_strdbName][self.var_strColectionName].insert_one(
                    json_Linha)
                print('Item ' + str(resultado.inserted_id) + ' inserido com sucesso')
        except Exception as e:
            print(f"Error ao inserir novo item: {e}")
    
    #Retorna o proximo item de acordo coma prioridade
    def next_item(self):
        '''
        Retornar o próximo item da fila a ser processado. 
        O método retorna o próximo item de acordo com a prioridade de execução (alta, normal ou baixa). 
        O status do item é atualizado para "EM PROCESSAMENTO".
        '''
        
        try:
            # Procura primeiro os itens com prioridade alta
            item = self.var_clienteConection[self.var_strdbName][self.var_strColectionName].find_one_and_update(
                {'Status': 'NOVO', 'Prioridade': 'Alta'},
                {'$set': {'Status': 'EM PROCESSAMENTO'}},
                sort=[('Historico.0.Horas', pymongo.ASCENDING)],
                return_document=pymongo.ReturnDocument.AFTER
            )
            if item:
                self.update_item(item, 'EM PROCESSAMENTO')
                return item
            # Procura os itens com prioridade normal, caso não tenha encontrado com prioridade alta
            item = self.var_clienteConection[self.var_strdbName][self.var_strColectionName].find_one_and_update(
                {'Status': 'NOVO', 'Prioridade': 'Normal'},
                {'$set': {'Status': 'EM PROCESSAMENTO'}},
                sort=[('Historico.0.Horas', pymongo.ASCENDING)],
                return_document=pymongo.ReturnDocument.AFTER
            )
            if item:
                self.update_item(item, 'EM PROCESSAMENTO')
                return item
            # Procura os itens com prioridade baixa, caso não tenha encontrado com prioridade alta nem normal
            item = self.var_clienteConection[self.var_strdbName][self.var_strColectionName].find_one_and_update(
                {'Status': 'NOVO', 'Prioridade': 'Baixa'},
                {'$set': {'Status': 'EM PROCESSAMENTO'}},
                sort=[('Historico.0.Horas', pymongo.ASCENDING)],
                return_document=pymongo.ReturnDocument.AFTER
            )
            if item:
                self.update_item(item, 'EM PROCESSAMENTO')
                return item
            # Retorna None, caso não tenha encontrado nenhum item
            return None
        except Exception as e:
            print(f"Error updating next item: {e}")

    #Atualiza o Status do item
    def update_item(self, item, status):
        '''
        Atualiza o status do item. 
        Ele recebe como parâmetros o item e o novo status. 
        O método adiciona uma nova entrada no histórico do item com a ação "Iniciado Processamento".
        '''
        try:
            if item['Status'] == status:
                print(f"Item {item['_id']} já está em {status}")
            else:
                item['Status'] = status
            max_key = max(
                map(int, item['Historico'].keys())) if item['Historico'] else 0
            new_key = str(max_key + 1)
            new_action = {
                'Ação': 'Iniciado Processamento',
                'Autor': self.var_strHostname,
                'Status': status,
                'Revisor': self.var_strHostname,
                'Horas': datetime.now()
            }
            item['Atualizado'] = datetime.now()
            item['Historico'][new_key] = new_action
            # atualizar o registro no banco de dados
            self.var_clienteConection[self.var_strdbName][self.var_strColectionName].update_one(
                {'_id': item['_id']}, {'$set': item})
            print(f"Item {item['_id']} atualizado com sucesso")
        except Exception as e:
            print(f"Erro ao atualizar a fila: {e}")
    
    #Cria um Ativo
    def set_Asset(self, asset, valor):
        '''
        Responsável por adicionar um novo ativo à coleção de ativos. 
        Ele recebe como parâmetros o nome do ativo e o seu valor.
        '''
        Ativos = self.var_strColectionName+'_Ativos'
        var_dbMongoDB = self.var_clienteConection[self.var_strdbName]
        if Ativos in var_dbMongoDB.list_collection_names():
            print(f"Os ativos de {Ativos} foi setada")
        else:
            var_dbMongoDB = self.var_clienteConection[self.var_strdbName]
            codec_options = CodecOptions(tz_aware=True)
            var_MGcol = var_dbMongoDB.create_collection(
            Ativos, codec_options=codec_options)
            print(f"A fila Selecionada {Ativos} foi criada")
        json_asset={
            asset:valor
        }
        resultado = self.var_clienteConection[self.var_strdbName][Ativos].insert_one(json_asset)
        print('Asset ' + str(resultado.inserted_id) + ' inserido com sucesso')
    
    #Pesquisa um ativo
    def get_Asset(self, asset):
        '''
        Responsável por obter o valor de um ativo da coleção de ativos. 
        Ele recebe como parâmetro o nome do ativo.
        '''
        Ativos = self.var_strColectionName+'_Ativos'
        var_dbMongoDB = self.var_clienteConection[self.var_strdbName]
        if Ativos in var_dbMongoDB.list_collection_names():
            print(f"Os ativos de {Ativos} foi encontrado")
            resultado = self.var_clienteConection[self.var_strdbName][Ativos].find_one({asset:{'$exists':True}})
            if resultado:
                return resultado[asset]
            else:
                print(f"O ativo {asset} não foi encontrado")
                return None
        else:
            print(f"A coleção de ativos {Ativos} não existe")
            return None

