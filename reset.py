import os
import sys

# Esto ayuda a que el script encuentre la carpeta src
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app import app
from api.models import db

with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("✅ TODO LIMPIO Y BASE DE DATOS CREADA DESDE CERO")
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")