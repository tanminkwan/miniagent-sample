def command_converter(message: dict) -> tuple[dict, str]:

    initial_param = dict(
        requester = message.get('requester'),
        target = message.get('target'),
        hitman = message.get('hitman'),
    )

    executer = "villains.executer.postbox.NoticeMurder"

    return initial_param, executer