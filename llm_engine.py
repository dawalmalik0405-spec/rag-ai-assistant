from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os 
from retriver import search_query
from vectordb import collection, embeddings
from langchain_community.chat_message_histories import FileChatMessageHistory


load_dotenv()



# chat_history = FileChatMessageHistory("chat_history.json")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
    temperature=0
)
# print(f"Using Groq model: {model_name}")
# return ChatGroq(
# api_key=os.getenv("GROQ_API_KEY"), model=model_name, temperature=0.0)
def llm_core(query, formatted_history, filename=None):
    chunks  = search_query(query, collection, embeddings, filename)


    context = "\n".join([chunk["content"] for chunk in chunks])




    prompt_template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a document-grounded AI assistant.\n"
            "Rules:\n"
            "1. Answer ONLY using the provided context.\n"
            "2. Do NOT use outside knowledge.\n"
            "3. If the answer is not present, say 'I don't know'.\n"
            "4. Be concise, structured, and factual.\n"
            "5. When appropriate, explain in steps or bullet points."
            "6. Always greet user with full energy and always encourage the user. "
        ),
        (
            "human",
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
    ])



    

      # Placeholder for assistant response

    messages = prompt_template.format_messages(context=context,chat_history=formatted_history, question=query)
    response = llm.invoke(messages)

    return(response.content)



# result = llm_core()
# print("Response from LLM:")
# print(result)


# def chat_with_llm():
    
#     while True:
#         query = input("You: ").strip()
#         if query.lower() in {"exit", "quit"}:
#             # print("Exiting chat.")
#             break
        
#         chat_history.add_user_message(query)
#         formatted_history = "\n".join(
#             f"{msg.type.upper()}: {msg.content}"
#             for msg in chat_history.messages
#         )
#         answer = llm_core(query, formatted_history)
#         # print(f"AI: {answer}")
#         chat_history.add_ai_message(answer)

    
        
# if __name__ == "__main__":
#     chat_with_llm()

    




