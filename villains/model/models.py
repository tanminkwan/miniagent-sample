from miniagent import db
from miniagent.models import YesNoEnum
from sqlalchemy import Enum

class VMurderRequest(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable=False)
   requester = db.Column(db.String(100), nullable=False)
   target = db.Column(db.String(100), nullable=False)
   hitman = db.Column(db.String(100), nullable=False)
   header = db.Column(db.String(1000))
   is_accepted = db.Column(Enum(YesNoEnum), nullable=False)
   accepted_date = db.Column(db.DateTime())
   created_date = db.Column(db.DateTime())
