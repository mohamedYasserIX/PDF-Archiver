from langchain_core.tools import tool
from pathlib import Path
import shutil
import re
import fitz  
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from state import AgentState #  تأكد إنك عندك ملف state.py وفيه تعريف AgentState


# -------------------------------
# ✅ Create Category Folder Tool
# -------------------------------
@tool
def make_dir(state: AgentState, name: str) -> AgentState:
    """
    Creates a subdirectory (category) in the base directory if it doesn't exist.
    Also updates the list of categories in the state.
    """
    try:
        base_path = Path(state['dir'])
        category_path = base_path / name

        if base_path.is_dir() and not category_path.exists():
            category_path.mkdir(parents=True)
            if name not in state['category']:
                state['category'].append(name)

    except Exception as e:
        print(f"Error creating directory '{name}': {e}")

    return state


# -------------------------------
# ✅ Move PDF to Category Folder
# -------------------------------
@tool
def pdf_move_category(state: AgentState, category: str) -> AgentState:
    """
    Moves the current PDF file to the specified category folder.
    Updates the path in pdf_curr and adds the category if new.
    """
    try:
        base_path = Path(state['dir'])
        current_file = base_path / state['pdf_curr']
        category_dir = base_path / category
        new_path = category_dir / state['pdf_curr']

        category_dir.mkdir(exist_ok=True)

        shutil.move(str(current_file), str(new_path))
        state['pdf_curr'] = str(Path(category) / state['pdf_curr'])

        if category not in state['category']:
            state['category'].append(category)

    except Exception as e:
        print(f"Error moving PDF: {e}")

    return state


# -------------------------------
# ✅ Rename PDF Tool
# -------------------------------
@tool
def rename_pdf(state: AgentState, new_name: str) -> AgentState:
    """
    Renames the currently selected PDF file to the new name.
    """
    try:
        old_path = Path(state['dir']) / state['pdf_curr']
        new_path = old_path.with_name(new_name)
        old_path.rename(new_path)
        state['pdf_curr'] = new_path.name
        print(f"Renamed to: {new_path.name}")

    except Exception as e:
        print(f"Error renaming: {e}")

    return state


# -------------------------------
# ✅ Read PDF (first 10 pages)
# -------------------------------
@tool
def read_pdf(state: AgentState) -> AgentState:
    """
    Reads the first 10 pages of the selected PDF, cleans symbols,
    and stores the result in state['content'].
    """
    text = ""  # ✅ كان ناقص تعريف text
    try:
        file_path = Path(state['dir']) / state['pdf_curr']
        print("read_pdf: ",state['dir'])
        print('read_pdf',file_path)
        with fitz.open(str(file_path)) as doc:
            max_pages = min(10, len(doc))
            for i in range(max_pages):
                page = doc.load_page(i)
                page_text = page.get_text("text")

                cleaned = (
                    page_text.replace("¼", "=")
                             .replace("ﬃ", "ffi")
                             .replace("\x04", "")
                             .replace("\x0f", "")
                             .replace("\x10", "")
                )
                cleaned = re.sub(r"[^\x00-\x7F]+", " ", cleaned)
                cleaned = re.sub(r"\n+", "\n", cleaned)
                cleaned = re.sub(r"\s{2,}", " ", cleaned)

                text += f"\n\n--- Page {i + 1} ---\n\n{cleaned.strip()}"

        state['content'].append(text.strip())

    except Exception as e:
        print(f"Error reading PDF: {e}")

    return state


# -------------------------------
# ✅ update the current pdf 
# -------------------------------

@tool
def update_currpdf(state: AgentState) -> AgentState:
    '''Take the last PDF from pdf_files and move it to pdf_curr to work on it.'''

    if state['pdf_files']:
        pdf_name = state['pdf_files'].pop()
        path=state['dir']
        pdf_path=os.path.join(path,pdf_name)
        print("before:::::",pdf_path)
        state['pdf_curr'] = str(pdf_path)  # نخزن المسار الكامل
        print("after:::::",state['pdf_curr'])
    else:
        state['pdf_curr'] = None
    return state


# ------------------------------------------
# ✅ read image and extract text from it 
# ------------------------------------------
# ---------------->SOON<--------------------
@tool
def extract_text_from_img(state:AgentState)->AgentState:
    """
    this extract text from image in pdf 
    """
    
    with open :
        pass