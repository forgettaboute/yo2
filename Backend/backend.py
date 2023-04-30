import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from sql import createConnection
from sql import executeReadQuery
from sql import executeQuery
from credentials import Creds
import hashlib
import datetime


#Initial setup for Flask
app = Flask(__name__) #sets up the application... (somehow)
app.config['DEBUG'] = True

#Initializing MySQL/AWS database connection for APIs
myCreds = Creds()
connection = createConnection(myCreds.conString, myCreds.username, myCreds.password, myCreds.dbname)
auth = {'auth': False, 'authUser': myCreds.authUser, 'authPass': myCreds.authPass}

#home/login API route
@app.route('/api/login', methods=['GET'])
def login():
    username = request.headers['username'] #get the header parameters. request headers are interpreted as dictionaries, so value access is easy and direct
    pw = request.headers['password']

    if username == auth['authUser'] and pw == auth['authPass']:
        auth['auth'] = True
        return "Access Granted! You are cleared to proceed to APIs ^v^"
    else:
        return 'SECURITY ERROR: INVALID CREDENTIALS.'

#Create CAPTAIN
@app.route('/api/captain/add', methods=['POST']) 
def addCaptain():
    requestData = request.get_json()
    firstname = requestData['firstname']
    lastname = requestData['lastname']
    rank = requestData['rank']
    homeplanet = requestData['homeplanet']

    #query = "INSERT INTO cis3368.captain (firstname, lastname, rank, homeplanet) VALUES ('%s', '%s', '%s', '%s')" % (firstname, lastname, rank, homeplanet)
    return executeQuery(connection, "INSERT INTO cis3368.captain (firstname, lastname, `rank`, homeplanet) VALUES ('%s', '%s', '%s', '%s')" % (firstname, lastname, rank, homeplanet))

#Read captain
@app.route('/api/captain/all', methods=['GET'])
def allCaptains():
    captains = executeReadQuery(connection, "SELECT * FROM cis3368.captain")

    return jsonify(captains)


#Update captain
@app.route('/api/captain/update', methods=['PUT'])
def updCaptain():
    requestData = request.get_json()
    captainID = requestData['id']
    rank = requestData['rank']
    
    return executeQuery(connection, "UPDATE cis3368.captain SET `rank` = '%s' WHERE id = %s" % (rank, captainID))

#Delete captain
@app.route('/api/captain/delete', methods=['DELETE'])
def delCaptain():
    requestData = request.get_json()
    idToDelete = requestData['id']

    return executeQuery(connection, "DELETE FROM cis3368.captain WHERE id = %s" % idToDelete)


#Create SPACESHIP
@app.route('/api/spaceship/add', methods=['POST']) 
def addSpaceship():
    requestData = request.get_json()
    maxweight = requestData['maxweight']
    captainid = requestData['captainid']
    
    #VERIFYING NEW CAPTAINID IS VALID, WILL BE USED IN SPRINT 2, ALTHOUGH UNSURE IF THIS EXACT CODE IS NEEDED AS THE DB WILL REINFORCE DATABASE INTEGRITY WITH THE FOREIGN KEY
    try:
        captain = executeReadQuery(connection, "SELECT id FROM cis3368.captain WHERE id = %s" % (captainid))
    except:
        return "Captain with that ID does not exist"
    else:    
        return executeQuery(connection, "INSERT INTO cis3368.spaceship (maxweight, captainid) VALUES (%s, %s)" % (maxweight, captainid))

#Read spaceship
@app.route('/api/spaceship/all', methods=['GET'])
def allSpaceships():
    spaceships = executeReadQuery(connection, "SELECT * FROM cis3368.spaceship")

    return jsonify(spaceships)


#Update spaceship
@app.route('/api/spaceship/update', methods=['PUT'])
def updSpaceship():
    requestData = request.get_json()
    idToUpdate = requestData['id']
    captainid = requestData['captainid']

    try:
        captain = executeReadQuery(connection, "SELECT id FROM cis3368.captain WHERE id = %s" % (captainid))
    except:
        return "Captain with that ID does not exist"
    else:    
        return executeQuery(connection, "UPDATE cis3368.spaceship SET captainid = %s WHERE id = %s" % (captainid, idToUpdate))

#Delete spaceship
@app.route('/api/spaceship/delete', methods=['DELETE'])
def delSpaceship():
    requestData = request.get_json()
    idToDelete = requestData['id']

    return executeQuery(connection, "DELETE FROM cis3368.spaceship WHERE id = %s" % idToDelete)


#Create CARGO
@app.route('/api/cargo/add', methods=['POST']) 
def addCargo():
    requestData = request.get_json()
    cargoweight = requestData['weight']
    cargotype = requestData['cargotype']
    departure = requestData['departure']
    arrival = requestData['arrival']
    shipid = requestData['shipid']

    return executeQuery(connection, "INSERT INTO cis3368.cargo (weight, cargotype, departure, arrival, shipid) VALUES (%s, '%s', '%s', '%s', %s)" % (cargoweight, cargotype, departure, arrival, shipid))

#Read cargo
@app.route('/api/cargo/all', methods=['GET'])
def allCargo():
    cargo = executeReadQuery(connection, "SELECT * FROM cis3368.cargo")

    return jsonify(cargo)

#Update cargo
@app.route('/api/cargo/update', methods=['PUT'])
def updCargo():
    requestData = request.get_json()
    idToUpdate = requestData['id']
    departure = requestData['departure']
    arrival = requestData['arrival']
    shipid = requestData['shipid']

    try:
        spaceship = executeReadQuery(connection, "SELECT id FROM cis3368.ship WHERE id = %s" % (shipid))
    except:
        return "Cargo with that ID does not exist"
    else:    
        executeQuery(connection, "UPDATE cis3368.cargo SET departure = '%s' WHERE id = %s" % (departure, idToUpdate))
        executeQuery(connection, "UPDATE cis3368.cargo SET arrival = '%s' WHERE id = %s" % (arrival, idToUpdate))
        return executeQuery(connection, "UPDATE cis3368.cargo SET shipid = %s WHERE id = %s" % (shipid, idToUpdate))

#Delete cargo
@app.route('/api/cargo/delete', methods=['DELETE'])
def delCargo():
    requestData = request.get_json()
    idToDelete = requestData['id']

    return executeQuery(connection, "DELETE FROM cis3368.cargo WHERE id = %s" % idToDelete)

app.run()
