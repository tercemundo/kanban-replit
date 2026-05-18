import os
import sys
import connexion
from flask_cors import CORS
from database import engine, Base

# Añadir la carpeta actual al path de Python para que Connexion resuelva handlers.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Auto-crear las tablas de base de datos en caso de iniciar sin Alembic de inmediato
Base.metadata.create_all(bind=engine)

# Inicializar Connexion
# specification_dir apunta al directorio del openapi.yaml
spec_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../shared/api-spec'))
app = connexion.FlaskApp(__name__, specification_dir=spec_dir)

# Agregar la API
# resolver_placeholder='handlers' le indica a Connexion que busque cada operationId en handlers.py
app.add_api('openapi.yaml', resolver_placeholder='handlers')

# Habilitar CORS en el servidor Flask subyacente para el frontend
CORS(app.app, supports_credentials=True, origins=["http://localhost:18929", "http://127.0.0.1:18929"])

flask_app = app.app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(port=port, host="0.0.0.0")
