from . import models
from .db import engine

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
