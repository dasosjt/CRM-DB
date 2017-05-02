from flask import Flask, render_template, request, Markup, session, redirect, g, url_for
app = Flask(__name__)

@app.route('/')
def homePage():
	return render_template('base.html')

@app.route('/newCustomer', methods=['GET','POST'])
def newCustomer():
	if request.method == 'GET':
		# fillableFields should be filled with the fields of the customers table in the DB, 
		# note that each field requires a fieldName and a fieldType, to provide a form accordingly to the types. Here's an example:
		fillableFields = [{'fieldName': "oficina", 'fieldType': "text"}, {'fieldName': "field1", 'fieldType': "text"}, {'fieldName': "contrato", 'fieldType': "text"}, {'fieldName': "field3", 'fieldType': "date"}]
		return render_template('newCustomer.html', fillableFields=fillableFields)


	elif request.method == 'POST':
		# Processing the insert
		for field in request.form:
			# For each field in the form
			if (field != 'action'):
				#If the field isn't the submit button

				fieldName = field
				fieldValue = request.form[field]

				print(fieldName + " has to be inserted with value: " + fieldValue)

		# Store to DB - Casting may be necessary, as all the data comes in unicode - TODO
		# Return success of fail feedback, and redirect user to a convenient view - TODO

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
	return render_template('searchCustomerResults.html')

@app.route('/newField')
def newField():
	return render_template('newField.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=80)