# 📚 PDF Archiver & Organizer Agent

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![LangChain](https://img.shields.io/badge/LangChain-💬-green)
![LLM Powered](https://img.shields.io/badge/LLM-Powered-purple)
![Automation](https://img.shields.io/badge/Automation-🚀-orange)

![Animated Header](https://media.giphy.com/media/26xBukhkvTzZa8lEs/giphy.gif)

## 📖 Overview
The **PDF Archiver & Organizer Agent** is an AI-powered tool that:
- Scans a directory for PDF files 📂
- Reads their content using OCR/text extraction 🧐
- Determines the **title** and **subject category**
- Renames PDFs to match the detected title ✏️
- Creates subject-based folders (e.g., `physics/`, `chemistry/`) 📁
- Moves files into their correct categories 🔄

Powered by **LangGraph**, **LangChain**, and an **LLM** for intelligent document understanding.

---

## 🛠️ Tech Stack

- **LLM** via `langchain_openai`  
- **LangGraph** for workflow orchestration  
- **PyMuPDF / OCR** for reading PDF content  
- **Python 3.10+**
- **Pathlib** for file operations  
- **Docker** (optional for deployment)  

---

## ⚙️ Features
✅ **Automated categorization** by reading document content  
✅ **Intelligent renaming** to match actual document titles  
✅ **Custom folder creation** for new subjects  
✅ **Tool integration** for flexible expansion  
✅ **Zero manual sorting** once set up  

---

## 🧩 Architecture

```mermaid
graph TD
    A[📂 Directory Path] --> B[📋 Collect Files]
    B --> C[🤖 Agent: Determine Title & Subject]
    C --> D[🛠 ToolNode: make_dir / rename_pdf / move]
    D -->|continue| C
    D -->|stop| E[✅ Finished]
