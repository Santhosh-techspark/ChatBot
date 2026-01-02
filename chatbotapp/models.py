from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# ==============================
# 📄 Document Model
# ==============================
class Document(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    file = models.FileField(upload_to="documents/")
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


# ==============================
# 💬 Conversation Model
# ==============================
class Conversation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    title = models.CharField(max_length=255, default="New chat")

    # ✅ Correct: Active document context (FK, not Integer)
    active_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_in_conversations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==============================
# 🗨️ Chat Message Model
# ==============================
class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ("text", "Text"),
        ("document", "Document"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPES,
        default="text"
    )

    # 🔹 Text chat
    user_message = models.TextField(blank=True)
    bot_reply = models.TextField(blank=True)

    # 🔹 Document upload reference
    uploaded_file_name = models.CharField(
        max_length=255,
        blank=True
    )

    # ✅ CRITICAL: binds chat message → exact document
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.message_type == "document":
            return f"Document: {self.uploaded_file_name}"
        return self.user_message[:30]
