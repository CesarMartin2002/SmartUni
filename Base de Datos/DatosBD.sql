--ALUMNO(id, correo, password)
INSERT INTO ALUMNO VALUES (1, 'juan@edu.uah.es', 'juan1234');
INSERT INTO ALUMNO VALUES (2, 'maria@edu.uah.es', 'm4r142023');
INSERT INTO ALUMNO VALUES (3, 'sonia@edu.uah.es', 's0n145790');
INSERT INTO ALUMNO VALUES (4, 'manuel@edu.uah.es', 'm4nu3l2020');
--SELECT * FROM ALUMNO;

--AULA(id, temp, lum)
INSERT INTO AULA VALUES (1, 20, 40);
INSERT INTO AULA VALUES (2, 18, 60);
INSERT INTO AULA VALUES (3, 23, 80);
--SELECT * FROM AULA;

--ASIENTO(id, id_aula, id_alumno)
INSERT INTO ASIENTO VALUES (1, 1, null);
INSERT INTO ASIENTO VALUES (2, 1, null);
INSERT INTO ASIENTO VALUES (3, 1, null);
INSERT INTO ASIENTO VALUES (4, 2, null);
INSERT INTO ASIENTO VALUES (5, 2, null);
INSERT INTO ASIENTO VALUES (6, 2, null);
INSERT INTO ASIENTO VALUES (7, 3, null);
INSERT INTO ASIENTO VALUES (8, 3, null);
INSERT INTO ASIENTO VALUES (9, 3, null);
--SELECT * FROM ASIENTO;

--TAQUILLA(id, password, ala, piso, pasillo, ocupado, id_alumno)
INSERT INTO TAQUILLA VALUES (1, 1234, 'este', 1, 1, FALSE, null);
INSERT INTO TAQUILLA VALUES (2, 4512, 'este', 2, 1, FALSE, null);
INSERT INTO TAQUILLA VALUES (3, 8888, 'norte', 1, 1, FALSE, null);
INSERT INTO TAQUILLA VALUES (4, 1200, 'oeste', 1, 2, FALSE, null); 
INSERT INTO TAQUILLA VALUES (5, 6975, 'norte', 1, 2, FALSE, null);
INSERT INTO TAQUILLA VALUES (6, 4638, 'oeste', 2, 2, FALSE, null);
INSERT INTO TAQUILLA VALUES (7, 3597, 'sur', 2, 2, FALSE, null);
INSERT INTO TAQUILLA VALUES (8, 4687, 'sur', 2, 1, FALSE, null);
--SELECT * FROM TAQUILLA;

--CAFETERIA(id)
INSERT INTO CAFETERIA VALUES (1);
--SELECT * FROM CAFETERIA

--PRODUCTO(id, descripcion, precio, id_cafeteria)
INSERT INTO PRODUCTO VALUES (1, 'bocadillo de lomo', 2.00, 1);
INSERT INTO PRODUCTO VALUES (2, 'bocadillo de bacon', 2.00, 1);
INSERT INTO PRODUCTO VALUES (3, 'bocadillo de tortilla', 2.00, 1);
INSERT INTO PRODUCTO VALUES (4, 'bocadillo de pollo', 2.00, 1);
INSERT INTO PRODUCTO VALUES (5, 'bocadillo de francesa', 2.00, 1);
INSERT INTO PRODUCTO VALUES (6, 'bocadillo de atun', 2.00, 1);
INSERT INTO PRODUCTO VALUES (7, 'extra queso', 0.50, 1);
INSERT INTO PRODUCTO VALUES (8, 'extra tomate', 0.50, 1);
INSERT INTO PRODUCTO VALUES (9, 'extra pimiento', 0.50, 1);
INSERT INTO PRODUCTO VALUES (10, 'extra huevo', 0.70, 1);
INSERT INTO PRODUCTO VALUES (11, 'extra bacon', 0.70, 1);
INSERT INTO PRODUCTO VALUES (12, 'sandwich mixto', 1.80, 1);
INSERT INTO PRODUCTO VALUES (13, 'sandwich vegetal', 2.50, 1);
INSERT INTO PRODUCTO VALUES (14, 'hamburguesa con patatas', 4.00, 1);
INSERT INTO PRODUCTO VALUES (15, 'ensalada', 4.00, 1);
--SELECT * FROM PRODUCTO;

--ASIGNATURA(id, descripcion, horario, id_aula)
INSERT INTO ASIGNATURA VALUES (1,'Gestion de Proyectos','08:00', 1);
INSERT INTO ASIGNATURA VALUES (2, 'Sistemas Empresariales', '10:00', 1);
INSERT INTO ASIGNATURA VALUES (3,'Estructuras Discretas','08:00', 2);
INSERT INTO ASIGNATURA VALUES (4,'CRA','12:00', 1);
INSERT INTO ASIGNATURA VALUES (5,'Gestion de Proyectos','10:00', 2);
--SELECT * FROM ASIGNATURA;