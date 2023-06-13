import logica
import random
import time

def simulacion(usuario = 0, numero_aleatorio = 0):
    #region seleccionamos el usuario y la consulta
    if usuario == 0:
        usuarios = [5,6,7,9]
        usuario = random.choice(usuarios)
    if numero_aleatorio == 0:
        numero_aleatorio = random.randint(1, 4)
    #endregion
    #seleccionamos la consulta
    if numero_aleatorio == 1:
    #region se reserva una taquilla
        id_taquilla = random.randint(1, 10)
        if id_taquilla == 2:
            id_taquilla = 1
        print(f"\nSe va a reservar la taquilla {id_taquilla} para el usuario {usuario}")
        numero = random.randint(1000, 9999)
        json = {"password": numero,
            "id_alumno_alumno": usuario,
            "ocupado": True
            }
        try:
            logica.reservar_taquilla(id_taquilla, json)
            print("\nSe ha reservado la taquilla")
        except Exception as e:
            print()
            print(e)
    #endregion

    elif numero_aleatorio == 2:
        #region se simula la cancelación de una reserva
        id_taquilla = random.randint(1, 10)
        print(f"\nSe va a cancelar la reserva de la taquilla {id_taquilla} para el usuario {usuario}")
        try:
            logica.cancelar_taquilla(id_taquilla, usuario)
            print("\nSe ha cancelado la reserva")
        except Exception as e:
            print()
            print(e)
        #endregion
    elif numero_aleatorio == 3:
        #region se simula la solicitud de un pedido a la cafetería
        pedido = {"id_alumno" : usuario,"productos" : [1,2,3]}
        print(f"\nSe va a realizar un pedido a la cafetería para el usuario {usuario}")
        try:
            logica.crear_pedido(pedido)
            print("\nSe ha realizado el pedido")
        except Exception as e:
            print()
            print(e)
        #endregion
    else:
        #region se simula el avance del estado de un pedido
        #region obtenemos el primer pedido del usuario cuyo estado sea 3 o inferior
        try:
            pedidos = logica.obtener_pedidos(usuario)
        except Exception as e:
            print()
            print(e)
        #endregion
        #Ejemplo de pedido [{'id_pedido': 23, 'correo_alumno': 'luciapicadoj@gmail.com', 'productos_ids': [16], 'productos_descripciones': ['☕ cafe ☕'], 'estado': 0},{'id_pedido': 27, 'correo_alumno': 'luciapicadoj@gmail.com', 'productos_ids': [16], 'productos_descripciones': ['☕ cafe ☕'], 'estado': 4}]
        mi_pedido = None
        for pedido in pedidos:
            if pedido['estado'] <= 3:
                mi_pedido = pedido
                break  # Termina el bucle si se encuentra el primer pedido con estado <= 3
        if mi_pedido is not None:
            id_pedido = mi_pedido["id_pedido"]
            pedido_actualizado = {"id_alumno" : usuario,"estado": mi_pedido["estado"] + 1}
            try:
                logica.actualizar_pedido(id_pedido, pedido_actualizado)
                print(f"\nSe ha actualizado el pedido {id_pedido}")
            except Exception as e:
                print()
                print(e)
        else:
            print("El alumno no tiene pedidos para avanzar")
        #endregion
            

try:
    while True:
        simulacion()
        print("\nSe esperarán 5 segundos para la siguiente simulación")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nEjecución interrumpida por el usuario")