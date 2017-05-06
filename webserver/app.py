import os
#from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+'/images/'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

from flask import Flask, render_template, request, Markup, session, redirect, g, url_for, send_from_directory
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import funciones
import sys
import psycopg2
conn_string = "host='localhost' dbname='proyecto2' user='postgres' password=''"
conn = psycopg2.connect(conn_string)

@app.route('/')
def homePage():
	return render_template('base.html')

@app.route('/newCustomer', methods=['GET','POST'])
def newCustomer():
	if request.method == 'GET':
		# fillableFields should be filled with the fields of the customers table in the DB, 
		# note that each field requires a fieldName and a fieldType, to provide a form accordingly to the types. Here's an example:
		#fillableFields = [{'fieldName': "oficina", 'fieldType': "text"}, {'fieldName': "field1", 'fieldType': "text"}, {'fieldName': "contrato", 'fieldType': "text"}, {'fieldName': "field3", 'fieldType': "date"}]
		fillableFields = [{'fieldName': "Nombre", 'fieldType': "text"}]
		fillableFields.append({'fieldName': "Apellido", 'fieldType': "text"})
		fillableFields.append({'fieldName': "Fecha inicio", 'fieldType': "date"})
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
			if (field != 'action'):
				#If the field isn't the submit button
                                
				fieldName = field
				fieldValue = request.form[field]
				campos.append(field.lower().replace(" ","_"))
				valores.append(fieldValue)
                                
				print(fieldName + " has to be inserted with val: " + fieldValue)
                
                image_info = request.files['Imagen de Perfil']
                # TODO When some client is deleted, notify server to delete the image name. Maybe a good trigger.
                image_info.save(UPLOAD_FOLDER+image_info.filename)

                campos.append("imagen_de_perfil")
                valores.append(image_info.filename)

                # Store to DB - Casting may be necessary, as all the data comes in unicode -R: The casting is done in postgres in the Insert
		print funciones.InsertarCliente(conn, valores, campos)
		# Return success of fail feedback, and redirect user to a convenient view - TODO
		return redirect('/')

@app.route('/searchCustomer', methods=['GET', 'POST'])
def searchCustomer():
	if request.method == 'GET':
		# filterableFields should be filled with the fields of the customers table in the DB, 
		# note that each field requires a fieldName and a fieldType, to provide a form accordingly to the types. Here's an example:
		filterableFields = [{'fieldName': "contrato", 'fieldType': "text"}, {'fieldName': "field2", 'fieldType': "date"}, {'fieldName': "field3", 'fieldType': "text"}]
		return render_template('searchCustomer.html', filterableFields=filterableFields)


	elif request.method == 'POST':
		# Processing the filter
		for field in request.form:
			print(field)
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

				fieldName = field
				fieldValue = request.form[field]
				if (fieldName == 'oficina') or (fieldName == 'contrato') or (fieldName == 'estado') or (fieldName == 'tipo_cliente'):
					fieldComparisonType = '1'
				else:
					fieldComparisonType = request.form[field+"_comparisonType"]

				print(fieldName + " has to be filtered with value: " + fieldValue + " applying comparison " + fieldComparisonType)

		return redirect("/searchCustomerResults")

		
		
@app.route('/searchCustomerResults')
def searchCustomerResults():
    
	campos = [{'fieldName': "Nombre", 'fieldType': "text"}]
	campos.append({'fieldName': "Apellido", 'fieldType': "text"})

	campos.append({'fieldName': "Fecha Inicio", 'fieldType': "date"})
	campos.append({'fieldName': "NIT", 'fieldType': "text"})
	campos.append({'fieldName': "Pago Total", 'fieldType': "text"})
		
	campos.append({'fieldName': "Oficina", 'fieldType': "text"})
	campos.append({'fieldName': "Contrato", 'fieldType': "text"})
	campos.append({'fieldName': "Estado", 'fieldType': "text"})
	campos.append({'fieldName': "Tipo Cliente", 'fieldType': "text"})

	
	data = funciones.listaClientes(conn)
	
	filas = []
	for dat in data:
		fila = []
                isID = 1
		for valor in dat:
                        # The last one is the id
                        if isID == len(dat):
                            fila.append({'id': valor})
                        else:
    			    fila.append({'valor': valor})
                        isID += 1
		filas.append(fila)
    

	return render_template('searchCustomerResults.html' , campos = campos, filas = filas)

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


		
@app.route('/profile/<client_id>', methods=['GET'])
def profile(client_id):
	
        campos = [{'fieldName': "Nombre", 'fieldType': "text"}]
	campos.append({'fieldName': "Apellido", 'fieldType': "text"})
        campos.append({'fieldName': "Usuario Twitter", 'fieldType': "text"})

	campos.append({'fieldName': "Fecha Inicio", 'fieldType': "text"})
	campos.append({'fieldName': "Domicilio", 'fieldType': "text"})
	campos.append({'fieldName': "Correo", 'fieldType': "text"})
	campos.append({'fieldName': "NIT", 'fieldType': "text"})
	campos.append({'fieldName': "Pago Total", 'fieldType': "text"})
		
	campos.append({'fieldName': "Oficina", 'fieldType': "text"})
	campos.append({'fieldName': "Contrato", 'fieldType': "text"})
	campos.append({'fieldName': "Estado", 'fieldType': "text"})
	campos.append({'fieldName': "Tipo Cliente", 'fieldType': "text"})
        

	data = funciones.clienteID(conn, client_id)
        
        image_name = funciones.clienteIDImagen(conn, client_id)
        image_path = "/images/"+image_name[0][0]
	
	for dat in data:
		fila = []
		for valor in dat:
                        fila.append({'valor': valor})

        
	return render_template('profile.html', campos = campos, fila = fila, image_path = image_path)

@app.route('/delete/<client_id>', methods=['POST'])
def delete(client_id):
    funciones.eliminarCliente(conn, client_id)
    
    return render_template('deleteProfile.html')

@app.route('/images/<image_name>', methods=['GET'])
def image(image_name):
    return send_from_directory('images', image_name)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
