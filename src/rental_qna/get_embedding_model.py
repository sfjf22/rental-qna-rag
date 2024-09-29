from langchain_aws import BedrockEmbeddings


# This will be called by different functions.
# Move this to its own file for easy update.
def get_embedding_model():
    embeddings = BedrockEmbeddings()
    return embeddings
