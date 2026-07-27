from typing import Literal, Optional
from json import load, dump
from fastapi import FastAPI, Path, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
from fastapi.responses import JSONResponse

import json

app = FastAPI(title="Patient Management System API", description="A fully functional CRUD API to manage patient records.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientBase(BaseModel):
    name: Annotated[str, Field(..., description="Enter Patient Name", examples=["John Doe"])]
    city: Annotated[str, Field(..., description="Enter Patient City", examples=["New York"])]
    age: Annotated[int, Field(..., ge=0, le=150, description="Enter Patient Age", examples=[25])]
    gender: Annotated[Literal['Male', 'Female', 'male', 'female'], Field(..., description="Enter Patient Gender", examples=["Male"])]
    height: Annotated[float, Field(..., gt=0, description="Enter Patient Height in m", examples=[1.75])]
    weight: Annotated[float, Field(..., gt=0, description="Enter Patient Weight in kg", examples=[70.0])]

class Patient(PatientBase):
    id: Annotated[str, Field(..., description="Enter Patient ID", examples=["P001"])]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height * self.height), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= self.bmi < 24.9:
            return 'Normal'
        elif 25 <= self.bmi < 29.9:
            return 'Overweight'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Enter Patient Name", examples=["John Doe"])]
    city: Annotated[Optional[str], Field(None, description="Enter Patient City", examples=["New York"])]
    age: Annotated[Optional[int], Field(None, description="Enter Patient Age", examples=[25])]
    gender: Annotated[Optional[Literal['Male', 'Female', 'male', 'female']], Field(None, description="Enter Patient Gender", examples=["Male"])]
    height: Annotated[Optional[float], Field(None, description="Enter Patient Height in m", examples=[1.75])]
    weight: Annotated[Optional[float], Field(None, description="Enter Patient Weight in kg", examples=[70.0])]

def load_data():
    try:
        with open("patient.json", "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

def save_data(data: dict):
    with open("patient.json", "w") as f:
        json.dump(data, f, indent=4)

@app.get("/", tags=["General"])
def hello():
    return {'message': 'Patient Management System API'}

@app.get('/about', tags=["General"])
def about():
    return {'message': 'A fully functional API to manage your patient records.'}

@app.get('/health', tags=["General"])
def health_check():
    """Health check endpoint to ensure the API is running."""
    return {'status': 'healthy'}

@app.get('/statistics', tags=["Analytics"])
def get_statistics():
    """Returns analytics about the patient data."""
    data = load_data()
    if not data:
        return {'message': 'No data available'}
        
    total_patients = len(data)
    total_age = sum(p.get('age', 0) for p in data.values())
    avg_age = round(total_age / total_patients, 2)
    
    genders = {'male': 0, 'female': 0}
    verdicts = {}
    
    for p in data.values():
        gender_val = p.get('gender', 'unknown').lower()
        if gender_val in genders:
            genders[gender_val] += 1
        verdict = p.get('verdict', 'Unknown')
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        
    return {
        'total_patients': total_patients,
        'average_age': avg_age,
        'gender_distribution': genders,
        'verdict_distribution': verdicts
    }

@app.get('/patient', tags=["Patients"])
def get_all_patients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    city: Optional[str] = Query(None, description="Filter by city"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    name_search: Optional[str] = Query(None, description="Search by name (partial match)")
):
    data = load_data()
    
    patients_list = []
    for pid, pdata in data.items():
        pdata_copy = pdata.copy()
        pdata_copy['id'] = pid
        patients_list.append(pdata_copy)
    
    if city:
        patients_list = [p for p in patients_list if p.get('city', '').lower() == city.lower()]
    if gender:
        patients_list = [p for p in patients_list if p.get('gender', '').lower() == gender.lower()]
    if name_search:
        patients_list = [p for p in patients_list if name_search.lower() in p.get('name', '').lower()]
        
    return patients_list[skip : skip + limit]

@app.get('/patient/{patient_id}', tags=["Patients"])
def get_patient(patient_id: str = Path(..., description="Enter Patient ID", examples=["P001"])):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort', tags=["Patients"])
def sort_patient(
    sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), 
    order: str = Query('asc', description='Sort in asc or desc order')
):
    valid_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order, select from ["asc", "desc"]')
    
    data = load_data()
    sort_order = True if order.lower() == 'desc' else False
    
    sorted_data = []
    for pid, pdata in data.items():
        pdata_copy = pdata.copy()
        pdata_copy['id'] = pid
        sorted_data.append(pdata_copy)
        
    sorted_data.sort(key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post('/patient', tags=["Patients"], status_code=status.HTTP_201_CREATED)
def create_patient(patient: Patient):
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    data[patient.id] = patient.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(content={'message': 'Patient created successfully', 'patient': data[patient.id]}, status_code=status.HTTP_201_CREATED)

@app.put('/patient/{patient_id}', tags=["Patients"])
def replace_patient(
    patient_data: PatientBase, 
    patient_id: str = Path(..., description="Enter Patient ID", examples=["P001"])
):
    """Fully replaces the patient data with the provided payload."""
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
        
    try:
        updated_patient = Patient(id=patient_id, **patient_data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    data[patient_id] = updated_patient.model_dump(exclude={'id'})
    save_data(data)
    return {'message': 'Patient replaced successfully', 'patient': data[patient_id]}

@app.patch('/patient/{patient_id}', tags=["Patients"])
def update_patient(
    patient_update: PatientUpdate, 
    patient_id: str = Path(..., description="Enter Patient ID", examples=["P001"])
):
    """Partially updates the patient data."""
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    update_data = patient_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail='No fields provided for update')
        
    current_patient_data = data[patient_id]
    current_patient_data.update(update_data)
    
    try:
        updated_patient = Patient(id=patient_id, **current_patient_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    data[patient_id] = updated_patient.model_dump(exclude={'id'})
    save_data(data)
    return {'message': 'Patient updated successfully', 'patient': data[patient_id]}

@app.delete('/patient/{patient_id}', tags=["Patients"], status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str = Path(..., description="Enter Patient ID", examples=["P001"])):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    data.pop(patient_id)
    save_data(data)
    return

