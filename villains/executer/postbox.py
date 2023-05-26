from miniagent import configure, db
from miniagent.executer import ExecuterInterface
from miniagent.flask_zipkin import child_zipkin_span
from villains.adapter.kafka_producer import KafkaProducerAdapter
from villains.adapter.rest_caller import RESTCaller
from villains.dbquery.queries import select_murder_request\
    , insert_murder_request, update_is_accepted

def _get_url(agent_name:str):
    return configure.get('AGENT_ENDPOINT').get(agent_name)

class RequestPayback(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:
        
        creditor = configure.get('AGENT_NAME')
        if not creditor==configure.get('C_CREDITOR'):
            return 0, {"message":"I'm not a creditor"}
        
        debtor = configure.get('C_DEBTOR')
        messenger = configure.get('C_MESSENGER')

        content = f"Hey [{debtor}], \
                    pay back the money you borrowed from [{creditor}] \
                    right away."

        url = "http://"+_get_url(messenger)\
                 +"/forward/"+creditor+"/"+debtor
        params={'content':content}

        return rest_caller.call_post(
                    url=url, 
                    json=params
                )

class Forward(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:

        creditor = initial_param.get('creditor')
        debtor = initial_param.get('debtor')
        messenger = configure.get('AGENT_NAME')
        
        #print("initial_param : ", initial_param)
        #print("initial_param.debtor : ", type(initial_param['debtor']), initial_param['debtor'])
        #print("debtor : ", type(debtor), debtor)
        #print("debtor : ", configure.get('AGENT_ENDPOINT'))
        #print("debtor : ", configure.get('AGENT_ENDPOINT').get(debtor))
        
        url = "http://"+_get_url(debtor)\
                 +"/answer/"+creditor+"/"+messenger
        params={'content':initial_param.get('content')}

        return rest_caller.call_post(
                    url=url, 
                    json=params
                )

class Answer(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        with child_zipkin_span('executer_answer') as span:

            header = str(
                dict(
                        trace_id = span.zipkin_attrs.trace_id,
                        span_id = span.zipkin_attrs.span_id,
                        parent_span_id = span.zipkin_attrs.parent_span_id,
                        flags = span.zipkin_attrs.flags,
                        is_sampled = span.zipkin_attrs.is_sampled
                    )
            )
            
            insert_dict = dict(
                requester = configure.get('AGENT_NAME'),
                target = initial_param.get('creditor'),
                hitman = configure.get('C_HITMAN'),
                header = header
            )

            span.update_tags(
                v_murder_request=insert_dict
            )

            insert_murder_request(insert_dict)

        db.session.commit()

        return 1, {'message':insert_dict}

class NoticeMurder(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            producer: KafkaProducerAdapter,
                        ) -> tuple[int, dict]:
        
        target = initial_param.get('target')
        topic = 'postbox.'+target.lower()
        sender = configure.get('AGENT_NAME')

        message = "To {}, You will be killed by me. From {}.".format(target, sender)

        return producer.produce_message(
            topic= topic,
            message= {'message':message, 'sender':sender}
            )
        
class MurderRequest(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        hitman = initial_param.get('hitman')
        req = select_murder_request(hitman)

        result = {}
        if req:
            
            result = dict(
                requester = req.requester,
                target = req.target,
                hitman = req.hitman,
                header = eval(req.header),
                created_date = req.created_date.isoformat()
            )

            update_is_accepted(req.id)
        
        db.session.commit()

        return 1 if result else 0, result
    
class ReadMessage(ExecuterInterface):

    def execute_command(self,
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        return 1, dict(message="I'm already dead.")
