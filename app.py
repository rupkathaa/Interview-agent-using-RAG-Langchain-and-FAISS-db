from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from prompt import prompt_template

chat_history = []
def append_to_chat_history(message):
    chat_history.append(
        {
            "sender": "AI",
            "message": message
        }
    )
#def get_chat_history():
    #if not chat_history:
        #return "No questions asked yet."
    #return "\n".join(f"{entry['sender']}: {entry['message']}" for entry in chat_history)
    
    


Db_FAISS_PATH="vectorstore/faiss"

#loading model
llm= ChatOllama(model="mistral", temperature=0.4)

#loading embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

#loading vector store
db=FAISS.load_local(Db_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

#performing similarity search
retreiver=db.as_retriever(search_type="similarity", search_kwargs={"k":3})

prompt=PromptTemplate.from_template(template=prompt_template)

chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retreiver,
    return_source_documents=False, 
    chain_type_kwargs={"prompt": prompt}
    )

print("Hello!, I am your Interview Agent. Type 'quit' to exit")
job_description=input("Enter the job description here:")
if job_description.lower()=="quit":
    exit()

# First query to get the initial question
first_question_query = f"Based on this job description: {job_description}, ask me the first interview question."
response = chain.invoke({"query": first_question_query})
ai_question = response["result"]
print(f"AI: {ai_question}")

append_to_chat_history(ai_question)
print("-" * 50)

# Main conversational loop
while True:
    user_input = input("Your Answer: ")
    if user_input.lower() == "quit":
        print("Exiting the interview. Goodbye!")
        break

    
    feedback_query = f"Based on this job description: {job_description}, and my answer: '{user_input}',provide feedback or ask another interview question."
    
    response = chain.invoke({"query": feedback_query})

    ai_response = response["result"]
    print(f"AI: {ai_response}")
    append_to_chat_history(ai_response)
    print("-" * 50)








