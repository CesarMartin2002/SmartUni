-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.9.3-beta1
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE new_database;
-- ddl-end --


-- object: public.Alumno | type: TABLE --
-- DROP TABLE IF EXISTS public.Alumno CASCADE;
CREATE TABLE public.Alumno (
	id_alumno serial NOT NULL,
	correo varchar(20),
	password varchar(20),
	CONSTRAINT Alumno_pk PRIMARY KEY (id_alumno)

);
-- ddl-end --
ALTER TABLE public.Alumno OWNER TO postgres;
-- ddl-end --

-- object: public.Aula | type: TABLE --
-- DROP TABLE IF EXISTS public.Aula CASCADE;
CREATE TABLE public.Aula (
	id_aula serial NOT NULL,
	temperatura integer,
	luminosidad integer,
	CONSTRAINT Aula_pk PRIMARY KEY (id_aula)

);
-- ddl-end --
ALTER TABLE public.Aula OWNER TO postgres;
-- ddl-end --

-- object: public.Asiento | type: TABLE --
-- DROP TABLE IF EXISTS public.Asiento CASCADE;
CREATE TABLE public.Asiento (
	id_asiento serial NOT NULL,
	id_aula_Aula integer NOT NULL,
	id_alumno_Alumno integer,
	CONSTRAINT Asiento_pk PRIMARY KEY (id_asiento)

);
-- ddl-end --
ALTER TABLE public.Asiento OWNER TO postgres;
-- ddl-end --

-- object: Aula_fk | type: CONSTRAINT --
-- ALTER TABLE public.Asiento DROP CONSTRAINT IF EXISTS Aula_fk CASCADE;
ALTER TABLE public.Asiento ADD CONSTRAINT Aula_fk FOREIGN KEY (id_aula_Aula)
REFERENCES public.Aula (id_aula) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: Alumno_fk | type: CONSTRAINT --
-- ALTER TABLE public.Asiento DROP CONSTRAINT IF EXISTS Alumno_fk CASCADE;
ALTER TABLE public.Asiento ADD CONSTRAINT Alumno_fk FOREIGN KEY (id_alumno_Alumno)
REFERENCES public.Alumno (id_alumno) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: Asiento_uq | type: CONSTRAINT --
-- ALTER TABLE public.Asiento DROP CONSTRAINT IF EXISTS Asiento_uq CASCADE;
ALTER TABLE public.Asiento ADD CONSTRAINT Asiento_uq UNIQUE (id_alumno_Alumno);
-- ddl-end --

-- object: public.Taquilla | type: TABLE --
-- DROP TABLE IF EXISTS public.Taquilla CASCADE;
CREATE TABLE public.Taquilla (
	id_taquilla serial NOT NULL,
	password integer,
	ala varchar(5),
	piso integer,
	pasillo integer,
	ocupado bool,
	id_alumno_Alumno integer,
	CONSTRAINT Taquilla_pk PRIMARY KEY (id_taquilla)

);
-- ddl-end --
ALTER TABLE public.Taquilla OWNER TO postgres;
-- ddl-end --

-- object: Alumno_fk | type: CONSTRAINT --
-- ALTER TABLE public.Taquilla DROP CONSTRAINT IF EXISTS Alumno_fk CASCADE;
ALTER TABLE public.Taquilla ADD CONSTRAINT Alumno_fk FOREIGN KEY (id_alumno_Alumno)
REFERENCES public.Alumno (id_alumno) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.Producto | type: TABLE --
-- DROP TABLE IF EXISTS public.Producto CASCADE;
CREATE TABLE public.Producto (
	id_producto serial NOT NULL,
	descripcion varchar(50),
	precio money,
	id_pedido_Pedido integer NOT NULL,
	id_empleado_Empelado integer NOT NULL,
	CONSTRAINT Producto_pk PRIMARY KEY (id_producto)

);
-- ddl-end --
ALTER TABLE public.Producto OWNER TO postgres;
-- ddl-end --

-- object: public.Asignatura | type: TABLE --
-- DROP TABLE IF EXISTS public.Asignatura CASCADE;
CREATE TABLE public.Asignatura (
	id_asignatura serial NOT NULL,
	descripcion varchar(50),
	id_aula_Aula integer NOT NULL,
	CONSTRAINT Asignatura_pk PRIMARY KEY (id_asignatura)

);
-- ddl-end --
ALTER TABLE public.Asignatura OWNER TO postgres;
-- ddl-end --

-- object: Aula_fk | type: CONSTRAINT --
-- ALTER TABLE public.Asignatura DROP CONSTRAINT IF EXISTS Aula_fk CASCADE;
ALTER TABLE public.Asignatura ADD CONSTRAINT Aula_fk FOREIGN KEY (id_aula_Aula)
REFERENCES public.Aula (id_aula) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.Pedido | type: TABLE --
-- DROP TABLE IF EXISTS public.Pedido CASCADE;
CREATE TABLE public.Pedido (
	id_pedido serial NOT NULL,
	estado varchar(15),
	id_alumno_Alumno integer NOT NULL,
	CONSTRAINT Pedido_pk PRIMARY KEY (id_pedido)

);
-- ddl-end --
ALTER TABLE public.Pedido OWNER TO postgres;
-- ddl-end --

-- object: Alumno_fk | type: CONSTRAINT --
-- ALTER TABLE public.Pedido DROP CONSTRAINT IF EXISTS Alumno_fk CASCADE;
ALTER TABLE public.Pedido ADD CONSTRAINT Alumno_fk FOREIGN KEY (id_alumno_Alumno)
REFERENCES public.Alumno (id_alumno) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: Pedido_fk | type: CONSTRAINT --
-- ALTER TABLE public.Producto DROP CONSTRAINT IF EXISTS Pedido_fk CASCADE;
ALTER TABLE public.Producto ADD CONSTRAINT Pedido_fk FOREIGN KEY (id_pedido_Pedido)
REFERENCES public.Pedido (id_pedido) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.NFC | type: TABLE --
-- DROP TABLE IF EXISTS public.NFC CASCADE;
CREATE TABLE public.NFC (
	id_NFC serial NOT NULL,
	id_pedido_Pedido integer,
	CONSTRAINT NFC_pk PRIMARY KEY (id_NFC)

);
-- ddl-end --
ALTER TABLE public.NFC OWNER TO postgres;
-- ddl-end --

-- object: Pedido_fk | type: CONSTRAINT --
-- ALTER TABLE public.NFC DROP CONSTRAINT IF EXISTS Pedido_fk CASCADE;
ALTER TABLE public.NFC ADD CONSTRAINT Pedido_fk FOREIGN KEY (id_pedido_Pedido)
REFERENCES public.Pedido (id_pedido) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: NFC_uq | type: CONSTRAINT --
-- ALTER TABLE public.NFC DROP CONSTRAINT IF EXISTS NFC_uq CASCADE;
ALTER TABLE public.NFC ADD CONSTRAINT NFC_uq UNIQUE (id_pedido_Pedido);
-- ddl-end --

-- object: public.Empelado | type: TABLE --
-- DROP TABLE IF EXISTS public.Empelado CASCADE;
CREATE TABLE public.Empelado (
	id_empleado serial NOT NULL,
	CONSTRAINT Empelado_pk PRIMARY KEY (id_empleado)

);
-- ddl-end --
ALTER TABLE public.Empelado OWNER TO postgres;
-- ddl-end --

-- object: Empelado_fk | type: CONSTRAINT --
-- ALTER TABLE public.Producto DROP CONSTRAINT IF EXISTS Empelado_fk CASCADE;
ALTER TABLE public.Producto ADD CONSTRAINT Empelado_fk FOREIGN KEY (id_empleado_Empelado)
REFERENCES public.Empelado (id_empleado) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.Horario | type: TABLE --
-- DROP TABLE IF EXISTS public.Horario CASCADE;
CREATE TABLE public.Horario (
	id_horario serial NOT NULL,
	dia date,
	hora_inicio time,
	hora_fin time,
	id_asignatura_Asignatura integer,
	CONSTRAINT Horario_pk PRIMARY KEY (id_horario)

);
-- ddl-end --
ALTER TABLE public.Horario OWNER TO postgres;
-- ddl-end --

-- object: Asignatura_fk | type: CONSTRAINT --
-- ALTER TABLE public.Horario DROP CONSTRAINT IF EXISTS Asignatura_fk CASCADE;
ALTER TABLE public.Horario ADD CONSTRAINT Asignatura_fk FOREIGN KEY (id_asignatura_Asignatura)
REFERENCES public.Asignatura (id_asignatura) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.Matricula | type: TABLE --
-- DROP TABLE IF EXISTS public.Matricula CASCADE;
CREATE TABLE public.Matricula (
	id_matricula serial NOT NULL,
	id_asignatura_Asignatura integer NOT NULL,
	id_alumno_Alumno integer NOT NULL,
	CONSTRAINT Matricula_pk PRIMARY KEY (id_matricula)

);
-- ddl-end --
ALTER TABLE public.Matricula OWNER TO postgres;
-- ddl-end --

-- object: Asignatura_fk | type: CONSTRAINT --
-- ALTER TABLE public.Matricula DROP CONSTRAINT IF EXISTS Asignatura_fk CASCADE;
ALTER TABLE public.Matricula ADD CONSTRAINT Asignatura_fk FOREIGN KEY (id_asignatura_Asignatura)
REFERENCES public.Asignatura (id_asignatura) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: Alumno_fk | type: CONSTRAINT --
-- ALTER TABLE public.Matricula DROP CONSTRAINT IF EXISTS Alumno_fk CASCADE;
ALTER TABLE public.Matricula ADD CONSTRAINT Alumno_fk FOREIGN KEY (id_alumno_Alumno)
REFERENCES public.Alumno (id_alumno) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

