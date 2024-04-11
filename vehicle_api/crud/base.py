from sqlalchemy.orm import Session

from vehicle_api.model.base import Base


class BaseRepository[ModelType: Base]:
    def __init__(self, session: Session, model_type: ModelType) -> None:
        self._sess = session
        self._model_type = model_type

    @property
    def connection(self) -> Session:
        return self._sess
