from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ast
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    functionName: str
    test: str

@app.post("/execute")
async def execute_code(request: CodeRequest):
    local_vars = {}
    try:
        exec(request.code, {}, local_vars)
        func = local_vars.get(request.functionName)
        if func and callable(func):
            result = func(ast.literal_eval(request.test))
            return {"success": True, "result": result}
        else:
            return {"success": False, "error": f"No se encontró una función '{request.functionName}'."}
    except Exception as e:
        tb = traceback.format_exc()
        return {"success": False, "error": tb}
