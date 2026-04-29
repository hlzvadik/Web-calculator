from fastapi import FastAPI
import calculator_module as cm
import uvicorn

app = FastAPI()

@app.get('/eval')
async def solving_expression(expression: str = ""):
    if (len(expression) == 0):
        return {"result": 0}
    else:
        return {"result": cm.eval(expression)}

if __name__ == "__main__":
    uvicorn.run(app)

