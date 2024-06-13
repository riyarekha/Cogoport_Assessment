from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_configuration", response_model=schemas.ConfigurationResponse)
def create_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = models.Configuration(country_code=config.country_code, requirements=config.requirements)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@app.get("/get_configuration/{country_code}", response_model=schemas.ConfigurationResponse)
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    db_config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_config

@app.put("/update_configuration", response_model=schemas.ConfigurationResponse)
def update_configuration(config: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    db_config = db.query(models.Configuration).filter(models.Configuration.country_code == config.country_code).first()
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    db_config.requirements = config.requirements
    db.commit()
    db.refresh(db_config)
    return db_config


@app.delete("/delete_configuration", response_model=schemas.ConfigurationResponse)
def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    db_config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    db.delete(db_config)
    db.commit()
    return db_config
