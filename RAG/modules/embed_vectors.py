from pinecone import Pinecone
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_pdf_file(data):
    loader  = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

loaded_data = load_pdf_file(data=".\data")


def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=40)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks=text_split(loaded_data)
print("Length of Text Chunks", len(text_chunks))

print(text_chunks[1999])
print(text_chunks[2000])
print(text_chunks[2001])

def download_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

embeddings = download_hugging_face_embeddings()


from pinecone import Pinecone

index_name="meditalk"

pc = Pinecone(api_key="PINECONE_API_KEY")

index = pc.Index(index_name)

id = 1

for t in text_chunks:
    embeds = embeddings.embed_query(t.page_content)
    meta = {
        "source":t.metadata["source"],
        "text":t.page_content,
        "page":t.metadata["page"]
    }
    index.upsert(
  vectors=[
    {"id": str(id), 
    "values": embeds,
    "metadata":meta
    }
  ])
    id = id + 1



