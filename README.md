# BFHL Array Processing API

A FastAPI-based REST API that processes arrays and categorizes elements according to specific requirements.

## Features

- **POST /bfhl**: Main endpoint that processes arrays
- **GET /**: Root endpoint with API information

## API Endpoint

- **Method**: POST
- **Route**: `/bfhl`
- **Status Code**: 200 (success)

## Request Format

```json
{
  "data": ["a", "1", "334", "4", "R", "$"]
}
```

## Response Format

```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334", "4"],
  "alphabets": ["A", "R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```

## Processing Logic

1. **Numbers**: Categorized as odd or even, summed up
2. **Alphabets**: Converted to uppercase
3. **Special Characters**: Identified and separated
4. **Concatenation**: All alphabets in reverse order with alternating caps
5. **User ID**: Generated in format `fullname_ddmmyyyy`

## Testing

### Example Requests

#### Example A
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["a","1","334","4","R", "$"]}'
```

#### Example B
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["2","a", "y", "4", "&", "-", "*", "5","92","b"]}'
```

#### Example C
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["A","ABcD","DOE"]}'
```

## Error Handling

The API includes comprehensive error handling:
- Input validation using Pydantic
- Exception handling with proper HTTP status codes
- Detailed error messages for debugging
