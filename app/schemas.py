from pydantic import BaseModel, Field
from typing import Dict, Any

class ConfigurationCreate(BaseModel):
    country_code: str = Field(..., example="IN")
    requirements: Dict[str, Any] = Field(..., example={"Business Name": "string", "PAN": "string", "GSTIN": "string"})

class ConfigurationUpdate(BaseModel):
    country_code: str = Field(..., example="IN")
    requirements: Dict[str, Any] = Field(..., example={"Business Name": "string", "PAN": "string", "GSTIN": "string"})

class ConfigurationResponse(BaseModel):
    country_code: str
    requirements: Dict[str, Any]
