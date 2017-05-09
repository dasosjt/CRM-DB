def reporte(conn, columna):
    cursor = conn.cursor()

    y = []
    if columna == "oficina":
        label = ['Zona 10 Guatemala', 'Zona 14 Guatemala', 'Zona 16 Guatemala']
    elif columna == "contrato":
        label = ['Anual', 'Mensual', 'Permanente']
    elif columna == "estado":
        label = ['Activo', 'Inactivo', 'Terminado']
    else:
        label = ['Regular', 'Familiar', 'Asociado']

    for i in range(1, 3):
        query = "SELECT count("+columna+") FROM clientes WHERE "+columna+" = "+str(i)+";"
        cursor.execute(query)
        temp = cursor.fetchall()
        print(temp)
        y.append(temp)



    conn.commit()

    return label, y


def eliminarCliente(conn, client_id):
    cursor = conn.cursor()

    query = "DELETE FROM clientes "
    query += "WHERE clientes.id_cliente = "+client_id
    query += ";"

    cursor.execute(query)
    conn.commit()

def eliminarCampo(conn, campo_id):
    cursor = conn.cursor()

    query = "DELETE FROM nuevos_campos "
    query += "WHERE id_campo = "+campo_id
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
<<<<<<< HEAD
	camposFijos.append("imagen_de_perfil")
=======
        camposFijos.append("imagen_de_perfil")
>>>>>>> 48dcc1c0e4631256755feb55a0457c88c625cb3e

	cursor.execute("SELECT * FROM clientes ORDER BY id_cliente;")
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
			query += " , "
			

	query = query[:-2]
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
        if(queryNuevosCampos != ""):
        	cursor.execute(queryNuevosCampos)
	conn.commit()

	return id_cliente

def updateCliente(conn, client_id, valores, campos):

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
    camposFijos.append("imagen_de_perfil")
    
    cursor = conn.cursor()
    query = "UPDATE clientes SET "

    c = 0

    for campo in campos:
        if(campo in camposFijos):
            query += campo + " = '" + valores[c] + "', " 
        else:
            id_query = "SELECT id_campo FROM nuevos_campos WHERE campo = '"+campo+"';"
            cursor.execute(id_query)
            id_campo = cursor.fetchall()
            update_query = "UPDATE valores_nuevos_campos SET valor  = '" + str(valores[c]) + "' "
            update_query += "WHERE id_cliente = "+str(client_id)+" AND id_campo = "+str(id_campo[0][0])+";"
            cursor.execute(update_query)
        c += 1

    query = query[:-2]
    query += " WHERE clientes.id_cliente = "+client_id+";"

    cursor.execute(query)

    conn.commit()



def renombrarColumns(columna):
    if columna != 'nit':
        return columna.replace("_", " ").title()
    else:
        return "NIT"



def listaColumnas(conn, id):
            

        cursor = conn.cursor()
        query = "SELECT campo FROM nuevos_campos;"
        cursor.execute(query)
        secondaryColumns = cursor.fetchall()
        conn.commit()

        columns = []

<<<<<<< HEAD
        for data in primaryColumns:
            for dat in data:
                if dat != 'id_cliente' and dat != 'imagen_de_perfil':
	            columns.append({'fieldName': renombrarColumns(dat)})
       # for data in secondaryColumns:
        #    for dat in data:
        #        columns.append({'fieldName': renombrarColumns(dat)})
=======
        columns.append({'fieldName': 'Nombre'})
        columns.append({'fieldName': 'Usuario Twitter'})
        columns.append({'fieldName': 'Apellido'})
        columns.append({'fieldName': 'Fecha Inicio'})
        columns.append({'fieldName': 'Domicilio'})
        columns.append({'fieldName': 'Correo'})
        columns.append({'fieldName': 'NIT'})
        columns.append({'fieldName': 'Pago total'})
        columns.append({'fieldName': 'Oficina'})
        columns.append({'fieldName': 'Contrato'})
        columns.append({'fieldName': 'Estado'})
        columns.append({'fieldName': 'Tipo cliente'})

        print(secondaryColumns)

        if(len(secondaryColumns) > 0): 
            for data in secondaryColumns:
                for dat in data:
                    if(dat):
                        columns.append({'fieldName': renombrarColumns(dat)})
>>>>>>> 48dcc1c0e4631256755feb55a0457c88c625cb3e

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

    cursor = conn.cursor()
    query = "SELECT valor FROM clientes, valores_nuevos_campos "
    query += "WHERE clientes.id_cliente = " + id + " "
    query += "AND clientes.id_cliente = valores_nuevos_campos.id_cliente ;"
    cursor.execute(query)
    secondaryData = cursor.fetchall()
    conn.commit()

    #print(secondaryData)

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
	
	
	query  = "SELECT DISTINCT nombre, apellido, fecha_inicio, domicilio, correo, nit, pago_total, direccion, contratos.tipo, estados.estado, tipos_cliente.tipo, clientes.id_cliente "
	query += " FROM clientes, oficinas, estados, contratos, tipos_cliente, nuevos_campos nc, valores_nuevos_campos nvc "
	query += " WHERE contrato = id_tipo_contrato "
	query += " AND oficina = id_oficina "
	query += " AND clientes.estado = id_estado_cliente "
	query += " AND clientes.tipo_cliente = tipos_cliente.id_tipo_cliente"
	query += " AND nvc.id_cliente = clientes.id_cliente"
	query += " AND nvc.id_campo = nc.id_campo"

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
				
				if(comp[0] in camposFijos):
					if(signo == " LIKE "):
						query += " AND clientes."+comp[0] + signo +" '%"+ comp[1]+"%' "
					else:
						query += " AND clientes."+comp[0] + signo + comp[1]
				else:
					if(signo == " LIKE "):
						query += " AND nc.campo = '"+comp[0]+"' AND nvc.valor " + signo +" '%"+ comp[1]+"%' "
					else:
						query += " AND LOWER(nc.campo) = '"+comp[0]+"' AND nvc.valor " + signo + "'"+comp[1]+"'"

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


	query = "INSERT INTO nuevos_campos VALUES ("+str(id_campo)+" , '"+ campo.replace(' ', '_').lower()+"' , '"+ type +"');"
	cursor.execute(query)
	conn.commit()
	return 0

	
	
def listaCampos (conn):
    cursor = conn.cursor()
    query  = "SELECT campo, tipo, id_campo FROM nuevos_campos"

    query +=";"
    cursor.execute(query)

    records = cursor.fetchall()
    return records
	

def dataNuevosCampos (conn, cliente):
    cursor = conn.cursor()
    query  = "SELECT campo, valor FROM nuevos_campos nc, valores_nuevos_campos vnc "
    query += " WHERE nc.id_campo = vnc.id_campo AND id_cliente = "+str(cliente)

    query +=";"
    cursor.execute(query)

    records = cursor.fetchall()
    return records
	
