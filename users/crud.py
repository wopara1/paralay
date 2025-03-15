from sqlalchemy.orm import Session

from . import models
from . import schemas

def get_all_users(db: Session):
    return db.query(models.User).all()