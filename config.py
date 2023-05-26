import os
from datetime import datetime, timedelta

#Custom Valuables
C_CREDITOR = 'blueskull13'
C_MESSENGER = 'freddy'
C_DEBTOR = 'jason'
C_HITMAN = 'jigsaw'
C_TARGET = 'blueskull13'

#PORT = 17080

#AGENT_NAME = os.environ.get('AGENT_NAME') or 'blueskull13'
import __main__
AGENT_NAME = os.path.basename(__main__.__file__).split('.')[0]

ZIPKIN_ADDRESS = ('localhost',9411)

if AGENT_NAME == C_HITMAN:
    COMMANDER_SERVER_URL = 'http://localhost:8303/api/v1/request/'+AGENT_NAME
    COMMANDER_MESSAGE_CONVERTER = "villains.executer.command_converter"

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, AGENT_NAME+'.app.db')

CUSTOM_MODELS_PATH = "villains.model"

CUSTOM_APIS_PATH = "villains.api"

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

EXECUTERS_BY_TOPIC =\
{
    "postbox."+AGENT_NAME.lower():
    "villains.executer.postbox.ReadMessage",
}

SCHEDULED_JOBS =\
[
    {
        "executer":"villains.executer.postbox.RequestPayback",
        "trigger":"interval",
        "id":"request_payback",
        "name":"Request Payback",
        "minutes":2,
        "start_date":datetime.now()+timedelta(minutes=1)
    }
]

AGENT_ENDPOINT =\
{
    "blueskull13":"localhost:8301/api/v1",
    "freddy":"localhost:8302/api/v1",
    "jason":"localhost:8303/api/v1",
    "jigsaw":"localhost:8304/api/v1",
}