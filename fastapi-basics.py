from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient', examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City where patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
    height:Annotated[float,Field(..., gt=0,description='Height of the patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the patient in kgs')]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=(self.weight/(self.height**2),2)
        return bmi 
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'normal'
        elif self.bmi <30:
            return 'Normal'
        else:
            return 'Obese'
        
'''creating a new pydantic model for updating the values as the above pydantic model is having
all the fields compulsory'''

class PatientUpdate(BaseModel):
    
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]
    

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
        
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get("/")                                       # they are endpoints 
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message':'A fully functional APi to manage your patient records'}

@app.get('/view')
def view():
    data=load_data()
    
    return data

# Path parameter        - dynamic part of url 
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str=Path(..., description='ID of the patient in the DB', examples='P001')):
    # load all the patients
    data=load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found ')

# Query - way (optional) to change url to modify behaviour of our endpoint 
@app.get('/sort')
def sort_patients(sort_by: str=Query(..., description='Sort on the basis of height, weight or bmi'),
                order:str=Query('asc',description='sort in asc or desc order')):
    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail='Invalid field select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data=load_data()
    
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

# all data received would be in the form of json
# we would have to add pydantic data to the dictionary
@app.post('/create')
def create_patient(patient:Patient):
    
    #load existing data
    data=load_data()
    
    # check if the patient laready exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    #new patient - add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    # save into the json file
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    existing_patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info():
        existing_patient_info[key]=value
        
    ''' How to update the values from json 
    existing_patient_info -> pydantic object -> calculate(updated bmi + verdict) =>
    pydantic object => dict(data[patient_id])
    '''
    existing_patient_info['id']=patient_id
    patient_pydantic_ob=Patient(**existing_patient_info)
    patient_pydantic_ob.model_dump(exclude='id')
    
    # add this diction to data
    data[patient_id]=existing_patient_info
    
    
    # save data
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    
    #load data
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'patient deleted'})
