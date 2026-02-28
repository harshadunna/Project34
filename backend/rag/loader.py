import os
import glob

def load_documents(data_dir: str) -> str:
    combined_text = ""
    txt_files = glob.glob(os.path.join(data_dir, "*.txt"))
    for file_path in txt_files:
        with open(file_path, "r", encoding="utf-8") as f:
            combined_text += f.read() + "\n\n"
    return combined_text
