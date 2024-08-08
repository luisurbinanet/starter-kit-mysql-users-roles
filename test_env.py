import os
from dotenv import load_dotenv, dotenv_values

dotenv_path = '.env'

print(f"Attempting to load .env file from: {dotenv_path}")

if os.path.exists(dotenv_path):
    print(f".env file found at: {dotenv_path}")
    
    # Leer y mostrar el contenido del archivo .env
    with open(dotenv_path, 'r') as file:
        content = file.read()
        print("Contenido del archivo .env:")
        print(content)
    
    # Verificar si SECRET_KEY ya está definida en el entorno
    if 'SECRET_KEY' in os.environ:
        print(f"APP_SECRET_KEY already defined in environment before loading .env: {os.environ['SECRET_KEY']}")
    else:
        print("APP_SECRET_KEY not found in environment before loading .env")

    # Cargar variables de entorno desde el archivo .env
    load_dotenv(dotenv_path)

    # Verificar si SECRET_KEY se ha cargado
    if 'SECRET_KEY' in os.environ:
        print(f"SECRET_KEY found in environment after loading .env: {os.environ['SECRET_KEY']}")
    else:
        print("SECRET_KEY not found in environment after loading .env")

    # Cargar variables de entorno manualmente
    env_values = dotenv_values(dotenv_path)
    print("Manual load of .env values:")
    for key, value in env_values.items():
        print(f"{key}: {value}")

    print("Environment variables after loading .env:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

    secret_key = os.getenv('APP_SECRET_KEY')
    if secret_key:
        print(f"APP_SECRET_KEY from .env: {secret_key}")
    else:
        print("APP_SECRET_KEY not found in .env")

else:
    print(f".env file not found at: {dotenv_path}")
