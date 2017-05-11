CREATE TABLE oficinas (
	id_oficina integer,
	direccion varchar(30),
	constraint oficina_pk primary key (id_oficina)

);


CREATE TABLE contratos (
	id_tipo_contrato integer,
	tipo varchar(20),
	costo float,
	constraint tipo_contrato_pk primary key (id_tipo_contrato)

);



CREATE TABLE estados (
	id_estado_cliente integer,
	estado varchar(20),
	constraint estado_pk primary key (id_estado_cliente)

);



CREATE TABLE tipos_cliente (
	id_tipo_cliente integer,
	tipo varchar(20),
	descuento float,
	constraint tipo_cliente_pk primary key (id_tipo_cliente)

);




CREATE TABLE nuevos_campos (
	id_campo integer,
	campo varchar(40),
	tipo varchar(10),
	constraint campo_pk primary key (id_campo)
);



CREATE TABLE clientes (
	id_cliente integer,
	nombre varchar(40),
	imagen_de_perfil varchar(40),
	usuario_twitter varchar(15),
	apellido varchar(40),
	fecha_inicio date default now(),
	domicilio varchar(40),
	correo varchar(30),
	nit varchar(15),
	pago_total float,


	oficina integer,
	contrato integer,
	estado integer,
	tipo_cliente integer,

	constraint cliente_pk primary key (id_cliente),


	constraint oficina_fk foreign key (oficina) references oficinas (id_oficina),
	constraint tipo_contrato_fk foreign key (contrato) references contratos (id_tipo_contrato),
	constraint estado_fk foreign key (estado) references estados (id_estado_cliente),
	constraint tipo_cliente_fk foreign key (tipo_cliente) references tipos_cliente (id_tipo_cliente)

);





CREATE TABLE valores_nuevos_campos(
	id_cliente integer,
	id_campo integer,
	valor varchar(50),
	constraint cliente_fk foreign key (id_cliente) references clientes (id_cliente),
	constraint campo_fk foreign key (id_campo) references nuevos_campos (id_campo)

);




INSERT INTO oficinas VALUES (1, 'Zona 10 Guatemala');
INSERT INTO oficinas VALUES (2, 'Zona 14 Guatemala' );
INSERT INTO oficinas VALUES (3, 'Zona 16 Guatemala');


INSERT INTO contratos VALUES (1, 'Anual', 10000);
INSERT INTO contratos VALUES (2, 'Mensual', 1000);
INSERT INTO contratos VALUES (3, 'Permanente', 50000);

INSERT INTO estados VALUES (1, 'Activo');
INSERT INTO estados VALUES (2, 'Inactivo');
INSERT INTO estados VALUES (3, 'Terminado');

INSERT INTO tipos_cliente VALUES (1, 'Regular' , 0);
INSERT INTO tipos_cliente VALUES (2, 'Familiar' , 0.15);
INSERT INTO tipos_cliente VALUES (3, 'Asociado' , 0.3);


CREATE INDEX b_apellido ON clientes (apellido);
CREATE INDEX b_contrato ON clientes (contrato);
CREATE INDEX b_tipo_cliente ON clientes (tipo_cliente);
CREATE INDEX b_estado ON clientes (estado);
CREATE INDEX b_oficinas ON clientes (oficina);



-- Trigger 1. Cuando se inserta un cliente, se calcula su pago.
CREATE OR REPLACE FUNCTION insert_cliente_pago ()
RETURNS TRIGGER AS $trigger_insert_cliente_pago$ 
BEGIN
	NEW.pago_total = (
	(SELECT costo FROM contratos WHERE id_tipo_contrato = NEW.contrato) 
	-  
	(SELECT costo FROM contratos WHERE id_tipo_contrato = NEW.contrato)
	*
	(SELECT descuento FROM tipos_cliente WHERE id_tipo_cliente = NEW.tipo_cliente)
	);

	RETURN NEW;
END;
$trigger_insert_cliente_pago$ LANGUAGE 'plpgsql';


CREATE TRIGGER trigger_insert_cliente_pago
BEFORE INSERT ON clientes
FOR EACH ROW
EXECUTE PROCEDURE insert_cliente_pago ();



-- Trigger 2. Cuando se actualiza la informacion de un cliente, se vuelve a calcular su pago.
CREATE OR REPLACE FUNCTION update_cliente_pago ()
RETURNS TRIGGER AS $trigger_update_cliente_pago$ 
BEGIN
	NEW.pago_total = (
	(SELECT costo FROM contratos WHERE id_tipo_contrato = NEW.contrato) 
	-  
	(SELECT costo FROM contratos WHERE id_tipo_contrato = NEW.contrato)
	*
	(SELECT descuento FROM tipos_cliente WHERE id_tipo_cliente = NEW.tipo_cliente)
	);

	RETURN NEW;
END;
$trigger_update_cliente_pago$ LANGUAGE 'plpgsql';


CREATE TRIGGER trigger_update_cliente_pago
BEFORE UPDATE ON clientes
FOR EACH ROW
EXECUTE PROCEDURE update_cliente_pago ();


-- Trigger 3. Cuando se borra un cliente, se borran todas las referencias de ese cliente en la tabla de valores de nuevos campos

CREATE OR REPLACE FUNCTION borrar_cliente_valores_nuevo_campo ()
RETURNS TRIGGER AS $trigger_borrar_cliente_valores_nuevo_campo$ 
BEGIN
	
	DELETE FROM valores_nuevos_campos WHERE valores_nuevos_campos.id_cliente = OLD.id_cliente;
	


	RETURN OLD;
END;
$trigger_borrar_cliente_valores_nuevo_campo$ LANGUAGE 'plpgsql';


CREATE TRIGGER trigger_borrar_cliente_valores_nuevo_campo
BEFORE DELETE ON clientes
FOR EACH ROW
EXECUTE PROCEDURE borrar_cliente_valores_nuevo_campo ();






-- Trigger 4. Cuando se agrega un nuevo campo, se crea una referencia a ese campo para cada usuario.

CREATE OR REPLACE FUNCTION valores_default_nuevo_campo ()
RETURNS TRIGGER AS $trigger_valores_default_nuevo_campo$ 
BEGIN
	
	INSERT INTO valores_nuevos_campos 
	(SELECT id_cliente, NEW.id_campo FROM clientes);
	


	RETURN NEW;
END;
$trigger_valores_default_nuevo_campo$ LANGUAGE 'plpgsql';


CREATE TRIGGER trigger_valores_default_nuevo_campo
AFTER INSERT ON nuevos_campos
FOR EACH ROW
EXECUTE PROCEDURE valores_default_nuevo_campo ();



-- Trigger 5. Cuando se borra un nuevo campo, se borran todos los valores que tenian los usuarios de ese campo

CREATE OR REPLACE FUNCTION borrar_valores_nuevo_campo ()
RETURNS TRIGGER AS $trigger_borrar_valores_nuevo_campo$ 
BEGIN
	
	DELETE FROM valores_nuevos_campos WHERE valores_nuevos_campos.id_campo = OLD.id_campo;
	


	RETURN OLD;
END;
$trigger_borrar_valores_nuevo_campo$ LANGUAGE 'plpgsql';


CREATE TRIGGER trigger_borrar_valores_nuevo_campo
BEFORE DELETE ON nuevos_campos
FOR EACH ROW
EXECUTE PROCEDURE borrar_valores_nuevo_campo ();


CREATE VIEW cant_oficina_1 AS
    SELECT count('oficina')
    FROM clientes
    WHERE oficina = 1;

CREATE VIEW cant_oficina_2 AS
    SELECT count('oficina')
    FROM clientes
    WHERE oficina = 2;

CREATE VIEW cant_oficina_3 AS
    SELECT count('oficina')
    FROM clientes
    WHERE oficina = 3;

CREATE VIEW cant_contrato_1 AS
    SELECT count('contrato')
    FROM clientes
    WHERE contrato = 1;

CREATE VIEW cant_contrato_2 AS
    SELECT count('contrato')
    FROM clientes
    WHERE contrato = 2;

CREATE VIEW cant_contrato_3 AS
    SELECT count('contrato')
    FROM clientes
    WHERE contrato = 3;

CREATE VIEW cant_estado_1 AS
    SELECT count('estado')
    FROM clientes
    WHERE estado = 1;

CREATE VIEW cant_estado_2 AS
    SELECT count('estado')
    FROM clientes
    WHERE estado = 2;

CREATE VIEW cant_estado_3 AS
    SELECT count('estado')
    FROM clientes
    WHERE estado = 3;

CREATE VIEW cant_tipo_cliente_1 AS
    SELECT count('tipo_cliente')
    FROM clientes
    WHERE tipo_cliente = 1;

CREATE VIEW cant_tipo_cliente_2 AS
    SELECT count('tipo_cliente')
    FROM clientes
    WHERE tipo_cliente = 3;

CREATE VIEW cant_tipo_cliente_3 AS
    SELECT count('oficina')
    FROM clientes
    WHERE tipo_cliente = 3;

CREATE VIEW cant_mes as
SELECT date_trunc('month', fecha_inicio) as mes, count(*)
FROM clientes
GROUP BY mes;

CREATE VIEW cant_ano as
SELECT date_trunc('year', fecha_inicio) as año, count(*)
FROM clientes
GROUP BY año;
