from sqlalchemy.orm import Session
from core.interfaces.repository_interface import IRepository


class BaseRepository(IRepository):
    def __init__(self, model, session: Session) -> None:
        self.model = model
        self.session: Session = session

    def create(self, data: dict) -> None:
        model = self.model(**data)
        self.session.add(model)
        self.session.commit()

    def exists(self, title: str) -> bool:
        return self.session.query(self.model).filter_by(title=title).first() is not None
