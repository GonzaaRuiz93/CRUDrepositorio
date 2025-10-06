import os
from dotenv import load_dotenv

load_dotenv()

Tipo_BD = os.environ['Tipo_BD']
Usuario_BD = os.environ['Usuario_BD']
Password_BD = os.environ['Password_BD']
Host_BD = os.environ['Host_BD']
Puerto_BD = os.environ['Puerto_BD']
Nombre_BD = os.environ['Nombre_BD']

DATABASE_URI = os.environ['DATABASE_URL']

# Concatenamos todo y lo pasamos a SQLAlchemy
# DATABASE_URI = f"{Tipo_BD}://{Usuario_BD}:{Password_BD}@{Host_BD}:{Puerto_BD}/{Nombre_BD}"

