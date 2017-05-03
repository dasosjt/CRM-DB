def InsertarCliente(conn, valores, campos):
	cursor = conn.cursor()
 

	cursor.execute("Select * FROM clientes")

	records = cursor.fetchall()
	if(len(records) == 0):
		id_cliente = 1
	else:
		id_cliente = records[len(records)-1][0]+1
	query = "INSERT INTO clientes ( id_cliente , "
	
	for campo in campos:
		query+= ""+str(campo) + ""
		if(campo != campos[len(campos)-1]):
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
	query  = "SELECT nombre, apellido, fecha_inicio, nit, pago_total, direccion, contratos.tipo, estados.estado, tipos_cliente.tipo "
	query += "FROM clientes, oficinas, estados, contratos, tipos_cliente "
	query += "WHERE contrato = id_tipo_contrato "
	query += "AND oficina = id_oficina "
	query += "AND clientes.estado = id_estado_cliente "
	query += "AND clientes.tipo_cliente = tipos_cliente.id_tipo_cliente;"
	cursor.execute(query)

	records = cursor.fetchall()
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