from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3

import jwt

import datetime

from pathlib import Path

async def get_employees(db: Session):

    employees_all = db.query(models.Employees).order_by(models.Employees.id).all()
    employees_all = [new_data.to_dict() for new_data in employees_all] if employees_all else employees_all

    res = {
        'employees_all': employees_all,
    }
    return res

async def get_employees_id(db: Session, id: int):

    employees_one = db.query(models.Employees).filter(models.Employees.id == id).first() 
    employees_one = employees_one.to_dict() if employees_one else employees_one

    res = {
        'employees_one': employees_one,
    }
    return res

async def post_employees(db: Session, raw_data: schemas.PostEmployees):
    name:str = raw_data.name
    employee_id:int = raw_data.employee_id
    age:int = raw_data.age
    username:str = raw_data.username
    password:str = raw_data.password
    emailid:str = raw_data.emailid


    record_to_be_added = {'id': employee_id, 'name': name, 'employee_id': employee_id, 'age': age, 'username': username, 'password': password, 'emailid': emailid}
    new_employees = models.Employees(**record_to_be_added)
    db.add(new_employees)
    db.commit()
    db.refresh(new_employees)
    employees_inserted_record = new_employees.to_dict()



    query = db.query(models.Employees)
    query = query.filter(
        
        and_(
            models.Employees.name == name
        )
    )

    query = query.order_by(models.Employees.id.asc())
    employee_list = query.all()


    employee_length = []  # Creating new list



    # Get the length of the list 'employee_length'
    employees_inserted_record['age'] = len(employee_length)


    # Clear all elements from the list 'employee_list'
    employee_list.clear()
    res = {
        'employees_inserted_record': employees_inserted_record,
    }
    return res

async def put_employees_id(db: Session, raw_data: schemas.PutEmployeesId):
    id:str = raw_data.id
    name:str = raw_data.name
    employee_id:str = raw_data.employee_id
    age:str = raw_data.age
    username:str = raw_data.username
    password:str = raw_data.password
    emailid:str = raw_data.emailid


    employees_edited_record = db.query(models.Employees).filter(models.Employees.id == id).first()
    for key, value in {'id': id, 'name': name, 'employee_id': employee_id, 'age': age, 'username': username, 'password': password, 'emailid': emailid}.items():
          setattr(employees_edited_record, key, value)
    db.commit()
    db.refresh(employees_edited_record)
    employees_edited_record = employees_edited_record.to_dict() 

    res = {
        'employees_edited_record': employees_edited_record,
    }
    return res

async def delete_employees_id(db: Session, id: int):

    employees_deleted = None
    record_to_delete = db.query(models.Employees).filter(models.Employees.id == id).first()

    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        employees_deleted = record_to_delete.to_dict() 

    res = {
        'employees_deleted': employees_deleted,
    }
    return res

