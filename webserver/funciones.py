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

        contador_valores = 0
	for valor in valores:
                contador_valores += 1
		query += "'"+str(valor) + "'"
		if(contador_valores != len(valores)):
		    query += " , "
	query += ");"
	print query
	cursor.execute(query)
	conn.commit()

	return id_cliente
