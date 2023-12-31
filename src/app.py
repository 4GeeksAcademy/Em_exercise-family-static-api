"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

#  --------------------------------------------------------------------------- Sitemap below
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ---------------------------------------------------------------------------- Endpoint to bring one family member

@app.route('/member/<int:member_id>', methods=['GET'])
def bring_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"msg": "no family member with this ID"}), 404
    return jsonify(member), 200

# ---------------------------------------------------------------------------- Endpoint to get all family members
@app.route('/members', methods=['GET'])
def bring_all_members():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200
# ---------------------------------------------------------------------------- Endpoint to add new family members
@app.route('/member', methods=['POST'])
def add_member():
    body =  request.get_json()
    member = {
        "first_name" : body["first_name"],
        "age" : body["age"],
        "lucky_numbers" : body["lucky_numbers"]
    } 
    new_member = jackson_family.add_member(member)
    response_body = {
        "msg" : "Se agrego el miembro",
        "member" : new_member
    }
    return jsonify(response_body), 200
# ---------------------------------------------------------------------------- Endpoint to update family members
@app.route("/members/<int:member_id>", methods=["PUT"])
def handle_update_member(member_id):
    json_data = request.get_json()
    result = jackson_family.update_member(member_id, json_data)
    return jsonify(result), 200
# ---------------------------------------------------------------------------- Endpoint to delete family members
@app.route('/member/<int:member_id>', methods=['DELETE'])
def handle_delete_member (member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
       return jsonify({"msg": "no family member with this ID"}), 404
    jackson_family.delete_member(member_id)
    response_body = {
        "done": True
    }
    return jsonify(response_body), 200







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
