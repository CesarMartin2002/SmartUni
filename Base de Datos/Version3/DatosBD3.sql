--ALUMNO(id, correo, password)
INSERT INTO ALUMNO (correo, password) VALUES ('juan@edu.uah.es', 'juan1234');
INSERT INTO ALUMNO (correo, password) VALUES('maria@edu.uah.es', 'm4r142023');
INSERT INTO ALUMNO (correo, password) VALUES('sonia@edu.uah.es', 's0n145790');
INSERT INTO ALUMNO (correo, password) VALUES ('manuel@edu.uah.es', 'm4nu3l2020');
--SELECT * FROM ALUMNO;

--AULA(id, temp, lum, lab, planta, ala, num_ala)
INSERT INTO AULA (temperatura, luminosidad, laboratorio, planta, ala, num_ala) VALUES (20, 40, FALSE, 1, 'este', 1);
INSERT INTO AULA (temperatura, luminosidad, laboratorio, planta, ala, num_ala) VALUES (18, 60, FALSE, 1, 'oeste', 2);
INSERT INTO AULA (temperatura, luminosidad, laboratorio, planta, ala, num_ala) VALUES (23, 80, TRUE, 2, 'norte', 2);
--SELECT * FROM AULA;

--ASIENTO(id, id_aula, id_alumno)
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (1, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (1, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (1, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (2, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (2, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (2, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (3, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (3, null);
INSERT INTO ASIENTO (id_aula_Aula, id_alumno_Alumno) VALUES (3, null);
--SELECT * FROM ASIENTO;

--TAQUILLA(id, password, ala, piso, pasillo, ocupado, id_alumno)
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('1234', 'este', 1, 1, TRUE, 1);
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('4512', 'este', 2, 1, FALSE, null);
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('8888', 'norte', 1, 1, FALSE, null);
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('1200', 'oeste', 1, 2, FALSE, null); 
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('6975', 'norte', 1, 2, FALSE, null);
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('4638', 'oeste', 2, 2, FALSE, null);
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('3597', 'sur', 2, 2, FALSE, null);
INSERT INTO TAQUILLA (password, ala, piso, pasillo, ocupado, id_alumno_Alumno) VALUES ('4687', 'sur', 2, 1, FALSE, null);
--SELECT * FROM TAQUILLA;

--EMPLEADO(id)
INSERT INTO EMPLEADO DEFAULT VALUES;
--SELECT * FROM EMPLEADO

--PRODUCTO(id, descripcion, precio, id_empleado)
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('bocadillo de lomo', 2.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('bocadillo de bacon', 2.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('bocadillo de tortilla', 2.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('bocadillo de pollo', 2.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('bocadillo de francesa', 2.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('bocadillo de atun', 2.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('extra queso', 0.50, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('extra tomate', 0.50, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('extra pimiento', 0.50, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('extra huevo', 0.70, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('extra bacon', 0.70, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('sandwich mixto', 1.80, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('sandwich vegetal', 2.50, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('hamburguesa con patatas', 4.00, 1);
INSERT INTO PRODUCTO (descripcion, precio, id_empleado_Empleado) VALUES ('ensalada', 4.00, 1);
--SELECT * FROM PRODUCTO;

--ASIGNATURA(id, descripcion)
INSERT INTO ASIGNATURA (descripcion) VALUES ('Gestion de Proyectos');
INSERT INTO ASIGNATURA (descripcion) VALUES ('Sistemas Empresariales');
INSERT INTO ASIGNATURA (descripcion) VALUES ('Estructuras Discretas');
INSERT INTO ASIGNATURA (descripcion) VALUES ('CRA');
INSERT INTO ASIGNATURA (descripcion) VALUES ('Gestion de Proyectos');
--SELECT * FROM ASIGNATURA;

--PEDIDO(id, estado, id_alumno)
INSERT INTO PEDIDO (estado, id_alumno_Alumno) VALUES ('0',3);
INSERT INTO PEDIDO (estado, id_alumno_Alumno) VALUES ('0',3);
INSERT INTO PEDIDO (estado, id_alumno_Alumno) VALUES ('0',3);
--SELECT * FROM PEDIDO

--PEDIDO_PRODUCTO (id, id_pedido, id_producto)
INSERT INTO PEDIDO_PRODUCTO (id_pedido_Pedido, id_producto_Producto) VALUES (1,1);
INSERT INTO PEDIDO_PRODUCTO (id_pedido_Pedido, id_producto_Producto) VALUES (2,2);
INSERT INTO PEDIDO_PRODUCTO (id_pedido_Pedido, id_producto_Producto) VALUES (2,3);
INSERT INTO PEDIDO_PRODUCTO (id_pedido_Pedido, id_producto_Producto) VALUES (3,1);
INSERT INTO PEDIDO_PRODUCTO (id_pedido_Pedido, id_producto_Producto) VALUES (3,2);
INSERT INTO PEDIDO_PRODUCTO (id_pedido_Pedido, id_producto_Producto) VALUES (3,3);
--SELECT * FROM PEDIDO_PRODUCTO

--NFC (id, id_pedido, num_serie)
INSERT INTO NFC (id_pedido_Pedido, num_serie) VALUES (null,'04:3c:b0:56:70:00:00');
INSERT INTO NFC (id_pedido_Pedido, num_serie) VALUES (null,'04:ef:8e:56:70:00:00');
--SELECT * FROM NFC

--HORARIO (id, dia, hora_inicio, hora_fin, id_asignatura, id_aula)
INSERT INTO HORARIO (dia, hora_inicio, hora_fin, id_asignatura_Asignatura, id_aula_Aula) VALUES ('2023/05/30','08:00','10:00',1, 1);
INSERT INTO HORARIO (dia, hora_inicio, hora_fin, id_asignatura_Asignatura, id_aula_Aula) VALUES ('2023/05/31','08:00','10:00',1, 2);
--SELECT * FROM HORARIO

--MATRICULA (id, id_asignatura, id_alumno)
INSERT INTO MATRICULA (id_asignatura_Asignatura, id_alumno_Alumno) VALUES ();
--SELECT * FROM MATRICULA

--HISTORICO_AULA (id, temp, tiempo, id_aula)
INSERT INTO HISTORICO_AULA (temperatura_previa, tiempo_calentar, id_aula_Aula) VALUES ();
--SELECT * FROM HISTORICO_AULA