--Vista pedidos
CREATE OR REPLACE VIEW public.vista_pedidos
AS SELECT pedido.id_pedido,
    pedido.id_alumno_alumno,
    string_agg(pedido_producto.id_producto_producto::text, '|'::text ORDER BY pedido_producto.id_pedido_producto) AS productos_ids,
    string_agg(producto.descripcion::text, '|'::text ORDER BY pedido_producto.id_pedido_producto) AS productos_descripciones,
    pedido.estado,
    alumno.correo AS correo_alumno,
    nfc.id_nfc,
    nfc.num_serie
   FROM pedido
     JOIN alumno ON pedido.id_alumno_alumno = alumno.id_alumno
     left JOIN pedido_producto ON pedido.id_pedido = pedido_producto.id_pedido_pedido
     left JOIN producto ON pedido_producto.id_producto_producto = producto.id_producto
     LEFT JOIN nfc ON pedido.id_pedido = nfc.id_pedido_pedido
  GROUP BY pedido.id_pedido, pedido.id_alumno_alumno, pedido.estado, alumno.correo, nfc.id_nfc, nfc.num_serie;
--Vista asignaturas
CREATE OR REPLACE VIEW public.vista_asignaturas
AS SELECT asignatura.id_asignatura,
    asignatura.descripcion,
    aula.id_aula,
    aula.laboratorio,
    aula.planta,
    aula.ala,
    horario.id_horario,
    horario.dia,
    horario.hora_inicio,
    horario.hora_fin,
    aula.num_ala,
    aula.temperatura
   FROM horario horario
     left JOIN aula aula ON horario.id_aula_aula = aula.id_aula
     left JOIN asignatura asignatura ON horario.id_asignatura_asignatura = asignatura.id_asignatura;
--Vista pedido estrella
CREATE VIEW vista_pedido_estrella AS
SELECT Pedido.id_pedido, Producto.id_producto, Producto.descripcion, Pedido.id_alumno_Alumno
FROM Pedido
JOIN Pedido_Producto ON Pedido.id_pedido = Pedido_Producto.id_pedido_Pedido
JOIN Producto ON Pedido_Producto.id_producto_Producto = Producto.id_producto;
--Vista resumen aula
CREATE OR REPLACE VIEW public.vista_resumen_aula
AS SELECT pc.id_aula,
    pc.id_asignatura,
    pc.nombre_asignatura,
    pc.fecha_inicio,
    pc.hora_inicio,
    pc.hora_fin,
        CASE
            WHEN pc.fecha_inicio = CURRENT_DATE AND pc.hora_inicio::time with time zone >= CURRENT_TIME OR pc.fecha_inicio > CURRENT_DATE THEN (date_part('epoch'::text, pc.fecha_inicio::timestamp without time zone + pc.hora_inicio::interval - (CURRENT_DATE::timestamp without time zone + CURRENT_TIME::time without time zone::interval)) / 60::double precision) < ta.tiempo_medio::double precision
            ELSE false
        END AS actuar,
    ta.tiempo_medio
   FROM ( SELECT a.id_aula,
            h.id_asignatura_asignatura AS id_asignatura,
            asig.descripcion AS nombre_asignatura,
            h.dia AS fecha_inicio,
            h.hora_inicio,
            h.hora_fin
           FROM aula a
             LEFT JOIN ( SELECT h_1.id_aula_aula,
                    h_1.id_asignatura_asignatura,
                    h_1.dia,
                    h_1.hora_inicio,
                    h_1.hora_fin
                   FROM horario h_1
                  WHERE h_1.dia >= CURRENT_DATE AND (h_1.dia > CURRENT_DATE OR h_1.hora_fin::time with time zone >= CURRENT_TIME)
                  ORDER BY h_1.dia, h_1.hora_inicio
                 LIMIT 1) h ON a.id_aula = h.id_aula_aula
             LEFT JOIN asignatura asig ON h.id_asignatura_asignatura = asig.id_asignatura) pc
     LEFT JOIN ( SELECT h.id_aula_aula AS id_aula,
            avg(h.tiempo_calentar) AS tiempo_medio
           FROM ( SELECT historico_aula.id_aula_aula,
                    historico_aula.tiempo_calentar
                   FROM historico_aula
                  ORDER BY historico_aula.id_historico_aula DESC
                 LIMIT 5) h
          GROUP BY h.id_aula_aula) ta ON pc.id_aula = ta.id_aula;