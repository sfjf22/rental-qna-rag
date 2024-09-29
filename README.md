# Renter QNA
This is a RAG (Retrieval Augmented Generation) application. The user can ask questions about the PDF files (included in image/src/data/source) populated into a Chroma DB and the application should respond with an answer according to the context of the PDF files. In this example, the following 2 PDF files related to lease agreement are populated:
- sample_pet_policy.pdf
- sample_renters_insurance.pdf

## Sample question and answer
- Question
   ```
   curl -X POST -H "Content-Type: application/json" \
        -d '{"question": "is assistive pet allowed?"}' \
        https://xxxxxxxxxx.lambda-url.us-west-2.on.aws/submit_query
   ```
- Answer
   ```
   {"question":"is assistive pet allowed?",
    "answer":"Based on the context provided, assistive animals that provide assistance, service, and support to a disabled person are not considered pets and are not limited by this policy. Specifically, section 4 states:\n\n\"Assistive animals that provide assistance, service and support to a disabled person are not considered pets and are not limited by this Policy. However, they must be registered with management.\"\n\nSo the answer is that assistive pets are allowed, but they must be registered with the property management.",
    "sources":["src/data/source/sample_pet_policy.pdf:0:3",
               "src/data/source/sample_pet_policy.pdf:0:2",
               "src/data/source/sample_pet_policy.pdf:0:4"]
   }
   ```

## How does it work?
- PDF files are loaded into a vector DB (Chroma in this case)
- `BedrockEmbeddings` from `langchain_aws` is selected as the embedding function for this RAG app.
- This RAG app will take the user's question and merge into the Prompt Template and pass it into the LLM model "anthropic.claude-3-haiku-20240307-v1:0".
