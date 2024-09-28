  
A classe FilaMongoDB é uma ferramenta desenvolvida para ser utilizada em conjunto com a plataforma BotCity, que é uma plataforma de automação robótica de processos (RPA). A plataforma BotCity permite a criação de robôs que automatizam tarefas repetitivas em diversos sistemas, como navegadores web, aplicativos desktop e bancos de dados.

FilaMongoDB é uma ferramenta que permite gerenciar uma fila de processamento de dados em um banco de dados MongoDB. Com ela, é possível adicionar itens à fila, atualizar o status dos itens, obter o próximo item a ser processado e gerenciar uma coleção de ativos. Essa ferramenta é muito útil para organizar e gerenciar o processamento de tarefas em um ambiente de automação robótica de processos.


## Pacotes importados
- pandas: um pacote popular para manipulação e análise de dados
- pymongo: um pacote que fornece uma API para interagir com o MongoDB a partir do Python
- bson.codec_options: um pacote para trabalhar com opções de codificação e decodificação JSON
- socket: um pacote para obter o nome do host da máquina
- datetime: um pacote para trabalhar com data e hora

## Classe FilaMongoDB
### Requisitos
- Pandas
- pymongo
- bson
- datetime
- socket

### Instalação
Não há necessidade de instalar bibliotecas adicionais para utilizar a classe `FilaMongoDB`, desde que já tenha as bibliotecas acima instaladas.

### Métodos da classe
__________________________
#### `__init__(self, var_strdbName, var_strColectionName)`

Construtor da classe `FilaMongoDB`. Recebe como parâmetros o nome do banco de dados e o nome da coleção onde a fila será armazenada. Caso o banco de dados ou a coleção não existam, a classe os criará automaticamente.
##### Parâmetros
-  `var_strdbName` : _string_ Nome do banco de dados onde a fila será armazenada.
-  `var_strColectionName` : _string_ Nome da coleção onde a fila será armazenada.
##### Exemplo
```python
`fila = FilaMongoDB('banco_de_dados', 'colecao_da_fila')`
```
__________________________
#### `Add_item(self, data_frame)`

Adiciona múltiplos itens na fila de uma vez. Recebe um objeto `data_frame` do Pandas como parâmetro, transforma o dataframe em um dicionário e adiciona cada registro como um item na fila.
##### Parâmetros

-  `data_frame` : pandas.DataFrame Objeto dataframe do Pandas que contém os registros a serem adicionados à fila.

##### Exemplo
```python
    df = pd.DataFrame({
    'nome': ['João', 'Maria', 'José'],
    'idade': [25, 30, 35],   
    })

    fila.Add_item(df)`
```
      
__________________________
#### `next_item(self)`

O método `next_item` é responsável por retornar o próximo item da fila a ser processado. O método retorna o próximo item de acordo com a prioridade de execução (alta, normal ou baixa). O status do item é atualizado para "EM PROCESSAMENTO".

##### Retorno
-  `item` :_Dicionario_ Dicionário com as informações do próximo item a ser processado.

##### Exemplo
```python
item = fila.next_item()
```
#### `update_item(self, item, status)`

O método `update_item` é responsável por atualizar o status do item. Ele recebe como parâmetros o item e o novo status. O método adiciona uma nova entrada no histórico do item com a ação "Iniciado Processamento".

##### Parâmetros

-  `item` : _Dicionario_ dicionário com as informações do item a ser atualizado.

-  `status` : _String_ string que representa o novo status do item.

##### Exemplo
```python
    fila.update_item(item, "CONCLUÍDO")
```
#### `next_item(self)`

O método `next_item` é responsável por retornar o próximo item da fila a ser processado. O método retorna o próximo item conforme a prioridade de execução (alta, normal ou baixa). O status do item é atualizado para "EM PROCESSAMENTO".

##### Retorno
-  `item` :_Dicionario_ Dicionário com as informações do próximo item a ser processado.

##### Exemplo
```python
item = fila.next_item()
```
#### `set_Asset(self, asset, valor)`

O método `set_Asset` é responsável por adicionar um novo ativo à coleção de ativos. Ele recebe como parâmetros o nome do ativo e o seu valor.

##### Parâmetros
-  `asset` :_String_ string que dita o nome do asset a ser criado na nova coleção.
-  `valor` : _String_ string que representa o novo valor a ser adicionado no `asset`.
##### Exemplo
```python
    fila.set_Asset("ativo1", 10)
```
#### `get_Asset(self, asset)`
O método `get_Asset` é responsável por obter o valor de um ativo da coleção de ativos. Ele recebe como parâmetro o nome do ativo.

##### Parâmetros

  -  `asset` :_String_ string que dita o nome do asset a ser pesquisado na coleção.
##### Exemplo
```python
    valor = fila.get_Asset("ativo1")
    print(valor)
```
  
## Exemplos de uso

### Exemplo 1: Criando uma nova fila e adicionando um único item

#### Importar bibliotecas necessárias
```python
    import pandas as pd
    from datetime import datetime    
    from fila_mongodb import FilaMongoDB
```
#### Criar uma instância da classe FilaMongoDB
```python
    fila = FilaMongoDB('minha_base', 'minha_fila')
```
#### Criar um dataframe com um único registro
```python
    df = pd.DataFrame({'nome': ['João'], 'idade': [30], 'data_cadastro': [datetime.now()]})
```
#### Adicionar o registro à fila
```python
    fila.Add_item(df)
```
### Exemplo 2: Adicionando vários itens de uma só vez

#### Criar um dataframe com vários registros
```python
    df = pd.DataFrame({
    'nome': ['João', 'Maria', 'José'], 
    'idade': [30, 25, 40], 
    'data_cadastro': [datetime.now(),
     datetime.now(), datetime.now()]
     })
```
#### Adicionar os registros à fila de uma só vez
```python
    fila.bulk_Add_item(df)
```
### Exemplo 3: Buscando o próximo item da fila para processamento


#### Obter o próximo item da fila
```python
    item = fila.next_item()
    if item:
        # Processar o item...
    else:
        print('Não há itens para processar')
```
### Exemplo 4: Atualizando o status de um item da fila

 #### Obter um item da fila (por exemplo, usando o método next_item)
```python
item = fila.next_item()
```
#### Atualizar o status do item para "CONCLUÍDO"

    fila.update_item(item, 'CONCLUÍDO')

### Exemplo 5: Adicionando um ativo 
```python
fila.set_Asset("ativo1", 10)
```
### Exemplo 6: Recuperando um ativo 
```python
valor = fila.get_Asset("ativo1")
print(valor)
```
# MongoDB

No Atlas Mongo DB as coleções geradas pelo codigo apresentado se comportam em um esquema não relacional de banco de dados apresentado como um esquema abaixo:

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
	}
	
Os dados são atualizados são atualizados dentro do codigo, e os campos de infromações alimentam um B.I. criado dentro da plataforma do atlas, uma ferramenta chamada Charts. Abaixo tem um exemplo de um possivel conjunto de infromações disponiveis.
![Imagem descritiva dos graficos do Atlas](https://i.imgur.com/1GMwFxj.png)

