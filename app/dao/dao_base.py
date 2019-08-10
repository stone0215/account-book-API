from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()


class DaoBase():
    def getDB(self):
        return db

    def session_commit(self):
        """Commit db action."""
        try:
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            reason = str(error)
            return reason
        return ''
