# FastAPI-Basics

# Patient Management System API
A fully functional REST API built with FastAPI for managing patient records with complete CRUD operations, BMI calculations, and comprehensive data validation.
## 🚀 Features

Complete CRUD Operations (Create, Read, Update, Delete)
Automatic BMI Calculation with health verdict classification
Data Validation using Pydantic models
Sorting Capabilities by height, weight, or BMI
JSON-based Data Storage
Comprehensive Error Handling
Interactive API Documentation (Swagger UI)

## 📋 Requirements

Python 3.7+
FastAPI
Pydantic
Uvicorn (for running the server)

## 🛠️ Installation

Clone the repository:

bashgit clone <your-repo-url>
cd patient-management-api

Install dependencies:

bashpip install fastapi uvicorn pydantic

Create a patients.json file in the root directory:

json{}

Run the application:

bashuvicorn main:app --reload
The API will be available at http://localhost:8000
📚 API Documentation
Once the server is running, visit:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## 🏗️ Data Model
Patient Schema
python{
  "id": "P001",           # Required: Patient ID
  "name": "John Doe",     # Required: Patient name
  "city": "New York",     # Required: City of residence
  "age": 30,              # Required: Age (1-119)
  "gender": "male",       # Required: male/female/others
  "height": 1.75,         # Required: Height in meters
  "weight": 70.5,         # Required: Weight in kg
  "bmi": 23.02,          # Auto-calculated: BMI value
  "verdict": "normal"     # Auto-calculated: Health status
}
BMI Classification

Underweight: BMI < 18.5
Normal: 18.5 ≤ BMI < 25
Overweight: 25 ≤ BMI < 30
Obese: BMI ≥ 30

## 🔄 CRUD Operations
### CREATE - Add New Patient
httpPOST /create
Content-Type: application/json

{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.5
}
Response:
json{
  "message": "patient created successfully"
}
### READ - Get Patient Data
Get All Patients
httpGET /view
Get Specific Patient
httpGET /patient/{patient_id}
Example:
httpGET /patient/P001
Response:
json{
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70.5,
  "bmi": 23.02,
  "verdict": "normal"
}
Get Sorted Patients
httpGET /sort?sort_by=bmi&order=desc
Parameters:

sort_by: height, weight, or bmi
order: asc or desc (default: asc)

### UPDATE - Modify Patient Data
httpPUT /edit/{patient_id}
Content-Type: application/json

{
  "weight": 75.0,
  "city": "Los Angeles"
}
Features:

Partial updates supported (only send fields to update)
BMI and verdict automatically recalculated
Data validation on all fields

Response:
json{
  "message": "patient updated"
}
### DELETE - Remove Patient
httpDELETE /delete/{patient_id}
Example:
httpDELETE /delete/P001
Response:
json{
  "message": "patient deleted"
}
📝 Additional Endpoints
System Information
httpGET /              # Welcome message
GET /about         # API description
## 🧪 Example Usage
Complete Workflow Example

Create a patient:

bashcurl -X POST "http://localhost:8000/create" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "P001",
    "name": "Alice Smith",
    "city": "Boston",
    "age": 28,
    "gender": "female",
    "height": 1.65,
    "weight": 60.0
  }'

View the patient:

bashcurl "http://localhost:8000/patient/P001"

Update patient weight:

bashcurl -X PUT "http://localhost:8000/edit/P001" \
  -H "Content-Type: application/json" \
  -d '{"weight": 65.0}'

Get all patients sorted by BMI:

bashcurl "http://localhost:8000/sort?sort_by=bmi&order=asc"

Delete the patient:

bashcurl -X DELETE "http://localhost:8000/delete/P001"
## ⚠️ Error Handling
The API provides comprehensive error handling:

400 Bad Request: Invalid data or patient already exists
404 Not Found: Patient not found
422 Unprocessable Entity: Validation errors

Example Error Response:
json{
  "detail": "Patient not found"
}
## 🏁 Key Features Demonstrated
CRUD Compliance:

✅ Create: POST /create - Add new patients with full validation
✅ Read: GET /view, GET /patient/{id}, GET /sort - Multiple read operations
✅ Update: PUT /edit/{id} - Partial and full updates with recalculation
✅ Delete: DELETE /delete/{id} - Safe patient removal

Advanced Features:

Computed Fields: Automatic BMI and health verdict calculation
Data Validation: Pydantic models ensure data integrity
Flexible Updates: Optional fields for partial updates
Query Parameters: Sorting and filtering capabilities
Path Parameters: Dynamic URL routing
Error Handling: Comprehensive HTTP status codes and messages

## 🔧 Technical Architecture

Framework: FastAPI for high-performance async API
Validation: Pydantic for data modeling and validation
Storage: JSON file-based persistence
Documentation: Auto-generated OpenAPI/Swagger docs
Type Hints: Full Python type annotation support
