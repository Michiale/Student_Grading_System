from  fastapi import  FastAPI

app = FastAPI()

list_of_numbers = []

@app.get('/addition/{a, b}')
def add(a:int, b:int):
    return {"Sum": a+b}

@app.get('/subtracton/{a, b}')
def sub(a:int, b:int):
    return {"Sub": a-b}


@app.post('/subtracton/{a, b}')
def add_to_list(a:int, b:int):
    list_of_numbers.append(a)
    list_of_numbers.append(b)
    return list_of_numbers





