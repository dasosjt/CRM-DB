def InsertarCliente(conn, valores, campos):
	cursor = conn.cursor()
	camposFijos = []
	camposFijos.append("id_cliente")
	camposFijos.append("nombre")
	camposFijos.append("apellido")
	camposFijos.append("fecha_inicio")
	camposFijos.append("domicilio")
	camposFijos.append("correo")
	camposFijos.append("pago_total")
	camposFijos.append("nit")
	camposFijos.append("contrato")
	camposFijos.append("oficina")
	camposFijos.append("estado")
	camposFijos.append("tipo_cliente")
	camposFijos.append("usuario_twitter")
	
	cursor.execute("Select * FROM clientes")

	records = cursor.fetchall()
	if(len(records) == 0):
		id_cliente = 1
	else:
		id_cliente = records[len(records)-1][0]+1
	query = "INSERT INTO clientes ( id_cliente , "
	
        contador_campos = 0
	for campo in campos:
		if(campo in camposFijos):
			query+= ""+str(campo) + ""
			if(campo != campos[len(campos)-1]):
				query += " , "

			
                contador_campos += 1
		query += str(campo)
		if(contador_campos != len(campos)):
		    query += " , "
>>>>>>> 3290067508fdb23619a017211ce9bce2d7ce9b22
	
	query += ")"
	query += " VALUES ('"+str(id_cliente) +"' , "
	contador = 0
	queryNuevosCampos = ""
	for valor in valores:
		contador += 1
		if(campos[contador-1] in camposFijos):
			query+= "'"+str(valor) + "'"
			query += " , "
		else:
			queryNuevosCampos += "INSERT INTO valores_nuevos_campos VALUES ( "+ str(id_cliente) +" , "
			queryNuevosCampos += "(SELECT nuevos_campos.id_campo FROM nuevos_campos WHERE LOWER(campo) = '"+ campos[contador-1]+"') , "
			queryNuevosCampos += " '" +valor+"' );   "

		
	query = query[:-2]
	query += ");"
	cursor.execute(query)
	cursor.execute(queryNuevosCampos)
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
