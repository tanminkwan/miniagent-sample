import os
from datetime import datetime, timedelta

PORT = 17080

AGENT_NAME = 'blue-skull13'

ZIPKIN_ADDRESS = ('localhost',9411)

COMMANDER_SERVER_URL = 'http://localhost:8809'

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app.db')

CUSTOM_MODELS_PATH = "villains.model"

CUSTOM_APIS_PATH = "villains.api"

KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

EXECUTERS_BY_TOPIC =\
{
    "BS13_POSTBOX":
    "villains.executer.postbox.ReadMessage",
}

SCHEDULED_JOBS =\
[
    {
        "executer":"villains.executer.scheduler.PostMessage",
        "trigger":"interval",
        "id":"DeviceHealth",
        "name":"Devices Health Check",
        "minutes":20,
        "start_date":datetime.now()+timedelta(minutes=1)
    }
]