from types import SimpleNamespace
from fastapi import FastAPI
from processing.process import run_process
from get_examples import examples_list
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search/{query_string}")
def read_search(query_string: str):
    response = run_process(query_string)
    res = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    return res

@app.get("/examples/")
def read_examples():
    res = examples_list()
    return res