from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def create_documents(segments):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    docs = []

    for segment in segments:

        split_docs = splitter.create_documents(
            [segment["text"]]
        )

        for doc in split_docs:

            doc.metadata = {
                "start": segment["start"],
                "end": segment["end"]
            }

            docs.append(doc)

    return docs