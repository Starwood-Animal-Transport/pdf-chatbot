import streamlit as st
import os
from openai import OpenAI

# Import the PDF extractor functions from your pdf_extractor.py file
from pdf_extractor import extract_text_from_folder, chunk_pdfs

# Set the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Step 1: Extract text from all PDFs in the folder (only needed for the first message)
folder_path = r"C:\Users\wes\OneDrive\Desktop\R_Cheatsheets"  # Update with your actual path
all_pdf_texts = extract_text_from_folder(folder_path)

# Step 2: Chunk the text for all PDFs (only needed for the first message)
all_chunks = chunk_pdfs(all_pdf_texts)

# Store the initial context (only for the first query)
context_message = {
    "role": "system",
    "content": f"You are a helpful assistant. Here is the context based on the PDFs: {''.join(all_chunks[:5])[:500]}"  # First 500 characters only
}

# Initialize the conversation history list
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize input query in session state if not already present
if "input_query" not in st.session_state:
    st.session_state.input_query = ""

# Function to query OpenAI with a user's prompt and conversation history
def query_openai(conversation_history, first_query=False):
    try:
        # Add context message only for the first query
        if first_query:
            conversation_history = [context_message] + conversation_history
        
        # Send the request to OpenAI API
        response = client.chat.completions.with_raw_response.create(
            model="gpt-4",  # You can use "gpt-3.5-turbo" or another model
            messages=conversation_history
        )
        
        # Parse the response
        completion = response.parse()

        # Access and return the message content from the response
        if hasattr(completion.choices[0], 'message'):
            message_content = completion.choices[0].message.content
            return message_content.strip()
        else:
            return "No response generated."

    except Exception as e:
        return f"Error in API request: {e}"

# Callback function to handle input submission
def handle_submit():
    user_query = st.session_state.input_query
    if user_query:
        # Step 3: Add user's query to the conversation history
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Step 4: Determine if this is the first query (to include the context)
        first_query = len(st.session_state.messages) == 1

        # Step 5: Query the OpenAI API with the conversation history
        response = query_openai(st.session_state.messages, first_query=first_query)
        
        # Step 6: Add assistant's response to the conversation history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Step 7: Clear the input field after submission
        st.session_state.input_query = ""  # Clear the input field

# Streamlit UI
st.title("PDF-Based AI Chatbot with Follow-up Questions")

# Show the conversation history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.write(f"**You**: {message['content']}")
    else:
        st.write(f"**Assistant**: {message['content']}")

# Input field for user query with on_change callback
st.text_input("Ask a question or continue the conversation:", key="input_query", on_change=handle_submit)
