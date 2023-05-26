from flask import request, make_response
from flask_restful import Resource, reqparse
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller

class Forward(Resource):

    def post(self, creditor, debtor):

        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        args = parser.parse_args()
        
        data = dict(
            initial_param = dict(
                creditor = creditor ,
                debtor = debtor ,
                content = args['content'],
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

    def post(self, creditor, messenger):

        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str)
        args = parser.parse_args()

        data = dict(
            initial_param = dict(
                creditor = creditor ,
                messenger = messenger ,
                content = args['content'],
                header = request.headers
            ),
            executer = 'villains.executer.postbox.Answer',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return dict(message=rtn_message['message']), status_code

class Request(Resource):

    def get(self, hitman):

        data = dict(
            initial_param = dict(
                hitman = hitman
            ),
            executer = 'villains.executer.postbox.MurderRequest',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_404_NOT_FOUND
        
        headers = {}
        if rtn_message:
            trace_id = rtn_message['header']['trace_id']
            span_id = rtn_message['header']['span_id']
            headers = {'x-b3-traceid':trace_id,'x-b3-spanid':span_id}

        return rtn_message, status_code, headers

api.add_resource(Forward, '/forward/<string:creditor>/<string:debtor>', endpoint='forward')
api.add_resource(Answer, '/answer/<string:creditor>/<string:messenger>', endpoint='answer')
api.add_resource(Request, '/request/<string:hitman>', endpoint='request')