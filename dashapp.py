from app import create_app
from app.extensions import db
from app.models import Raffler, Raffle, Buy, Cancel, End, Winner

server = create_app()


@server.shell_context_processor
def make_shell_context():
    return {'db': db, 'Raffler': Raffler, 'Raffle': Raffle, 'Buy': Buy,
            'Cancel': Cancel, 'End': End, 'Winner': Winner
            }