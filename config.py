import os
from dotenv import load_dotenv

load_dotenv()

Tipo_BD = os.environ['Tipo_BD']
Usuario_BD = os.environ['Usuario_BD']
Password_BD = os.environ['Password_BD']
Host_BD = os.environ['Host_BD']
Puerto_BD = os.environ['Puerto_BD']
Nombre_BD = os.environ['Nombre_BD']


# Concatenamos todo y lo pasamos a SQLAlchemy
DATABASE_URI = f"{Tipo_BD}://{Usuario_BD}:{Password_BD}@{Host_BD}:{Puerto_BD}/{Nombre_BD}"

if 'localhost' not in DATABASE_URI and '127.0.0.1' not in DATABASE_URI:
        if '?' in DATABASE_URI:
            DATABASE_URI += '&sslmode=require'
        else:
            DATABASE_URI += '?sslmode=require'