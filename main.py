from logging import debug
import re
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class songModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plays = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"song(name = {name}, plays = {plays}, likes = {likes})"

db.create_all()

song_put_args = reqparse.RequestParser()
song_put_args.add_argument("name", type=str, help="Name is required", required=True)
song_put_args.add_argument("plays", type=int, help="Plays is required", required=True)
song_put_args.add_argument("likes", type=int, help="Likes is required", required=True)

song_update_args = reqparse.RequestParser()
song_update_args.add_argument("name", type=str, help="Name of the song")
song_update_args.add_argument("plays", type=int, help="Plays of the song")
song_update_args.add_argument("likes", type=int, help="Likes of the song")


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "plays": fields.Integer,
    "likes": fields.Integer
}

class song(Resource):
    @marshal_with(resource_fields)
    def get(self, song_id):
        result = songModel.query.filter_by(id=song_id).first()
        if not result:
            abort(404, message="Could not find song with that id...")
        return result

    @marshal_with(resource_fields)
    def put(self, song_id):
        args = song_put_args.parse_args()
        result = songModel.query.filter_by(id=song_id).first()
        if result:
            abort(409, message="Song id taken...")

        song = songModel(id=song_id, name=args["name"], plays=args["plays"], likes=args["likes"])
        db.session.add(song)
        db.session.commit()
        return song, 200

    @marshal_with(resource_fields)
    def patch(self, song_id):
        args = song_update_args.parse_args()
        result = songModel.query.filter_by(id=song_id).first()
        if not result:
            abort(404, "Song doesn't exist, cannot update")
        
        if args["name"]:
            result.name = args["name"]
        if args["plays"]:
            result.plays = args["plays"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.commit()

        return result

    
    #def delete(self, song_id):
    #    abort_if_song_id_doesnt_exist(song_id)
    #    del songs[song_id]
    #    return "", 200


api.add_resource(song, "/song/<int:song_id>")


if __name__ == "__main__":
    app.run(debug=True)
