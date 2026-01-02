from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from chatbotapp.rag.rag_pipeline import ingest_document, retrieve_context
from .gemini import get_ai_reply
from .models import ChatMessage, Conversation, Document
import re

def extract_word_limit(message: str):
    """
    Extract word limit from phrases like:
    - '100 words'
    - 'in 100 words'
    - 'of 100 words'
    """
    match = re.search(r"\b(\d+)\s*words\b", message.lower())
    if match:
        return int(match.group(1))
    return None


# ==================================================
# 🧠 HELPER — Resolve which document user means
# ==================================================
def resolve_target_document_id(conversation, user_msg):
    user_msg = user_msg.lower()

    # Get document messages IN ORDER
    document_messages = (
        ChatMessage.objects
        .filter(
            conversation=conversation,
            message_type="document",
            document__isnull=False
        )
        .select_related("document")
        .order_by("created_at")
    )

    if not document_messages.exists():
        return conversation.active_document_id

    documents = [msg.document for msg in document_messages]

    # 1️⃣ Ordinal resolution
    ordinals = {
        "first": 0,
        "second": 1,
        "third": 2,
        "fourth": 3,
    }

    for word, index in ordinals.items():
        if f"{word} document" in user_msg:
            if index < len(documents):
                return documents[index].id

    # 2️⃣ Filename match
    for doc in documents:
        filename = doc.file.name.lower().split("/")[-1]
        name_no_ext = filename.replace(".pdf", "").replace(".docx", "").replace("_", " ")

        if name_no_ext in user_msg:
            return doc.id

        for token in name_no_ext.split():
            if len(token) > 4 and token in user_msg:
                return doc.id

    # 3️⃣ Fallback → active document
    return conversation.active_document.id if conversation.active_document else None


# ==================================================
# 🗑 Delete Conversation
# ==================================================
@login_required
@require_POST
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        user=request.user
    )
    conversation.delete()
    return redirect("home")


# ==================================================
# 🏠 Home View
# ==================================================
@login_required
def home(request, conversation_id=None):
    user = request.user

    # -------------------------------
    # Resolve conversation
    # -------------------------------
    if conversation_id:
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            user=user
        )
    else:
        conversation = (
            Conversation.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )
        if not conversation:
            conversation = Conversation.objects.create(
                user=user,
                title="New chat"
            )

    # ==================================================
    # POST: Upload or Chat
    # ==================================================
    if request.method == "POST":

        # -------------------------------
        # 📄 Document Upload
        # -------------------------------
        uploaded_file = request.FILES.get("document")
        if uploaded_file:
            document = Document.objects.create(
                user=user,
                file=uploaded_file
            )

            # Set active document
            conversation.active_document_id = document.id
            conversation.save(update_fields=["active_document_id"])

            ingest_document(
                user=user,
                uploaded_file=uploaded_file,
                document_id=document.id
            )

            ChatMessage.objects.create(
                conversation=conversation,
                user=user,
                message_type="document",
                uploaded_file_name=uploaded_file.name,
                document=document
            )

            return redirect("conversation", conversation_id=conversation.id)

        # -------------------------------
        # 💬 Text Chat (SMART RAG)
        # -------------------------------
        user_msg = request.POST.get("message", "").strip()

        if user_msg:
            # Chat history (no document rows)
            history_qs = (
                ChatMessage.objects
                .filter(conversation=conversation)
                .exclude(message_type="document")
                .order_by("-created_at")[:8]
            )

            history_text = ""
            for chat in reversed(history_qs):
                history_text += f"User: {chat.user_message}\n"
                history_text += f"Bot: {chat.bot_reply}\n"

            # 🧠 Resolve document explicitly
            target_document_id = resolve_target_document_id(
                conversation,
                user_msg
            )

            document_context = ""
            if target_document_id is not None:
                chunks = retrieve_context(
                    question=user_msg,
                    document_id=target_document_id,
                    top_k=3
                )
                if chunks:
                    document_context = "\n\n".join(chunks)

            word_limit = extract_word_limit(user_msg)

            if word_limit:
                enforced_prompt = (
                    f"{user_msg}\n\n"
                    f"STRICT INSTRUCTION:\n"
                    f"- Write a complete story\n"
                    f"- Use EXACTLY {word_limit} words\n"
                    f"- Do NOT exceed or fall below the limit\n"
                )
            else:
                enforced_prompt = user_msg

            bot_reply = get_ai_reply(
                message=enforced_prompt,
                history_text=history_text,
                document_text=document_context
            )

            ChatMessage.objects.create(
                conversation=conversation,
                user=user,
                message_type="text",
                user_message=user_msg,
                bot_reply=bot_reply
            )

            if conversation.title == "New chat":
                conversation.title = user_msg[:40]
                conversation.save(update_fields=["title"])

        return redirect("conversation", conversation_id=conversation.id)

    # ==================================================
    # Load UI
    # ==================================================
    conversations = (
        Conversation.objects
        .filter(user=user)
        .order_by("-created_at")
    )

    chat_history = (
        ChatMessage.objects
        .filter(conversation=conversation)
        .order_by("created_at")
    )

    return render(
        request,
        "chatbotapp/index.html",
        {
            "chat_history": chat_history,
            "conversations": conversations,
            "active_conversation": conversation,
        }
    )


# ==================================================
# ➕ New Chat
# ==================================================
@login_required
def new_chat(request):
    conversation = Conversation.objects.create(
        user=request.user,
        title="New chat"
    )
    return redirect("conversation", conversation_id=conversation.id)


# ==================================================
# 👤 Signup
# ==================================================
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )
