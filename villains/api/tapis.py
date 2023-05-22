from flask_restful import Resource
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller

class Forward(Resource):

    def get(self, receiver, content):

        data = dict(
            init_param = dict(
                receiver = receiver ,
                content = content,
            ),
            executer = 'villains.executer.postbox.Forward',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return dict(message=rtn_message['message']), status_code
    
class Answer(Resource):

    def get(self, sender, content):

        data = dict(
            init_param = dict(
                sender = sender ,
                content = content,
            ),
            executer = 'villains.executer.postbox.Reply',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_400_BAD_REQUEST


api.add_resource(Forward, '/forward/<str:receiver>/<str:content>', endpoint='forward')
api.add_resource(Answer, '/answer/<str:sender>/<str:content>', endpoint='answer')