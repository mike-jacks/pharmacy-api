import json

from fastapi import FastAPI, HTTPException, status

from models import Patient

with open("patients.json", "r") as f:
    patient_list = json.load(f)

patients = [Patient(**patient) for patient in patient_list]
# Use the first name as the unique identifier. For example, in the PUT route, you'd have something like this: "/patients/{first_name}"
app = FastAPI()

@app.get("/patients")
async def get_patients():
    return patients

@app.post("/patients")
async def add_patient(new_patient: Patient):
    for patient in patients:
        if new_patient.last_name == patient.last_name:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Patient with last name {new_patient.last_name} already exists." )
    patients.append(new_patient)
    return {"detail": f"Patient successfully added."}

@app.put("/patients/{last_name}")
async def update_patient(last_name: str, new_patient: Patient):
    for i, patient in enumerate(patients):
        if patient.last_name == last_name:
            patients[i] = new_patient
            return {"detail": f"Patient with last name: {last_name} successfully updated"}
    patients.append(new_patient)
    return {"detail": f"Patient with last name: {last_name} successfully created"}

@app.delete("/patients/{last_name}")
async def delete_patient(last_name: str):
    for i, patient in enumerate(patients):
        if patient.last_name == last_name:
            patients.pop(i)
            return {"detail": f"Patient with last name: {last_name} successfully deleted."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with last name: {last_name} not found.")
                    