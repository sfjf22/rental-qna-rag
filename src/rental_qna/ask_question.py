import os
import sys

from dataclasses import dataclass
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from renter_qna.get_vector_db_instance import get_vector_db_instance

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


@dataclass
class QueryResponse:
    question: str
    answer: str
    sources: List[str]


def ask_question(question: str) -> QueryResponse:
    db = get_vector_db_instance()

    # Search the DB.
    results = db.similarity_search_with_score(question, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)
    print(prompt)

    model = ChatBedrock(model_id=BEDROCK_MODEL_ID)
    response = model.invoke(prompt)
    answer = response.content

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(f"Response: {answer}\nSources: {sources}")

    return QueryResponse(
        question=question, answer=answer, sources=sources
    )


if __name__ == "__main__":
    ask_question("Is assistive pet allowed?")
