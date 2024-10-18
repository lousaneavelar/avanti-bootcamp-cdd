import requests
import os
import subprocess

# Função para baixar dados
def baixar_dados(url, caminho_pasta, nome_arquivo):
    # Verifica se a pasta existe, e cria se necessário
    os.makedirs(caminho_pasta, exist_ok=True)

    # Caminho completo do arquivo onde será salvo
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

    # Realiza o download dos dados
    response = requests.get(url)
    if response.status_code == 200:
        with open(caminho_arquivo, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo salvo em: data/raw/penguins.csv")
        return caminho_arquivo
    else:
        print(f"Erro ao baixar dados. Status code: {response.status_code}")
        return None

# Função para executar comandos Git
def executar_comando_git(comando):
    try:
        # Executa o comando no terminal
        resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
        print(f"Comando '{comando}' executado com sucesso.")
        print(resultado.stdout)
    except subprocess.CalledProcessError as erro:
        print(f"Erro ao executar o comando: {erro}")
        print(erro.stderr)

# Função para fazer o commit e push no Git
def git_commit_push(caminho_arquivo, mensagem_commit):
    # Adiciona o arquivo ao índice
    executar_comando_git(['git', 'add', caminho_arquivo])
    
    # Faz o commit
    executar_comando_git(['git', 'commit', '-m', mensagem_commit])
    
    # Envia as mudanças para o repositório remoto
    executar_comando_git(['git', 'push'])

# URL de exemplo de um arquivo CSV
url_dados = 'https://github.com/atlantico-academy/datasets/blob/main/penguins.csv'

# Definindo a pasta e o nome do arquivo
pasta_destino = 'data/raw'
nome_arquivo = 'penguins.csv'

# Coletando os dados e salvando no diretório
caminho_arquivo_baixado = baixar_dados(url_dados, pasta_destino, nome_arquivo)

# Se o download foi bem-sucedido, faz o commit e push
if caminho_arquivo_baixado:
    git_commit_push(caminho_arquivo_baixado, "Adiciona dados coletados à pasta data/raw")
