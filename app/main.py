from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import re
from datetime import datetime

app = FastAPI(title="BFHL API", description="Array Processing API", version="1.0.0")

class ArrayRequest(BaseModel):
    data: List[str]

class ArrayResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    odd_numbers: List[str]
    even_numbers: List[str]
    alphabets: List[str]
    special_characters: List[str]
    sum: str
    concat_string: str

def generate_user_id(full_name="john_doe"):
    current_date = datetime.now()
    date_str = current_date.strftime("%d%m%Y")
    return f"{full_name.lower()}_{date_str}"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_alphabet(s):
    return bool(re.match(r'^[a-zA-Z]+$', s))

def is_special_character(s):
    return bool(re.match(r'^[^a-zA-Z0-9\s]+$', s))

def process_array(data):
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    sum_numbers = 0
    alphabet_chars = []
    
    for item in data:
        if is_number(item):
            num = float(item)
            if num.is_integer():
                num_int = int(num)
                if num_int % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                sum_numbers += num_int
        elif is_alphabet(item):
            alphabets.append(item.upper())
            alphabet_chars.extend(list(item))
        elif is_special_character(item):
            special_characters.append(item)
    
    if alphabet_chars:
        reversed_chars = list(reversed(alphabet_chars))
        concat_string = ""
        for i, char in enumerate(reversed_chars):
            if i % 2 == 0:
                concat_string += char.upper()
            else:
                concat_string += char.lower()
    else:
        concat_string = ""
    
    return {
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(int(sum_numbers)),
        "concat_string": concat_string
    }

@app.get("/")
async def root():
    return {"message": "BFHL API is running! Use POST /bfhl to process arrays."}

@app.post("/bfhl", response_model=ArrayResponse)
async def process_array_endpoint(request: ArrayRequest):
    try:
        result = process_array(request.data)
        
        response = ArrayResponse(
            is_success=True,
            user_id=generate_user_id(),
            email="john@xyz.com",
            roll_number="ABCD123",
            odd_numbers=result["odd_numbers"],
            even_numbers=result["even_numbers"],
            alphabets=result["alphabets"],
            special_characters=result["special_characters"],
            sum=result["sum"],
            concat_string=result["concat_string"]
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing array: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
