from pydantic import BaseModel, field_validator
from typing import Optional, List, Union


class ValuationItem(BaseModel):
    List_Price: Optional[float] = None
    Zestimate: Optional[float] = None
    ARV: Optional[float] = None
    Expected_Rent: Optional[float] = None
    Rent_Zestimate: Optional[float] = None
    Low_FMR: Optional[float] = None
    High_FMR: Optional[float] = None
    Redfin_Value: Optional[float] = None
    Previous_Rent: Optional[float] = None


class HOAItem(BaseModel):
    HOA: Optional[float] = None
    HOA_Flag: Optional[str] = None


class RehabItem(BaseModel):
    Underwriting_Rehab: Optional[float] = None
    Rehab_Calculation: Optional[float] = None
    Flooring_Flag: Optional[str] = None
    Foundation_Flag: Optional[str] = None
    Roof_Flag: Optional[str] = None
    HVAC_Flag: Optional[str] = None
    Kitchen_Flag: Optional[str] = None
    Bathroom_Flag: Optional[str] = None
    Appliances_Flag: Optional[str] = None
    Windows_Flag: Optional[str] = None
    Landscaping_Flag: Optional[str] = None
    Trashout_Flag: Optional[str] = None


class PropertyRecord(BaseModel):
    Address: Optional[str] = None
    City: Optional[str] = None
    State: Optional[str] = None
    Zip: Optional[str] = None
    SQFT_Total: Union[str, int, None] = None
    Bed: Optional[int] = None
    Bath: Optional[int] = None
    Year_Built: Optional[int] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None

    Valuation: List[ValuationItem] = []
    HOA: List[HOAItem] = []
    Rehab: List[RehabItem] = []

    @field_validator("SQFT_Total", mode="before")
    def normalize_sqft(cls, v):
        """Convert int to string, allow None."""
        if v is None:
            return None
        return str(v)

    class Config:
        extra = "allow"
