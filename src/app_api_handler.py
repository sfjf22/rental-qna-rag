import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
from renter_qna.ask_question import QueryResponse, ask_question

app = FastAPI()
handler = Mangum(app)  # Entry point for AWS Lambda.


class SubmitQueryRequest(BaseModel):
    question: str


@app.get("/")
def index():
    return {"renter_qna": "v0.1.3"}


@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryResponse:
    query_response = ask_question(request.question)
    return query_response


if __name__ == "__main__":
    # Run this to test locally
    port = 8000
    print(f"Running server on port {port}.")
    uvicorn.run("app_api_handler:app", host="0.0.0.0", port=port)
