# Backend - API de Treinos

Este projeto é a API backend responsável pelo gerenciamento de treinos e exercícios.  
Desenvolvido com Flask, SQLAlchemy e SQLite, fornece endpoints para criar, ler, atualizar e deletar dados relacionados a treinos e seus exercícios associados.

---

## Instruções de Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior instalado  
- Git instalado  
- Ambiente virtual (opcional, mas recomendado)  

### 2. Clonar o repositório


git clone <URL_DO_REPOSITORIO_BACKEND>
cd <NOME_DA_PASTA_BACKEND>
3. Configurar ambiente virtual (opcional)

No Linux/macOS:

python3 -m venv venv
source venv/bin/activate

No Windows:

python -m venv venv
venv\Scripts\activate
4. Instalar dependências
pip install -r requirements.txt
5. Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto com as variáveis:

FLASK_ENV=development
APP_PORT=5000
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=sqlite:///database.db
6. Executar a aplicação
python run.py

Por padrão, o servidor estará disponível em http://localhost:5000.

Estrutura do Projeto

server/ - Contém os arquivos da API (configurações, rotas, inicialização)

config/ - Classes de configuração para diferentes ambientes

run.py e run_app.bat - Scripts para iniciar o servidor

.env - Arquivo para variáveis de ambiente

Funcionalidades Principais

Criação, leitura, atualização e exclusão de treinos e exercícios

Utiliza SQLite como banco de dados padrão, com possibilidade de configurar outro banco via variável de ambiente

Configuração CORS para integração com front-end local ou remoto
