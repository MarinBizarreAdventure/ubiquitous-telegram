from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.schemas import (
    ChatMessageResponse,
    CreateSessionRequest,
    SendMessageRequest,
    SessionResponse,
    SessionSummaryResponse,
)
from app.container import get_chat_use_case
from app.use_cases.chat import ChatUseCase

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/sessions", response_model=SessionResponse, status_code=201)
def create_session(body: CreateSessionRequest, uc: ChatUseCase = Depends(get_chat_use_case)):
    try:
        session = uc.create_session(body.user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return SessionResponse(id=session.id, user_id=session.user_id, messages=[])


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, uc: ChatUseCase = Depends(get_chat_use_case)):
    try:
        session = uc.get_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    messages = [ChatMessageResponse(role=m.role, content=m.content, timestamp=m.timestamp) for m in session.messages]
    return SessionResponse(id=session.id, user_id=session.user_id, messages=messages)


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
def send_message(session_id: str, body: SendMessageRequest, uc: ChatUseCase = Depends(get_chat_use_case)):
    try:
        message = uc.send_message(session_id, body.content)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ChatMessageResponse(role=message.role, content=message.content, timestamp=message.timestamp)


@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: str, uc: ChatUseCase = Depends(get_chat_use_case)):
    try:
        uc.delete_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/{user_id}/sessions", response_model=list[SessionSummaryResponse])
def list_user_sessions(user_id: str, uc: ChatUseCase = Depends(get_chat_use_case)):
    sessions = uc.get_sessions_by_user(user_id)
    return [
        SessionSummaryResponse(id=s.id, user_id=s.user_id, message_count=len(s.messages))
        for s in sessions
    ]
