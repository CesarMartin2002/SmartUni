# Para levantar el frontend y el backend

En primer lugar deberemos crear el entorno virtual donde se instalarán todas las dependencias.
Para ello podemos abrir el fichero ```cargador env.bat```
O, podemos ejecutar el siguiente comando:
```
python -m venv env
```
Una vez creado el entorno virtual debemos acceder al mismo. Si se ha creado el entorno con el fichero .bat, este paso se realizará automáticamente.
Si se ha creado con el comando o no es la primera vez que se quiere utilizar el entorno, debemos ejecutar:
```
env\Scripts\activate.bat
```

Una vez nos encontremos en el entorno virtual, debemos instalar todas las librerías en el mismo.
Para ello basta con símplemente ejcutar:
```
pip install -r requirements.txt
```

Una vez instaladas todas estas librerías podemos proceder a levantar el servidor con **uvicorn**  
Para ello podemos ejecutar este comando:
```
uvicorn --app-dir=BACK/ main:app --port 0.0.0.0 --reload  
```

## Funcionamiento

Una vez levantado el servidor por defecto se va a alojar en [localhost:8000](http://localhost:8000/) .  
Ahora podremos realizar todos los cambios que deseemos, y simplemente al guardar se va a actualizar la información en tiempo real y podremos llamar a los empujones de nuevo y ver cómo efectivamente se han aplicado los cambios.

## Documentación

Para acceder a la documentación podemos usar el siguiente enlace: [localhost:8000/docs](http://localhost:8000/docs).  
Se puede accceder a la documentación alternativa utilizando este otro enlace: [localhost:8000/redoc](http://localhost:8000/redoc)

