from villains.model.models import VMurderRequest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import insert, update
from miniagent import db
from datetime import datetime

def select_murder_request(hitman: str):

    req = VMurderRequest.query\
        .filter(VMurderRequest.is_accepted == 'NO',
                VMurderRequest.hitman == hitman).first()
    
    return req

def insert_murder_request(data: dict):

    insert_dict = data.copy()
    insert_dict.update(dict(
        is_accepted = 'NO',
        created_date = datetime.now()
    ))
    stmt = insert(VMurderRequest).values(**insert_dict)
    db.session.execute(stmt)

def update_is_accepted(id: int):

    stmt = update(VMurderRequest)\
        .where(VMurderRequest.id==id)\
        .values(is_accepted='YES',accepted_date=datetime.now())
    db.session.execute(stmt)