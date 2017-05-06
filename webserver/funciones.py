def eliminarCliente(conn, client_id):
    cursor = conn.cursor()
    
    query = "DELETE FROM clientes "
    query += "WHERE clientes.id_cliente = "+client_id
    query += ";"

    cursor.execute(query)
    conn.commit()

def InsertarCliente(conn, valores, campos):
	cursor = conn.cursor()
 

	cursor.execute("Select * FROM clientes")

	records = cursor.fetchall()
	if(len(records) == 0):
		id_cliente = 1
	else:
		id_cliente = records[len(records)-1][0]+1
	query = "INSERT INTO clientes ( id_cliente , "
	
        contador_campos = 0
	for campo in campos:
                contador_campos += 1
		query += str(campo)
		if(contador_campos != len(campos)):
		    query += " , "
	
	query += ")"
	query += " VALUES ('"+str(id_cliente) +"' , "
	contador = 0
	for valor in valores:
		contador += 1
		query+= "'"+str(valor) + "'"
		if(contador != len(valores)):
			query += " , "
	query += ");"
	cursor.execute(query)
	conn.commit()

	return id_cliente

	
def listaClientes (conn):
	cursor = conn.cursor()
	query  = "SELECT nombre, apellido, fecha_inicio, nit, pago_total, direccion, contratos.tipo, estados.estado, tipos_cliente.tipo, id_cliente "
	query += "FROM clientes, oficinas, estados, contratos, tipos_cliente "
	query += "WHERE contrato = id_tipo_contrato "
	query += "AND oficina = id_oficina "
	query += "AND clientes.estado = id_estado_cliente "
	query += "AND clientes.tipo_cliente = tipos_cliente.id_tipo_cliente;"
	cursor.execute(query)

	records = cursor.fetchall()
        conn.commit()
	return records

def clienteID(conn, id):
    cursor = conn.cursor()
    query = "SELECT nombre, apellido, usuario_twitter, fecha_inicio, domicilio, correo, nit, pago_total, oficina, contrato, estado, tipo_cliente "
    query += "FROM clientes "
    query += "WHERE clientes.id_cliente = "+id+";"
    
    cursor.execute(query)
    records = cursor.fetchall()
    conn.commit()

    return records

def clienteIDImagen(conn, id):
    cursor = conn.cursor()
    query = "SELECT imagen_de_perfil "
    query += "FROM clientes "
    query += "WHERE clientes.id_cliente = "+id+";"
    
    cursor.execute(query)
    records = cursor.fetchall()
    conn.commit()

    return records
	
	
def nuevoCampo(conn, campo, tipo):
	cursor = conn.cursor()
	
	type = ""
	if(tipo == "1"):
		type = "texto"
	elif(tipo == "2"):
		type = "entero"
	elif(tipo == "3"):
		type = "decimal"
	elif(tipo == "4"):
		type = "fecha"
		
		
	cursor.execute("Select * FROM nuevos_campos;")

	records = cursor.fetchall()
	if(len(records) == 0):
		id_campo = 1
	else:
		id_campo = records[len(records)-1][0]+1
		
	
	query = "INSERT INTO nuevos_campos VALUES ("+str(id_campo)+" , '"+ campo+"' , '"+ type +"');"
	cursor.execute(query)
	conn.commit()
	return 0
