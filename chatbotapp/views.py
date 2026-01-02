from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from chatbotapp.rag.rag_pipeline import ingest_document, retrieve_context
from .gemini import get_ai_reply
from .models import ChatMessage, Conversation, Document

@login_required
def home(request, conversation_id=None):
    user = request.user

    # ==================================================
    # 1️⃣ Resolve active conversation
    # ==================================================
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
    # 2️⃣ Handle POST (UPLOAD or CHAT)
    # ==================================================
    if request.method == "POST":

        # -------------------------------
        # 📄 DOCUMENT UPLOAD (ACTIVE CONTEXT SWITCH)
        # -------------------------------
        uploaded_file = request.FILES.get("document")
        if uploaded_file:
            # ✅ Save document
            document = Document.objects.create(
                user=user,
                file=uploaded_file
            )

            # ✅ Switch active document (CRITICAL)
            conversation.active_document_id = document.id
            conversation.save(update_fields=["active_document_id"])

            # ✅ Ingest document with document_id
            ingest_document(
                user=user,
                uploaded_file=uploaded_file,
                document_id=document.id
            )

            # ✅ Log upload in chat
            ChatMessage.objects.create(
                conversation=conversation,
                user=user,
                message_type="document",
                uploaded_file_name=uploaded_file.name,
            )

            return redirect(
                "conversation",
                conversation_id=conversation.id
            )

        # -------------------------------
        # 💬 TEXT CHAT (DOCUMENT-AWARE)
        # -------------------------------
        user_msg = request.POST.get("message", "").strip()

        if user_msg:
            # 🔒 Chat history (ignore document rows)
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

            # ✅ Retrieve ONLY active document context
            document_context = ""
            if conversation.active_document_id:
                retrieved_chunks = retrieve_context(
                    question=user_msg,
                    document_id=conversation.active_document_id,
                    top_k=3
                )
                document_context = "\n\n".join(retrieved_chunks)

            # 🤖 AI reply (text-only OR document-based)
            bot_reply = get_ai_reply(
                message=user_msg,
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

            # Auto-title conversation
            if conversation.title == "New chat":
                conversation.title = user_msg[:40]
                conversation.save(update_fields=["title"])

        return redirect(
            "conversation",
            conversation_id=conversation.id
        )

    # ==================================================
    # 3️⃣ Load sidebar + chat history
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


@login_required
def new_chat(request):
    conversation = Conversation.objects.create(
        user=request.user,
        title="New chat"
    )
    return redirect(
        "conversation",
        conversation_id=conversation.id
    )


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
