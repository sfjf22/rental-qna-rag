import shutil
import sys
import os
from langchain_community.vectorstores import Chroma
from renter_qna.get_embedding_model import get_embedding_model

VECTOR_DB_PATH = "data/chroma"
RUNNING_IN_DOCKER = bool(os.environ.get("RUNNING_IN_DOCKER", False))
VECTOR_DB_INSTANCE = None  # Reference to singleton instance of ChromaDB


def get_vector_db_instance():
    global VECTOR_DB_INSTANCE
    if not VECTOR_DB_INSTANCE:
        if RUNNING_IN_DOCKER:
            # get an updated version of SQLite
            __import__("pysqlite3")
            sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
            # copy the db to /tmp to have write permissions in Lambda runtime
            copy_vector_db_to_tmp()

        # Init the DB.
        VECTOR_DB_INSTANCE = Chroma(
            persist_directory=get_runtime_db_path(),
            embedding_function=get_embedding_model(),
        )
        print(f"Init ChromaDB {VECTOR_DB_INSTANCE} from {get_runtime_db_path()}")

    return VECTOR_DB_INSTANCE


def copy_vector_db_to_tmp():
    """
    https://aws.amazon.com/blogs/aws/aws-lambda-now-supports-up-to-10-gb-ephemeral-storage

    While AWS Lambda includes a 512 MB temporary file system (/tmp) for your code,
    this is an ephemeral scratch resource not intended for durable storage.
    """
    dst_VECTOR_DB_PATH = get_runtime_db_path()

    if not os.path.exists(dst_VECTOR_DB_PATH):
        os.makedirs(dst_VECTOR_DB_PATH)

    tmp_contents = os.listdir(dst_VECTOR_DB_PATH)
    if len(tmp_contents) == 0:
        print(f"Copying ChromaDB from {VECTOR_DB_PATH} to {dst_VECTOR_DB_PATH}")
        os.makedirs(dst_VECTOR_DB_PATH, exist_ok=True)
        shutil.copytree(VECTOR_DB_PATH, dst_VECTOR_DB_PATH, dirs_exist_ok=True)
    else:
        print(f"DB already exists in {dst_VECTOR_DB_PATH}")


def get_runtime_db_path():
    if RUNNING_IN_DOCKER:
        return f"/tmp/{VECTOR_DB_PATH}"
    else:
        return VECTOR_DB_PATH
