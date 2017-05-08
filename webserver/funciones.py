def eliminarCliente(conn, client_id):
    cursor = conn.cursor()

    query = "DELETE FROM clientes "
    query += "WHERE clientes.id_cliente = "+client_id
    query += ";"

    cursor.execute(query)
    conn.commit()

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


def renombrarColumns(columna):
    if columna != 'nit':
        return columna.replace("_", " ").title()
    else:
        return "NIT"



def listaColumnas(conn, id):
        cursor = conn.cursor()
        query = "SELECT column_name FROM information_schema.columns WHERE table_name='clientes';"
        cursor.execute(query)
        primaryColumns = cursor.fetchall()
        conn.commit()

        cursor = conn.cursor()
        query = "SELECT id_campo FROM clientes, valores_nuevos_campos WHERE clientes.id_cliente = valores_nuevos_campos.id_cliente"
        cursor.execute(query)
        secondaryColumns = cursor.fetchall()
        conn.commit()

        columns = []

        for data in primaryColumns:
            for dat in data:
                if dat != 'id_cliente' and dat != 'imagen_de_perfil':
	            columns.append({'fieldName': renombrarColumns(dat)})
        for data in secondaryColumns:
            for dat in data:
                columns.append({'fieldName': renombarColumns(dat)})

        return columns

def dataCliente(conn, id):
    cursor = conn.cursor()
    query = "SELECT nombre, usuario_twitter, apellido, fecha_inicio, domicilio, correo, nit, pago_total, oficinas.direccion, contratos.tipo, estados.estado, tipos_cliente.tipo "
    query += "FROM clientes, oficinas, estados, contratos, tipos_cliente "
    query += "WHERE clientes.id_cliente = "+id+" "
    query += "AND clientes.contrato = contratos.id_tipo_contrato "
    query += "AND clientes.oficina = oficinas.id_oficina "
    query += "AND clientes.estado = estados.id_estado_cliente "
    query += "AND clientes.tipo_cliente = tipos_cliente.id_tipo_cliente;"

    cursor.execute(query)
    primaryData = cursor.fetchall()
    conn.commit()

    cursor = conn.cursor()
    query = "SELECT nuevos_campos.campo FROM clientes, valores_nuevos_campos, nuevos_campos "
    query += "WHERE clientes.id_cliente = " + id + " "
    query += "AND clientes.id_cliente = valores_nuevos_campos.id_cliente "
    query += "AND valores_nuevos_campos.id_campo = nuevos_campos.id_campo;"
    cursor.execute(query)
    secondaryData = cursor.fetchall()
    conn.commit()

    dataA = []

    for data in primaryData:
        for dat in data:
            dataA.append({'value': dat})
    for data in secondaryData:
        for dat in data:
            dataA.append({'value': dat})

    return dataA

def clienteIDImagen(conn, id):
    cursor = conn.cursor()
    query = "SELECT imagen_de_perfil "
    query += "FROM clientes "
    query += "WHERE clientes.id_cliente = "+id+";"

    cursor.execute(query)
    records = cursor.fetchall()
    conn.commit()

    return records



def listaClientes (conn, comparaciones):
    cursor = conn.cursor()
    query  = "SELECT nombre, apellido, fecha_inicio, nit, pago_total, direccion, contratos.tipo, estados.estado, tipos_cliente.tipo "
    query += "FROM clientes, oficinas, estados, contratos, tipos_cliente "
    query += "WHERE contrato = id_tipo_contrato "
    query += "AND oficina = id_oficina "
    query += "AND clientes.estado = id_estado_cliente "
    query += "AND clientes.tipo_cliente = tipos_cliente.id_tipo_cliente"

    for comp in comparaciones:
        if((comp[0] == 'oficina') or (comp[0] == 'contrato') or (comp[0] == 'estado') or (comp[0] == 'tipo_cliente')):
            if(comp[1] == '0'):
                no = 0
            else:
                query += " AND clientes."+comp[0] + " = "+comp[1]
        else:
            if (comp[1] == ''):
                no = 0
            else:
				# Comparison type 1 corresponds to ==
				# Comparison type 2 corresponds to !=
				# Comparison type 3 corresponds to <
				# Comparison type 4 corresponds to <=
				# Comparison type 5 corresponds to >
				# Comparison type 6 corresponds to >=

                signo = ""
                if(comp[2] == '1'):
                    signo = "="
                elif(comp[2] == '2'):
                    signo = "!="
                elif(comp[2] == '3'):
                    signo = "<"
                elif(comp[2] == '4'):
                    signo = "<="
                elif(comp[2] == '5'):
                    signo = ">"
                elif(comp[2] == '6'):
                    signo = ">="
                elif(comp[2] == '7'):
                    signo = " LIKE "

                if(signo == " LIKE "):
                    query += " AND clientes."+comp[0] + signo +" '%"+ comp[1]+"%' "
                else:
                    query += " AND clientes."+comp[0] + signo + comp[1]

    query +=";"
    print query
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
