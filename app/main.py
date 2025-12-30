from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="FastAPI AWS Deployment",
    version="1.0.0",
    docs_url="/docs"
)

# ----- Data Contract -----
class AddRequest(BaseModel):
    a: int
    b: int

class AddResponse(BaseModel):
    result: int

# Fun stuffs
class CurrencyConvertRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class CurrencyConvertResponse(BaseModel):
    converted_amount: float
    rate_used: float

FAKE_RATES = {
    ("USD", "MYR"): 4.06,
    ("MYR", "USD"): 0.25,
    ("USD", "EUR"): 0.85,
}

# ----- Routes -----
@app.get("/")
def root():
    """
    Docstring for root
    """
    return {"message": "Welcome to the FastAPI AWS Deployment!"}    

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

@app.post("/add", response_model=AddResponse)
def add_numbers(payload: AddRequest):
    """
    Example POST endpoint with payload validation
    """
    #return AddResponse(result=request.a + request.b)
    return {"result": payload.a + payload.b}

@app.post("/convert_currency", response_model=CurrencyConvertResponse)
def convert_currency(payload: CurrencyConvertRequest):
    """
    Convert currency using fake rates
    """
    key = (payload.from_currency.upper(), payload.to_currency.upper())
    if key not in FAKE_RATES:
        raise HTTPException(status_code=400, detail="Conversion rate not found.")
    
    rate = FAKE_RATES[key]
    converted_amount = payload.amount * rate

    return {
        "converted_amount": round(converted_amount, 2),
        "rate_used": rate
    }

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)