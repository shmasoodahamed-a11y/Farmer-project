from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from auth import create_access_token
import random
# import redis  # Uncomment when your local Redis server is running

app = FastAPI(title="Gramin-Queue Auth Service")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from auth import get_current_user
from fastapi import Depends

@app.get("/api/v1/farmer/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    # If the token is invalid, FastAPI blocks the request before this code even runs!
    return {"message": "Welcome to your profile!", "user_data": current_user}
class OTPRequest(BaseModel):
    mobile_number: str = Field(..., min_length=10, max_length=15)

@app.post("/api/v1/auth/request-otp", status_code=status.HTTP_200_OK)
async def request_otp(payload: OTPRequest):
    # 1. Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # 2. Store in Redis with a 5-minute (300 seconds) expiration
    # redis_key = f"otp:{payload.mobile_number}"
    # redis_client.setex(redis_key, 300, otp)
    
    # 3. In a real scenario, dispatch to Celery worker for SMS delivery here
    print(f"DEBUG ONLY - Sending OTP {otp} to {payload.mobile_number}")
    
    return {
        "status": "SUCCESS", 
        "message": "OTP generated and dispatched successfully."
    }

@app.get("/api/v1/farmer/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    # If the token is missing, expired, or invalid, FastAPI automatically blocks the request!
    # It will throw a 401 Unauthorized error before this code even runs.
    
    return {
        "status": "SUCCESS",
        "message": "Welcome to the secure Gramin-Queue dashboard!",
        "user_data": current_user
    }

class VerifyOTPRequest(BaseModel):
    mobile_number: str = Field(..., min_length=10, max_length=15)
    otp: str = Field(..., min_length=6, max_length=6)

@app.post("/api/v1/auth/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(payload: VerifyOTPRequest):
    # In a full build, we would check Redis here to see if the OTP matches.
    # For this fast prototype, we will accept the OTP and issue the token!
    
    # Generate the JWT containing the user's role
    token = create_access_token(data={"sub": payload.mobile_number, "role": "FARMER"})
    
    return {
        "status": "SUCCESS",
        "access_token": token,
        "token_type": "bearer"
    }

class StaffLoginRequest(BaseModel):
    mobile_number: str
    password: str # In a production app, we would hash this!

@app.post("/api/v1/staff/login", status_code=status.HTTP_200_OK)
async def staff_login(payload: StaffLoginRequest):
    # Mock database check for the hackathon prototype
    if payload.mobile_number == "admin" and payload.password == "admin123":
        # Issue a JWT specifically with the STAFF role
        token = create_access_token(data={"sub": payload.mobile_number, "role": "STAFF"})
        return {
            "status": "SUCCESS",
            "access_token": token,
            "token_type": "bearer",
            "message": "Welcome to the Mandi Admin Dashboard"
        }
    
    raise HTTPException(status_code=401, detail="Invalid staff credentials")

class FarmerProfile(BaseModel):
    full_name: str
    aadhaar_hash: str
    mobile_number: str
    land_holding_hectares: float
    village_name: str

@app.post("/api/v1/farmers/register")
def register_farmer(profile: FarmerProfile):
    # In a full build, this saves to the PostgreSQL farmers table[cite: 1]
    return {
        "status": "SUCCESS", 
        "message": "Farmer successfully registered!", 
        "data": profile
    }

class StaffLoginRequest(BaseModel):
    mobile_number: str
    password: str

@app.post("/api/v1/staff/login")
def staff_login(payload: StaffLoginRequest):
    # Mocking a staff login for the hackathon prototype
    if payload.mobile_number == "admin" and payload.password == "admin123":
        # Issue a JWT specifically with the STAFF role
        token = create_access_token(data={"sub": payload.mobile_number, "role": "STAFF"})
        return {
            "status": "SUCCESS",
            "access_token": token,
            "token_type": "bearer",
            "message": "Welcome to the Mandi Admin Dashboard"
        }
    raise HTTPException(status_code=401, detail="Invalid staff credentials")