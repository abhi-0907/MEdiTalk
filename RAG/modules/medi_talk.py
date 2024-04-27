from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import CTransformers
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


def query_meditalk(query):
    
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    pc = Pinecone(api_key="fb0a5867-42bb-4432-ace6-fe0db1fba076")
    index = pc.Index('meditalk')
    text_field = "text"
    vectorstore = PineconeVectorStore(index, embeddings, text_field)

    template = """
    <|context|>
    You are MediTalk, a reliable Medical Assistant who answers medical related queries in four to five sentences.
    Please be truthful and give direct answers
    </s>
    <|user|>
    {query}
    </s>
    <|assistant|>
    """

    PROMPT=ChatPromptTemplate.from_template(template=template)

    llm = CTransformers(model="B:\llama-2-7b-chat.Q8_0.gguf",
                    model_type="llama",
                    config={'max_new_tokens':2048,
                            'temperature':0.3,
                            'context_length' : 2048
                            },
                            )

    retriever = vectorstore.as_retriever(search_kwargs={'k': 5})

    rag_chain = (
        {"context": retriever,  "query": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(query)
    return result


