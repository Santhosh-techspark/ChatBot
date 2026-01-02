# 🤖 ChatBot – Django AI Chatbot with RAG

An intelligent **Django-based AI chatbot** that supports **text conversation and document-based question answering** using **Retrieval-Augmented Generation (RAG)**.  
Users can upload documents (PDF/DOCX/TXT), switch active document context, and ask precise questions without hallucination.

---

## 📌 Project Overview

**Project Name:** ChatBot – Django AI chatbotapp with RAG  
**Developer:** Santhosh  
**Tech Stack:** Django, Python, RAG, Vector Search, HTML/CSS, JavaScript  

This chatbot allows:
- Normal text-based conversations
- Document uploads with contextual understanding
- Switching between multiple uploaded documents
- Accurate answers based only on the active document
- Previous documents remain searchable later

---

## ✨ Features

- ✅ User authentication (Login / Signup / Logout)
- ✅ Text-only chat support
- ✅ Upload documents (PDF, DOCX, TXT)
- ✅ Automatic document chunking & embedding
- ✅ RAG-based document querying
- ✅ Active document context switching
- ✅ No hallucination (answers grounded in documents)
- ✅ Clean UI with modern chat experience
- ✅ Conversation history management

---

## 🧠 How RAG Works Here

1. User uploads a document  
2. Document text is extracted and chunked  
3. Chunks are converted into embeddings  
4. Embeddings are stored in a vector store with `document_id`  
5. When a question is asked:
   - Only the **active document’s chunks** are retrieved
   - The AI responds using retrieved context + chat history

---


## 📂 Project Structure

ChatBot/
│
├── chatbotapp/
│ ├── models.py # Conversation, ChatMessage, Document models
│ ├── views.py # Chat logic, upload handling, RAG integration
│ ├── rag/
│ │ ├── rag_pipeline.py
│ │ ├── loader.py
│ │ ├── vectorstore.py
│ │ └── embeddings.py
│ ├── templates/
│ │ └── chatbotapp/
│ │ └── index.html
│ └── static/
│
├── ChatBot/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── manage.py
├── requirements.txt


---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Santhosh-techspark/ChatBot.git
cd ChatBot

2️⃣ Create Virtual Environment

python -m venv myvenv
myvenv\Scripts\activate   # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the project root:

DJANGO_SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key

5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Start the Server
python manage.py runserver


Open browser:
👉 http://127.0.0.1:8000/

🧪 Code Quality

✔ Pylint score: 9.85 / 10

✔ Only minor, non-functional warnings

✔ Clean architecture and separation of concerns

✔ Production-ready RAG flow powered by Google Gemini LLM ("openai/gpt-oss-120b")

🔐 Security Notes

API keys are loaded via .env

.env is excluded from Git using .gitignore

No sensitive data committed to repository

📈 Future Enhancements

Multi-document comparison mode

Streaming AI responses

PDF preview in chat

Role-based access

Deployment with Docker & AWS

🧑‍💻 Author

Santhosh
Django & AI Developer
GitHub: https://github.com/Santhosh-techspark

⭐ Support

If you like this project, please ⭐ star the repository.
Feel free to fork, improve, and contribute!


---

## ✅ Next Steps for You

1. Save this as `README.md`
2. Run:
   ```bash
   git add README.md
   git commit -m "Add project README"
   git push
