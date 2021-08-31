from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

# Candidate Class/Model
class Candidate(db.Model):
    candidateId = db.Column(db.Integer, primary_key=True)
    candidateUniId = db.Column(db.String(100), unique=True)
    candidateName = db.Column(db.String(100))
    candidateEmail = db.Column(db.String(100))
    candidateImg = db.Column(db.String(200))

    def __init__(self, candidateUniId, candidateName, candidateEmail, candidateImg):
        self.candidateUniId = candidateUniId
        self.candidateName = candidateName
        self.candidateEmail = candidateEmail
        self.candidateImg = candidateImg

# Candidate Schema
class CandidateSchema(ma.Schema):
    class Meta:
        fields = ('candidateId', 'candidateUniId', 'candidateName', 'candidateEmail', 'candidateImg')

# Init Schema
candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)

# Create a Candidate
@app.route('/candidate', methods=['POST'])
def add_candidate():
    candidateUniId = request.json['candidateUniId']
    candidateName = request.json['candidateName']
    candidateEmail = request.json['candidateEmail']
    candidateImg = request.json['candidateImg']

    new_candidate = Candidate(candidateUniId, candidateName, candidateEmail, candidateImg)

    db.session.add(new_candidate)
    db.session.commit()

    return candidate_schema.jsonify(new_candidate)

# Get All Candidates
@app.route('/candidates', methods=['GET'])
def get_candidates():
    all_candidates = Candidate.query.all()
    result = candidates_schema.dump(all_candidates)
    return jsonify(result)

# Get Single Candidate
@app.route('/candidate/<string:candidateUniId>', methods=['GET'])
def get_candidate(candidateUniId):
    candidate = Candidate.query.get(candidateUniId)
    return candidate_schema.jsonify(candidate)

# Update a Candidate
@app.route('/candidate/<string:candidateUniId>', methods=['PUT'])
def update_candidate(candidateUniId):
    candidate = Candidate.query.get(candidateUniId)

    candidateUniId = request.json['candidateUniId']
    candidateName = request.json['candidateName']
    candidateEmail = request.json['candidateEmail']
    candidateImg = request.json['candidateImg']

    candidate.candidateUniId = candidateUniId
    candidate.candidateName = candidateName
    candidate.candidateEmail = candidateEmail
    candidate.candidateImg = candidateImg

    db.session.commit()

    return candidate_schema.jsonify(candidate)

# Delete Product
@app.route('/candidate/<candidateUniId>', methods=['DELETE'])
def delete_candidate(candidateUniId):
  candidate = Candidate.query.get(candidateUniId)
  db.session.delete(candidate)
  db.session.commit()

  return candidate_schema.jsonify(candidate)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)