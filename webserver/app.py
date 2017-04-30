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
		fillableFields = [{'fieldName': "field1", 'fieldType': "text"}, {'fieldName': "field2", 'fieldType': "date"}, {'fieldName': "field3", 'fieldType': "text"}]
		return render_template('newCustomer.html', fillableFields=fillableFields)


	elif request.method == 'POST':
		#Get values from form
		firstName = request.form['firstName']
		lastName = request.form['lastName']
		twitterUsername = request.form['twitterUsername']
		startDate = request.form['startDate']
		address = request.form['address']
		email = request.form['email']
		nit = request.form['nit']
		office = request.form['office']
		contract = request.form['contract']
		state = request.form['state']
		clientType = request.form['clientType']

		#Store to DB - Casting may be necessary, as all the data comes in unicode - TODO
		# print(
		# 	str(firstName) + " --TYPE: " + str(type(firstName)) + "\n" +
		# 	str(lastName) + " --TYPE: " + str(type(lastName)) + "\n" +
		# 	str(twitterUsername) + " --TYPE: " + str(type(twitterUsername)) + "\n" +
		# 	str(startDate) + " --TYPE: " + str(type(startDate)) + "\n" +
		# 	str(address) + " --TYPE: " + str(type(address)) + "\n" +
		# 	str(email) + " --TYPE: " + str(type(email)) + "\n" +
		# 	str(nit) + " --TYPE: " + str(type(nit)) + "\n" +
		# 	str(office) + " --TYPE: " + str(type(office)) + "\n" +
		# 	str(contract) + " --TYPE: " + str(type(contract)) + "\n" +
		# 	str(state) + " --TYPE: " + str(type(state)) + "\n" +
		# 	str(clientType) + " --TYPE: " + str(type(clientType)) + "\n"
		# )

		# Return success of fail feedback, and redirect user to a convenient view - TODO

@app.route('/searchCustomer', methods=['GET', 'POST'])
def searchCustomer():
	if request.method == 'GET':
		# filterableFields should be filled with the fields of the customers table in the DB, 
		# note that each field requires a fieldName and a fieldType, to provide a form accordingly to the types. Here's an example:
		filterableFields = [{'fieldName': "field1", 'fieldType': "text"}, {'fieldName': "field2", 'fieldType': "date"}, {'fieldName': "field3", 'fieldType': "text"}]
		return render_template('searchCustomer.html', filterableFields=filterableFields)


	elif request.method == 'POST':
		# Processing the filter
		for field in request.form:
			#For each field in the form
			if (field != 'submit') and ("_comparisonType" not in field):
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
				fieldComparisonType = request.form[field+"_comparisonType"]

				# print(fieldName + " has to be filtered with value: " + fieldValue + " applying comparison " + fieldComparisonType)




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=80)