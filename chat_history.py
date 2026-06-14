from database import SessionLocal
from models import Chat, ChatMessage


# Create a new chat
def create_chat(title="New Chat"):

    db = SessionLocal()

    chat = Chat(title=title)

    db.add(chat)
    db.commit()
    db.refresh(chat)

    chat_id = chat.id

    db.close()

    return chat_id


# Get all chats
def get_chats():

    db = SessionLocal()

    chats = db.query(Chat).order_by(
        Chat.id.desc()
    ).all()

    db.close()

    return chats


# Save a message
def save_message(chat_id, role, content):

    db = SessionLocal()

    message = ChatMessage(
        chat_id=chat_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()

    db.close()


# Get messages of one chat
def get_messages(chat_id):

    db = SessionLocal()

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.id)
        .all()
    )

    db.close()

    return messages


# Update chat title
def update_chat_title(chat_id, title):

    db = SessionLocal()

    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id)
        .first()
    )

    if chat:
        chat.title = title
        db.commit()

    db.close()


# Delete chat and its messages
def delete_chat(chat_id):

    db = SessionLocal()

    db.query(ChatMessage).filter(
        ChatMessage.chat_id == chat_id
    ).delete()

    db.query(Chat).filter(
        Chat.id == chat_id
    ).delete()

    db.commit()

    db.close()