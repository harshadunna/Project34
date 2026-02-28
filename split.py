import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_pdf_to_txt(pdf_path, output_dir):
    # 1️⃣ Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 2️⃣ Load the PDF
    print(f"Loading {pdf_path}...")
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"Successfully loaded {len(documents)} pages")
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return

    # 3️⃣ Configure the Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", r"(?<=\. )", " ", ""]
    )

    # 4️⃣ Split documents into chunks
    print("Splitting text into chunks...")
    chunks = text_splitter.split_documents(documents)

    # 5️⃣ Save chunks as individual .txt files
    print(f"Saving {len(chunks)} chunks to {output_dir}...")

    for i, chunk in enumerate(chunks):
        filename = f"chunk_{i+1:03d}.txt"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(chunk.page_content)

    print("Done! All .txt files are ready.")


if __name__ == "__main__":
    INPUT_PDF = r"D:\aitam\Project34\airport.pdf"
    OUTPUT_FOLDER = r"D:\aitam\Project34\data_chunks"

    split_pdf_to_txt(INPUT_PDF, OUTPUT_FOLDER)