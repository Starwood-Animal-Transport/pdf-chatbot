import fitz  # PyMuPDF
import os

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract text from all PDFs in a folder
def extract_text_from_folder(folder_path):
    pdf_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Extracting text from: {pdf_path}")
            pdf_texts[filename] = extract_text_from_pdf(pdf_path)
    return pdf_texts

# Function to chunk the extracted text
def chunk_text(text, max_chunk_size=1000):
    chunks = []
    current_chunk = ""
    for line in text.split("\n"):
        if len(current_chunk) + len(line) + 1 <= max_chunk_size:
            current_chunk += line + " "
        else:
            chunks.append(current_chunk)
            current_chunk = line + " "
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# Function to chunk the text for all PDFs
def chunk_pdfs(pdf_texts):
    all_chunks = []
    for pdf_name, text in pdf_texts.items():
        chunks = chunk_text(text)
        all_chunks.extend(chunks)
    return all_chunks

# Example usage
if __name__ == "__main__":
    folder_path = r"C:\Users\wes\OneDrive\Desktop\R_Cheatsheets"  # Path to your folder with PDFs
    all_pdf_texts = extract_text_from_folder(folder_path)
    
    # Chunk the text for all PDFs
    all_chunks = chunk_pdfs(all_pdf_texts)
    
    # Print out the first 5 chunks to see the result
    for i, chunk in enumerate(all_chunks[:5]):
        print(f"\n--- Chunk {i+1} ---\n{chunk[:500]}...\n")  # Show first 500 characters of each chunk
