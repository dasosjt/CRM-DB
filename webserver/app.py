import os
import twitterModule
#from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+'/images/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

from flask import Flask, render_template, request, Markup, session, redirect, g, url_for, send_from_directory
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import funciones
import sys
import psycopg2
conn_string = "host='localhost' dbname='proyecto2' user='postgres' password='Gentoo12'"
conn = psycopg2.connect(conn_string)
camposComparar = []

@app.route('/')
def homePage():
	return redirect('/reports')

@app.route('/newCustomer', methods=['GET','POST'])
def newCustomer():
	if request.method == 'GET':
		# fillableFields should be filled with the fields of the customers table in the DB,
		# note that each field requires a fieldName and a fieldType, to provide a form accordingly to the types. Here's an example:
		#fillableFields = [{'fieldName': "oficina", 'fieldType': "text"}, {'fieldName': "field1", 'fieldType': "text"}, {'fieldName': "contrato", 'fieldType': "text"}, {'fieldName': "field3", 'fieldType': "date"}]
		fillableFields = [{'fieldName': "Nombre", 'fieldType': "text"}]
		fillableFields.append({'fieldName': "Apellido", 'fieldType': "text"})
		fillableFields.append({'fieldName': "Fecha Inicio", 'fieldType': "date"})
		fillableFields.append({'fieldName': "Domicilio", 'fieldType': "text"})
		fillableFields.append({'fieldName': "Correo", 'fieldType': "text"})
		fillableFields.append({'fieldName': "NIT", 'fieldType': "text"})

		fillableFields.append({'fieldName': "oficina", 'fieldType': "text"})
		fillableFields.append({'fieldName': "contrato", 'fieldType': "text"})
		fillableFields.append({'fieldName': "estado", 'fieldType': "text"})
		fillableFields.append({'fieldName': "tipo_cliente", 'fieldType': "text"})
		fillableFields.append({'fieldName': "Usuario Twitter", 'fieldType': "text"})
		fillableFields.append({'fieldName': "Imagen de Perfil", 'fieldType': "file"})

		cursor = conn.cursor()
		cursor.execute("Select * FROM nuevos_campos")
		records = cursor.fetchall()
		for campo in records:
			if(campo[2] == "texto"):
				fillableFields.append({'fieldName': campo[1], 'fieldType': "text"})
			elif(campo[2] == "entero"):
				fillableFields.append({'fieldName': campo[1], 'fieldType': "number"})
			elif(campo[2] == "decimal"):
				fillableFields.append({'fieldName': campo[1], 'fieldType': "number"})
			elif(campo[2] == "fecha"):
				fillableFields.append({'fieldName': campo[1], 'fieldType': "date"})
		return render_template('newCustomer.html', fillableFields=fillableFields)


	elif request.method == 'POST':
		# Processing the insert
		valores = []
		campos = []
		for field in request.form:
			# For each field in the form
			#Follow the user on Twitter
			

			if (field != 'action'):
				#If the field isn't the submit button

				if str(field) == "Usuario Twitter":
					try:
						print("Trying to follow user @"+str(request.form[field]))
						twitterModule.followUsername(request.form[field])
						print('User followed succesfully')
					except:
						print("Tweepy error, user maybe already followed.")

				fieldName = field
				fieldValue = request.form[field]
				campos.append(field.lower().replace(" ","_"))
				valores.append(fieldValue)

				print(fieldName + " has to be inserted with val: " + fieldValue)


				

				# Store to DB - Casting may be necessary, as all the data comes in unicode -R: The casting is done in postgres in the Insert

		image_info = request.files['Imagen de Perfil']
		# TODO When some client is deleted, notify server to delete the image name. Maybe a good trigger.
		image_info.save(UPLOAD_FOLDER+image_info.filename)

		campos.append("imagen_de_perfil")
		#print(image_info.filename)
		valores.append(image_info.filename)

		print funciones.InsertarCliente(conn, valores, campos)
		# Return success of fail feedback, and redirect user to a convenient view - TODO
		return redirect('/')

@app.route('/searchCustomer', methods=['GET', 'POST'])
def searchCustomer():
	if request.method == 'GET':
		# filterableFields should be filled with the fields of the customers table in the DB,
		# note that each field requires a fieldName and a fieldType, to provide a form accordingly to the types. Here's an example:


		filterableFields = [{'fieldName': "Nombre", 'fieldType': "text"}]
		filterableFields.append({'fieldName': "Apellido", 'fieldType': "text"})
		filterableFields.append({'fieldName': "Fecha inicio", 'fieldType': "date"})
		filterableFields.append({'fieldName': "Domicilio", 'fieldType': "text"})
		filterableFields.append({'fieldName': "Correo", 'fieldType': "text"})
		filterableFields.append({'fieldName': "NIT", 'fieldType': "text"})
		filterableFields.append({'fieldName': "Pago Total", 'fieldType': "number"})

		filterableFields.append({'fieldName': "oficina", 'fieldType': "text"})
		filterableFields.append({'fieldName': "contrato", 'fieldType': "text"})
		filterableFields.append({'fieldName': "estado", 'fieldType': "text"})
		filterableFields.append({'fieldName': "tipo_cliente", 'fieldType': "text"})




		cursor = conn.cursor()
		cursor.execute("Select * FROM nuevos_campos")
		records = cursor.fetchall()
		for campo in records:
			if(campo[2] == "texto"):
				filterableFields.append({'fieldName': campo[1], 'fieldType': "text"})
			elif(campo[2] == "entero"):
				filterableFields.append({'fieldName': campo[1], 'fieldType': "number"})
			elif(campo[2] == "decimal"):
				filterableFields.append({'fieldName': campo[1], 'fieldType': "number"})
			elif(campo[2] == "fecha"):
				filterableFields.append({'fieldName': campo[1], 'fieldType': "date"})


		return render_template('searchCustomer.html', filterableFields=filterableFields)


	elif request.method == 'POST':

		del camposComparar[:]

		# Processing the filter
		for field in request.form:
			#print(field)
			#For each field in the form
			if (field != 'action') and ("_comparisonType" not in field):
				#If the field isn't the submit button or a comparison type descriptor

				# Each field with its filter value should be arranged in a SQL query to get all the matching customers.
				# Comparison type 1 corresponds to ==
				# Comparison type 2 corresponds to !=
				# Comparison type 3 corresponds to <
				# Comparison type 4 corresponds to <=
				# Comparison type 5 corresponds to >
				# Comparison type 6 corresponds to >=

				campo = []

				fieldName = field
				campo.append(fieldName.lower().replace(" ","_"))

				fieldValue = request.form[field]
				campo.append(fieldValue)

				if (fieldName == 'oficina') or (fieldName == 'contrato') or (fieldName == 'estado') or (fieldName == 'tipo_cliente') or ():
					fieldComparisonType = '1'
				else:
					fieldComparisonType = request.form[field+"_comparisonType"]

				campo.append(fieldComparisonType)
				print(fieldName + " has to be filtered with value: " + fieldValue + " applying comparison " + fieldComparisonType)

			camposComparar.append(campo)


		#print camposComparar

		return redirect("/searchCustomerResults")



@app.route('/searchCustomerResults')
def searchCustomerResults():
        #Good because the columns are not dynamic
	campos = [{'fieldName': "Nombre", 'fieldType': "text"}]
	campos.append({'fieldName': "Apellido", 'fieldType': "text"})

	campos.append({'fieldName': "Fecha Inicio", 'fieldType': "date"})
	campos.append({'fieldName': "Domicilio", 'fieldType': "text"})
	campos.append({'fieldName': "Correo", 'fieldType': "text"})
	campos.append({'fieldName': "NIT", 'fieldType': "text"})
	campos.append({'fieldName': "Pago Total", 'fieldType': "text"})

	campos.append({'fieldName': "Oficina", 'fieldType': "text"})
	campos.append({'fieldName': "Contrato", 'fieldType': "text"})
	campos.append({'fieldName': "Estado", 'fieldType': "text"})
	campos.append({'fieldName': "Tipo Cliente", 'fieldType': "text"})

	data = funciones.listaClientes(conn, camposComparar)
	

	filas = []
	for dat in data:
		fila = []
                isID = 1
		for valor in dat:
                        # The last one is the id
                        if isID == len(dat):
                            
							nuevaData = funciones.dataNuevosCampos(conn, valor)
							for nuevoValor in nuevaData:
								if not(({'fieldName': nuevoValor[0], 'fieldType': "text"} ) in campos):
									campos.append({'fieldName': nuevoValor[0], 'fieldType': "text"})
								fila.append({'valor': nuevoValor[1]})
							
							fila.append({'id': valor})
							
                        else:
							fila.append({'valor': valor})
                        isID += 1
		
		
		
		filas.append(fila)
	num_resultados = len(filas)

	return render_template('searchCustomerResults.html' , campos = campos, filas = filas, num_resultados = num_resultados)

	
	
	
@app.route('/Fields')
def Fields():
        #Good because the columns are not dynamic
	campos = [{'fieldName': "Campo", 'fieldType': "text"}]
	campos.append({'fieldName': "Tipo", 'fieldType': "text"})

	

	data = funciones.listaCampos(conn)

	filas = []
	for dat in data:
		fila = []
		isID = 1
		for valor in dat:
			if isID == len(dat):
				fila.append({'id': valor})
			else:
				fila.append({'valor': valor})
			isID += 1
                    
                       
		filas.append(fila)


	return render_template('Fields.html' , campos = campos, filas = filas)
@app.route('/newField', methods=['GET', 'POST'])
def newField():
	if request.method == 'GET':
		return render_template('newField.html')
	elif request.method == 'POST':
		newFieldName = request.form['newFieldName']
		newFieldType = request.form['newFieldType']

		# Field type 1 corresponds to text
		# Field type 2 corresponds to integer
		# Field type 3 corresponds to float
		# Field type 4 corresponds to date
		print("Create field: "+newFieldName+" with type: "+newFieldType)
		#Create field
		print funciones.nuevoCampo(conn, newFieldName, newFieldType)
		return redirect('/newCustomer')



@app.route('/profile/<client_id>', methods=['GET', 'POST'])
def profile(client_id):
	if request.method == 'GET':
		#Relational data
		columns  = funciones.listaColumnas(conn, client_id)
		data = funciones.dataCliente(conn, client_id)
		print("Data is type"+str(type(data)))
		print("Columns is type"+str(type(columns)))
		image_name = funciones.clienteIDImagen(conn, client_id)
		image_path = "/images/"+image_name[0][0]

		#Tweets
		#Get username
		username = data[columns.index({'fieldName':'Usuario Twitter'})]['value']
		tweets = twitterModule.getTweets(username)

		return render_template('profile.html', client_id = client_id, columns = columns, line = data, image_path = image_path, username=username, tweets=tweets)

	elif request.method == 'POST':
		#Relational data
		columns  = funciones.listaColumnas(conn, client_id)
		data = funciones.dataCliente(conn, client_id)
		print("Data is type"+str(type(data)))
		print("Columns is type"+str(type(columns)))
		image_name = funciones.clienteIDImagen(conn, client_id)
		image_path = "/images/"+image_name[0][0]

		#Tweets
		#Get username
		username = data[columns.index({'fieldName':'Usuario Twitter'})]['value']

		#Get filter parameters
		containingWord = request.form['containingWord']
		afterDate = request.form['afterDate']
		beforeDate = request.form['beforeDate']

		tweets = twitterModule.getTweets(username, containingWord=containingWord, afterDate=afterDate, beforeDate=beforeDate)

		return render_template('profile.html', client_id = client_id, columns = columns, line = data, image_path = image_path, username=username, tweets=tweets)


@app.route('/edit/<client_id>', methods=['GET', 'POST'])
def edit(client_id):
    if request.method == 'GET':
        fillableFields = [{'fieldName': "Nombre", 'fieldType': "text", 'fieldValue': funciones.getInfo(conn, "nombre", client_id)}]
        fillableFields.append({'fieldName': "Apellido", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "apellido", client_id)})
        fillableFields.append({'fieldName': "Fecha Inicio", 'fieldType': "date", 'fieldValue' : funciones.getInfo(conn, "fecha_inicio", client_id)})
        fillableFields.append({'fieldName': "Domicilio", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "domicilio", client_id)})
        fillableFields.append({'fieldName': "Correo", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "correo", client_id)})
        fillableFields.append({'fieldName': "NIT", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "nit", client_id)})

        fillableFields.append({'fieldName': "oficina", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "oficina", client_id)})
        fillableFields.append({'fieldName': "contrato", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "contrato", client_id)})
        fillableFields.append({'fieldName': "estado", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "estado", client_id)})
        fillableFields.append({'fieldName': "tipo_cliente", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "tipo_cliente", client_id)})
        fillableFields.append({'fieldName': "Usuario Twitter", 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, "usuario_twitter", client_id)})
        fillableFields.append({'fieldName': "Imagen de Perfil", 'fieldType': "file", 'fieldValue' : funciones.getInfo(conn, "imagen_de_perfil", client_id)})

        cursor = conn.cursor()
        cursor.execute("Select * FROM nuevos_campos")
        records = cursor.fetchall()
        for campo in records:
                if(campo[2] == "texto"):
                    fillableFields.append({'fieldName': campo[1], 'fieldType': "text", 'fieldValue' : funciones.getInfo(conn, str(campo[1]), client_id)})
                elif(campo[2] == "entero"):
                    fillableFields.append({'fieldName': campo[1], 'fieldType': "number", 'fieldValue' : funciones.getInfo(conn, str(campo[1]), client_id)})
                elif(campo[2] == "decimal"):
                    fillableFields.append({'fieldName': campo[1], 'fieldType': "number", 'fieldValue' : funciones.getInfo(conn, str(campo[1]), client_id)})
                elif(campo[2] == "fecha"):
                    fillableFields.append({'fieldName': campo[1], 'fieldType': "date", 'fieldValue' : funciones.getInfo(conn, str(campo[1]), client_id)})

        return render_template('editProfile.html', fillableFields=fillableFields, client_id = client_id)
    
    elif request.method == 'POST':		
        # Processing the insert
	valores = []
	campos = []
        for field in request.form:
                # For each field in the form
                if (field != 'action'):
                        #If the field isn't the submit button

                        fieldName = field
                        fieldValue = request.form[field]
                        campos.append(field.lower().replace(" ","_"))
                        valores.append(fieldValue)

                        print(fieldName + " has to be updated with val: " + fieldValue)

        image_info = request.files['Imagen de Perfil']
        # TODO When some client is deleted, notify server to delete the image name. Maybe a good trigger.
        image_info.save(UPLOAD_FOLDER+image_info.filename)

        campos.append("imagen_de_perfil")
        #print(image_info.filename)
        valores.append(image_info.filename)

        # Store to DB - Casting may be necessary, as all the data comes in unicode -R: The casting is done in postgres in the Insert
        funciones.updateCliente(conn, client_id, valores, campos)
        # Return success of fail feedback, and redirect user to a convenient view - TODO
        return redirect('/')

@app.route('/delete/<client_id>', methods=['POST'])
def delete(client_id):
    funciones.eliminarCliente(conn, client_id)

    return render_template('deleteProfile.html')
	
	
@app.route('/deleteCampo/<campo_id>', methods=['POST'])
def deleteCampo(campo_id):
    funciones.eliminarCampo(conn, campo_id)

    return render_template('Fields.html')

@app.route('/images/<image_name>', methods=['GET'])
def image(image_name):
    return send_from_directory('images', image_name)

@app.route('/reports', methods=['GET'])
def reports():
    label_oficina, y_oficina = funciones.reporteCatalogo(conn, "oficina")
    label_contrato, y_contrato = funciones.reporteCatalogo(conn, "contrato")
    label_estado, y_estado = funciones.reporteCatalogo(conn, "estado")
    label_tipo, y_tipo = funciones.reporteCatalogo(conn, "tipo_cliente")
    info_ano = funciones.reporteTiempo(conn, "ano")
    info_mes = funciones.reporteTiempo(conn, "mes")


    data = []
    data.append({"label_oficina": label_oficina, "y_oficina": y_oficina})
    data.append({"label_contrato": label_contrato, "y_contrato": y_contrato})
    data.append({"label_estado": label_estado, "y_estado": y_estado})
    data.append({"label_tipo": label_tipo, "y_tipo": y_tipo})

    return render_template('reports.html', data = data, info_ano = info_ano, info_mes = info_mes )

@app.route('/twitterStats/<username>', methods=['GET'])
def twitterStats(username):
	dayStats, hourStats = twitterModule.getStats(username)
	print(dayStats)
	print(hourStats)
	# return "This is the page for twitter stats for "+username
	return render_template('twitterStats.html', dayStats=dayStats, hourStats=hourStats, username=username)


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
