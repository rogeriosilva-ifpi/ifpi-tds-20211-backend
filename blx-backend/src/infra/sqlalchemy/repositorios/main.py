from sqlalchemy.orm import Session


class RepositorioBase():

    def __init__(self, db: Session):
        self.db = db
