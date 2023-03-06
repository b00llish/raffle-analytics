from app.extensions import db
from sqlalchemy.sql.functions import GenericFunction

class immutable_date_trunc(GenericFunction):
    type = db.DateTime()
    name = 'immutable_date_trunc'
    identifier = 'date_trunc'
    render_as_batch = True

    @classmethod
    def _register(cls, *args, **kwargs):
        return db.func.date_trunc(*args, **kwargs).immutable()
