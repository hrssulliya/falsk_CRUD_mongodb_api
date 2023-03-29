from flask import Flask, request, make_response,Response, json, jsonify
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000)
    db = mongo.company
    mongo.server_info()
except:
    print("ERROR - Cannit connrct to db")

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     f_name = db.Column(db.String(50),  nullable=False)
#     l_name = db.Column(db.String(50),  nullable=False)
#     email = db.Column(db.String(150), nullable=False)
#     dob = db.Column(db.String(50), nullable=False)
#     gender = db.Column(db.String(10),  nullable=False)
#     education = db.Column(db.String(150), nullable=False)
#     company = db.Column(db.String(150), nullable=False)
#     Experience = db.Column(db.Integer, nullable=True)
#     package = db.Column(db.Integer, nullable=False)
    
@app.route('/')
def test():
    return 'this is test'

@app.route('/user', methods=['POST'])
def new_user():
    try:
        # user = {"name":"A", "lastname": "AA"}
        data = request.get_json()
        user = {"f_name" : data['firstName'], "l_name" : data['lastName'],"email" : data['email'],"dob" : data['dob'],"gender" : data['gender'],"education" : data['education'],"company" : data['company'],"Experience" : data['experience'],"package" : data['package']}
        dbResponse = db.users.insert_one(user)
        return make_response({"message":"user created","id":f"{dbResponse.inserted_id}",})
    except Exception as ex:
        return jsonify({'error': ex}), 500


@app.route('/get_user')
def getuser():
    try:
        data = list(db.users.find())
        print(data)
        for one_data in data:
            one_data["_id"] = str(one_data["_id"])
            # return jsonify(one_data)
        return make_response({"user":data})
    except Exception as ex:
        return jsonify({'error': "Can not read all users"}), 500
    


@app.route('/delete_user/<id>', methods=['DELETE'])
def deleteuser(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        return jsonify({'error': "User Deleted","id":f"{id}"})
    except Exception as ex:
        return jsonify({'error': "Can not delete all users"}), 500
    # user =User.query.filter_by(id=id).first()

    # db.session.delete(user)
    # db.session.commit()
    # return jsonify({'success': True}), 200


@app.route('/update_user/<id>', methods=['PUT'])
def updateuser(id):
    try:
        data = request.get_json()
        user = {"f_name" : data['firstName'], "l_name" : data['lastName'],"email" : data['email'],"dob" : data['dob'],"gender" : data['gender'],"education" : data['education'],"company" : data['company'],"Experience" : data['experience'],"package" : data['package']}
        dbResponse = db.users.update_one({"_id":ObjectId(id)},{"$set":user})
        return make_response({"message":"user updated"})
    except Exception as ex:
        return jsonify({'error': "Can not read all users"}), 500

# with app.app_context():
#     db.create_all()

app.run(debug=True, port=5585)
