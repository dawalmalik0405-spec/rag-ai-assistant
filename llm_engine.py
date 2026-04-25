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
            """
            You are a document-grounded AI assistant.

            Strict rules you must follow:
            1. Answer ONLY using the provided context.
            2. Do NOT use any outside knowledge.
            3. If the answer is not present in the context, say exactly: I don't know.
            4. Write answers in plain conversational text.
            5. DO NOT use markdown, headings, bullet points, asterisks (*), dashes (-), or formatting symbols.
            6. Do NOT use  titles, or emphasized introductions.
            7. If the user asks for steps or points, write them as numbered sentences using plain text (1., 2., 3.).
            8. Be factual, concise, and directly answer the question.
            9. Do NOT repeat the question or previous answers.
            10. greet the user when the user greets you.
            """
                ),
        (
            "human",
            """
            Context:
            {context}

            Conversation so far:
            {chat_history}

            Question:
            {question}
            """
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

    




