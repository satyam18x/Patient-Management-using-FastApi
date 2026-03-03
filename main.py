from fastapi import FastAPI
from pydantic import BaseModel,Field, EmailStr
from fastapi.responses import JSONResponse
from typing import List, Dict, Annotated ,Literal , Optional
import json

app=FastAPI()

class Patient(BaseModel):

    id: Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name: str = Annotated[str,Field(...,description="Name of the patient")] 
    age: int = Annotated[int,Field(...,gt=0,lt=120 , description="Age of the patient")]
    gender: Annotated[Literal['male','female'],Field(...,description="gender of the patient")]

class Patientupdate(BaseModel):

    id: Annotated[Optional[str],Field(default=None)]
    name: str = Annotated[Optional[str],Field(default=None)] 
    age: int = Annotated[Optional[int],Field(default=None,gt=0)]
    gender: Annotated[Optional[Literal['male','female']],Field(default=None)]    
  

def load_data():
    with open('Patient.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('Patient.json','w') as f:
        json.dump(data, f)


@app.get('/')
def hello():
    return{'message':'hello'}

@app.get('/about')
def about():
    return{'message':'hii'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.post('/create')
def create_patient(patient_var: Patient):

    # Load existing data
    data = load_data()

    # Check if patient exists
    if str(patient_var.id) in data:
        raise HTTPException(
            status_code=400,
            detail='Patient already exists'
        )

    # Add new patient
    data[str(patient_var.id)] = patient_var.model_dump(exclude=['id'])

    # Save data
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={'message': 'Patient created successfully'}
    )

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update: Patientupdate):

     # Load existing data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        ) 

    existing_data_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,value in  updated_patient_info.items():
        existing_data_info[key] = value

    data[patient_id] = existing_data_info

    save_data(data)    
     
    return JSONResponse(
        status_code=200,
        content={'message': 'Patient updated successfully'}
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    #load data
    data = load_data()

 #if data is not present then raise error
    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        ) 

        #delete patient

    del data[patient_id]
 # then save data
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'Patient deleted successfully'}
    )
