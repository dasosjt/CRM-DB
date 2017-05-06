
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
