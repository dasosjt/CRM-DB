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
	for valor in valores:
		query+= "'"+str(valor) + "'"
		if(valor != valores[len(valores)-1]):
			query += " , "
	query += ");"
	print query
	cursor.execute(query)
	conn.commit()

	return id_cliente