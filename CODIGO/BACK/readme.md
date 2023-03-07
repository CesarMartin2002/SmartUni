# Para usar el backend

En primer lugar deberemos utilizar el entorno virtual que se encuentra en fastapi-env
Para ello podemos ejecutar este comando:
```
fastapi-env\Scripts\activate
```
Una vez nos encontremos en el entorno virtual, debemos levantar el servidor con **uvicorn**
Para ello podemos ejecutar este comando:
```
uvicorn main:app --reload
```

## Funcionamiento

Una vez levantado el servidor por defecto se va a alojar en [localhost:8000](http://localhost:8000/) .  
Ahora podremos realizar todos los cambios que deseemos, y simplemente al guardar se va a actualizar la información en tiempo real y podremos llamar a los empujones de nuevo y ver cómo efectivamente se han aplicado los cambios.

##Documentación

Para acceder a la documentación podemos usar el siguiente enlace: [localhost:8000/docs](http://localhost:8000/docs)

