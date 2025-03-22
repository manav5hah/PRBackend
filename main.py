from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from repository.estro import Estro
from security.secure import Authorization
from models.client_master import UserClientCode, UserMCap


app = FastAPI()
auth = Authorization() 

@app.on_event("startup")
def add_custom_headers():
    openapi_schema = app.openapi()
    # Define a custom header
    openapi_schema["components"]["headers"] = {
        "X-Authorization": {
            "description": "Custom authorization header",
            "required": True,
            "schema": {
                "type": "string",
                "example": "<your_token_here>",
            },
        }
    }
    
    # Assign this custom header to all paths in the OpenAPI schema
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "parameters" not in operation:
                operation["parameters"] = []
            operation["parameters"].append({
                "in": "header",
                "name": "x-authorization",
                "required": True,
                "schema": {
                    "type": "string",
                    "example": "<your_token_here>"
                }
            })
    
    app.openapi_schema = openapi_schema

@app.post('/users/pan')
def users_client_code(client:UserClientCode):
    if client.client_id == None:
        return JSONResponse(content={'message':'Client id is requried'}, status_code=500)
    repo:Estro = Estro('Estro', auth.username, auth.password)
    result = repo.get_accounts(client.client_id)
    return JSONResponse(content=result.to_dict(orient='records'), status_code=202)

@app.post('/users/mcap')
def users_mcap(user:UserMCap):
    if user.family_code == None and user.client_code == None:
        return JSONResponse(content={'message':'Client code or family code is requried'}, status_code=500)
    repo:Estro = Estro('Estro', auth.username, auth.password)
    if user.family_code != None:
        result = repo.get_mcap_fc(user.family_code)
    if user.client_code != None:
        result = repo.get_mcap_cc(user.client_code)
    return JSONResponse(content=result, status_code=202)

@app.middleware('http')
async def authenticate(request:Request, call_next):
    if request.url.path == "/docs" or request.url.path == "/openapi.json":
        return await call_next(request)
    if 'x-authorization' not in request.headers:
        return JSONResponse(content={'detail': 'Authorization header missing'}, status_code=401)
    request_token = request.headers['x-authorization']
    auth.set_cred(request_token)
    response = await call_next(request)
    return response