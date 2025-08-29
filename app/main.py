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
    return re.fullmatch(r"-?\d+", s) is not None

def is_alphabet(s):
    return re.fullmatch(r"[a-zA-Z]+", s) is not None

def is_special_character(s):
    return re.fullmatch(r"[^a-zA-Z0-9\s]", s) is not None

def alternating_caps(s):
    """Convert string into alternating caps starting with uppercase."""
    result = []
    upper = True
    for ch in s:
        if ch.isalpha():
            result.append(ch.upper() if upper else ch.lower())
            upper = not upper
        else:
            result.append(ch)
    return "".join(result)

def process_array(data):
    odd_numbers, even_numbers, alphabets, special_characters = [], [], [], []
    sum_numbers = 0
    alpha_chars = []

    for item in data:
        if is_number(item):
            num = int(item)
            if num % 2 == 0:
                even_numbers.append(item)  # keep as string
            else:
                odd_numbers.append(item)
            sum_numbers += num
        elif item.isalpha():
            alphabets.append(item.upper())
            alpha_chars.extend(list(item))
        elif is_special_character(item):
            special_characters.append(item)

    # Reverse collected alphabets and apply alternating caps
    concat_string = alternating_caps("".join(alpha_chars[::-1]))

    return {
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(sum_numbers),
        "concat_string": concat_string,
    }

@app.post("/bfhl", response_model=ArrayResponse)
async def process_array_endpoint(request: ArrayRequest):
    try:
        result = process_array(request.data)
        return ArrayResponse(
            is_success=True,
            user_id=generate_user_id(),
            email="john@xyz.com",
            roll_number="ABCD123",
            odd_numbers=result["odd_numbers"],
            even_numbers=result["even_numbers"],
            alphabets=result["alphabets"],
            special_characters=result["special_characters"],
            sum=result["sum"],
            concat_string=result["concat_string"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "BFHL API running! Use POST /bfhl."}
