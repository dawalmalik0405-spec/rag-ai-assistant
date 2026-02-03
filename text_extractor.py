from langchain_community.document_loaders import TextLoader, PyPDFLoader,Docx2txtLoader
import os



def extract_text_from_file(file_path):
    _, file_extension  = os.path.splitext(file_path)
    file_extension = file_extension.lower()
      # print(file_extension)

    if file_extension == ".txt":
        loader  = TextLoader(file_path)
        docs = loader.load()
        text = "\n".join(doc.page_content for doc in docs)
        return text
      
    elif file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text = "\n".join(doc.page_content for doc in docs)
        return text
    
    elif file_extension == ".docx":
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
        text = "\n".join(doc.page_content for doc in docs)
        return text

# l = extract_text_from_file(file_path)
# print(l)
  


