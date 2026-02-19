from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

def build_rag_chain(vectorstore, groq_api_key):

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_template("""
You are a Smart Contract Assistant.

Answer ONLY using the provided context.
If the answer is not found, say:
"Not found in the document."

Context:
{context}

Question:
{question}
""")
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=groq_api_key,
      
    )

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever
