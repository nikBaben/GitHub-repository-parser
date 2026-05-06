from pydantic import BaseModel


class Archived(BaseModel): 
    """Модель объекта-значения архива."""
    archived: bool