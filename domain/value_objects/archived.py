from pydantic import BaseModel


class Archived(BaseModel): 
    """Модель объекта-значения контрибьюторов."""
    archived: bool