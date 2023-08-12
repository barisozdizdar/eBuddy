from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import sys
import os
import openai
'''
This python program takes the private external data from the local files and stores them inside a vector store (index.json)
Later compares query embeddings and the most relevant chunk that is looked up to the index file by top_k_score algorithm,
then both the query and the relevant information is sent to the API to get the right answer of user's question. 
'''


class eBuddy:
        
    def construct_index(directory):

        #OpenAI API KEY is set. 
        os.environ["OPENAI_API_KEY"] = "SECRET KEY"
        # set maximum input size
        maximum_input_size = 4096
        # set number of output tokens
        number_of_output_tokens = 2000
        # set maximum chunk overlap
        maximum_chunk_overlap = 20
        # set chunk size limit
        chunk_limit = 600 

        # define prompt helper, prompt helper is passed attributs which defines how the text in index json file will be splitted, also the input size is set
        promptHelper = PromptHelper(maximum_input_size, number_of_output_tokens, maximum_chunk_overlap, chunk_size_limit=chunk_limit)

        # defines LLM, in our case it is OpenAI, some additional arguments are passed like which pre-trained model will be used 
        # and the maximum output tokens for the response from the OpenAI API
        llmPredictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=number_of_output_tokens))
    
        #Can read files into seperate documents, loads the private external data from the input dir.
        external_data = SimpleDirectoryReader(directory).load_data() 
        
        serviceContext = ServiceContext.from_defaults(llm_predictor=llmPredictor, prompt_helper=promptHelper)

        #creates indexes from documents that are passed if multiple documents are passes they are combined into one file
        #index file contains the chunks, also the vectors of each chunk.
        index = GPTSimpleVectorIndex.from_documents(external_data, service_context=serviceContext)

        #saves the index file into local directory
        index.save_to_disk('index4.json')

        return index
    
    #construct_index("/Users/orbiszeus/eBuddy/dataset/LATEST_DATA")
    


def ask_ebuddy(query):
    os.environ["OPENAI_API_KEY"] = "SECRET KEY"
    index = GPTSimpleVectorIndex.load_from_disk('/Users/orbiszeus/eBuddy/index4.json')
    
    while True:
        #query = input("What do you want to ask to E-Buddy? ")

        #sends the prompt (question) to OpenAI API with the most relevant chunk from the index file and the query from the user to get the response.
        response = index.query(query, response_mode="default", verbose=True)
    
        #print("\n\nEbuddy :\n\n" + response.response + "\n\n\n")
        return str(response.response)    




#ask_ebuddy()