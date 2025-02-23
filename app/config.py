from dotenv import load_dotenv

import os
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader

load_dotenv()

# Consistent variable name
API_KEY = os.getenv("TELEX_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def validate_api_key(api_key: str = Depends(api_key_header)):
    print(f"DEBUG: Received API Key = {api_key}, Expected = {API_KEY}") 
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key