-- Database generated with pgModeler (aotdlhviQL Database Modeler).
-- pgModeler  version: 0.9.3-beta1
-- aotdlhviQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE new_database;
-- ddl-end --


-- object: public.Alumno | type: TABLE --
-- DROP TABLE IF EXISTS public.Alumno CASCADE;
CREATE TABLE public.Alumno (
	id_alumno varchar(20) NOT NULL,
	correo varchar(20),
	password varchar(20),
	CONSTRAINT Alumno_pk PRIMARY KEY (id_alumno)

);
-- ddl-end --
ALTER TABLE public.Alumno OWNER TO aotdlhvi;
-- ddl-end --

-- object: public.Aula | type: TABLE --
-- DROP TABLE IF EXISTS public.Aula CASCADE;
CREATE TABLE public.Aula (
	id_aula varchar(20) NOT NULL,
	temperatura integer,
	luminosidad integer,
	CONSTRAINT Aula_pk PRIMARY KEY (id_aula)

);
-- ddl-end --
ALTER TABLE public.Aula OWNER TO aotdlhvi;
-- ddl-end --

-- object: public.Asiento | type: TABLE --
-- DROP TABLE IF EXISTS public.Asiento CASCADE;
CREATE TABLE public.Asiento (
	id_asiento varchar(20) NOT NULL,
	id_aula_Aula varchar(20) NOT NULL,
	id_alumno_Alumno varchar(20),
	CONSTRAINT Asiento_pk PRIMARY KEY (id_asiento)

);
-- ddl-end --
ALTER TABLE public.Asiento OWNER TO aotdlhvi;
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
	id_taquilla varchar(20) NOT NULL,
	password integer,
	ala varchar(5),
	piso integer,
	pasillo integer,
	ocupado bool,
	id_alumno_Alumno varchar(20),
	CONSTRAINT Taquilla_pk PRIMARY KEY (id_taquilla)

);
-- ddl-end --
ALTER TABLE public.Taquilla OWNER TO aotdlhvi;
-- ddl-end --

-- object: Alumno_fk | type: CONSTRAINT --
-- ALTER TABLE public.Taquilla DROP CONSTRAINT IF EXISTS Alumno_fk CASCADE;
ALTER TABLE public.Taquilla ADD CONSTRAINT Alumno_fk FOREIGN KEY (id_alumno_Alumno)
REFERENCES public.Alumno (id_alumno) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.Cafeteria | type: TABLE --
-- DROP TABLE IF EXISTS public.Cafeteria CASCADE;
CREATE TABLE public.Cafeteria (
	id_cafeteria varchar(20) NOT NULL,
	CONSTRAINT Cafeteria_pk PRIMARY KEY (id_cafeteria)

);
-- ddl-end --
ALTER TABLE public.Cafeteria OWNER TO aotdlhvi;
-- ddl-end --

-- object: public.Producto | type: TABLE --
-- DROP TABLE IF EXISTS public.Producto CASCADE;
CREATE TABLE public.Producto (
	id_producto varchar(20) NOT NULL,
	descripcion varchar(50),
	precio money,
	id_cafeteria_Cafeteria varchar(20) NOT NULL,
	CONSTRAINT Producto_pk PRIMARY KEY (id_producto)

);
-- ddl-end --
ALTER TABLE public.Producto OWNER TO aotdlhvi;
-- ddl-end --

-- object: Cafeteria_fk | type: CONSTRAINT --
-- ALTER TABLE public.Producto DROP CONSTRAINT IF EXISTS Cafeteria_fk CASCADE;
ALTER TABLE public.Producto ADD CONSTRAINT Cafeteria_fk FOREIGN KEY (id_cafeteria_Cafeteria)
REFERENCES public.Cafeteria (id_cafeteria) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.Asignatura | type: TABLE --
-- DROP TABLE IF EXISTS public.Asignatura CASCADE;
CREATE TABLE public.Asignatura (
	id_asignatura varchar(20) NOT NULL,
	descripcion varchar(50),
	horario time,
	id_aula_Aula varchar(20) NOT NULL,
	CONSTRAINT Asignatura_pk PRIMARY KEY (id_asignatura)

);
-- ddl-end --
ALTER TABLE public.Asignatura OWNER TO aotdlhvi;
-- ddl-end --

-- object: Aula_fk | type: CONSTRAINT --
-- ALTER TABLE public.Asignatura DROP CONSTRAINT IF EXISTS Aula_fk CASCADE;
ALTER TABLE public.Asignatura ADD CONSTRAINT Aula_fk FOREIGN KEY (id_aula_Aula)
REFERENCES public.Aula (id_aula) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


