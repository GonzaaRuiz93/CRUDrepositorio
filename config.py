import os
from dotenv import load_dotenv

load_dotenv()

Tipo_BD = os.environ['Tipo_BD']
Usuario_BD = os.environ['Usuario_BD']
Password_BD = os.environ['Password_BD']
Host_BD = os.environ['Host_BD']
#Puerto_BD = os.environ['Puerto_BD']
Nombre_BD = os.environ['Nombre_BD']
SSLMode_BD = os.environ['SSLMode_BD']
Channel_Binding_BD =os.environ['Channel_Binding_BD']

#DATABASE_URI = os.environ['DATABASE_URL']

# Concatenamos todo y lo pasamos a SQLAlchemy
DATABASE_URI = f"{Tipo_BD}://{Usuario_BD}:{Password_BD}@{Host_BD}/{Nombre_BD}?sslmode={SSLMode_BD}&channel_binding={Channel_Binding_BD}"
# DATABASE_URI = f"{Tipo_BD}://{Usuario_BD}:{Password_BD}@{Host_BD}:{Puerto_BD}/{Nombre_BD}"
