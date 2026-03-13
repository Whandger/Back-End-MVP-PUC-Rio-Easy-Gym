from flask import Flask
from flask_cors import CORS 
import os
from sqlalchemy import create_engine, text
from server.config.config import ProductionConfig, DevelopmentConfig
from server import db
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def create_app():
    print("Iniciando app Flask...")

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '../../Front-end/templates'),
        static_folder=os.path.join(os.path.dirname(__file__), '../../Front-end/static')
    )

    # Configuração CORS - Permite arquivos locais e servidor
    CORS(app, supports_credentials=True)
    
    # Configuração ambiente
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)
        print("⚙️  Modo: Produção")
    else:
        app.config.from_object(DevelopmentConfig)
        print("⚙️  Modo: Desenvolvimento")

    # FORÇA SQLITE
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"🔗 Database URL: {db_url}")

    # Inicializa SQLAlchemy
    db.init_app(app)
    print("✅ SQLAlchemy inicializado")

    # Registrar blueprints
    from server.routes.dataroute import data_bp
    app.register_blueprint(data_bp)

    print("✅ Blueprints registrados")
    
    # Criar tabelas se não existirem
    with app.app_context():
        init_db()
    
    print("✅ App configurado com sucesso!")

    return app

# ---------------------------
# CRIAÇÃO DAS TABELAS
# ---------------------------
def init_db():
    try:
        db.session.execute(text("""
        CREATE TABLE IF NOT EXISTS Treino (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_treino TEXT NOT NULL
        )
        """))

        db.session.execute(text("""
        CREATE TABLE IF NOT EXISTS Exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_treino INTEGER,
            nome_exercicio TEXT,
            series INTEGER,
            repeticao INTEGER,
            FOREIGN KEY (id_treino) REFERENCES Treino(id) ON DELETE CASCADE
        )
        """))

        db.session.commit()
        print("✅ Tabelas verificadas/criadas com sucesso")
        
        # Teste de conexão SQLite
        engine = create_engine(db.session.get_bind().url)
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                ORDER BY name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Tabelas existentes: {tables}")

    except Exception as e:
        print(f"❌ ERRO ao criar tabelas: {str(e)[:200]}")


if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv('FLASK_ENV', 'development') != 'production'
    app.run(debug=debug_mode, port=int(os.getenv('APP_PORT', 5000)))