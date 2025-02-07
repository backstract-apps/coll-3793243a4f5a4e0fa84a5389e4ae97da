from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
import service, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/employees/')
async def get_employees(db: Session = Depends(get_db)):
    try:
        return await service.get_employees(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/employees/id')
async def get_employees_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_employees_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/employees/')
async def post_employees(raw_data: schemas.PostEmployees, db: Session = Depends(get_db)):
    try:
        return await service.post_employees(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/employees/id/')
async def put_employees_id(raw_data: schemas.PutEmployeesId, db: Session = Depends(get_db)):
    try:
        return await service.put_employees_id(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/employees/id')
async def delete_employees_id(id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_employees_id(db, id)
    except Exception as e:
        raise HTTPException(500, str(e))

