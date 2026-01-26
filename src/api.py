from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import StreamingResponse
import json

from src.rag import get_query_engine

app = FastAPI(title="Medical Retrieval Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Initialize engine lazily
query_engine = None
def get_engine():
    global query_engine
    if query_engine is None:
        query_engine = get_query_engine()
    return query_engine

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that returns a streaming response.
    """
    try:
        # Get the last user message
        user_message = request.messages[-1].content
        
        engine = get_engine()
        streaming_response = engine.query(user_message)
        
        async def event_generator():
            # 1. Yield sources first (as a special event or just text? 
            # Ideally structured, but for simple text stream let's prepend sources or yield distinct chunks)
            # For this 'simple' custom implementation, we'll stream text. 
            # If we want sources, we might want to send a JSON structure per line.
            
            # Let's send sources as a JSON object in the first chunk, or appended at end?
            # Standard pattern: Text stream. Sources usually come with the retrieval.
            
            sources_list = []
            if streaming_response.source_nodes:
                for i, node in enumerate(streaming_response.source_nodes):
                    metadata = node.metadata
                    sources_list.append({
                        "id": i+1,
                        "file_name": metadata.get('file_name', 'Unknown File'),
                        "page_label": metadata.get('page_label', '?'),
                        "snippet": node.node.get_content()[:200]
                    })
            
            # Yield sources as a special JSON line (optional)
            # For now, let's just allow the client to handle it. 
            # But wait, Vercel AI SDK expects text delta. 
            # We can use custom data protocol. 
            # Let's stick to simple text stream for the answer, and maybe append formatted sources at the end?
            # Or better: Standard SSE.
            
            # Send citations header
            if sources_list:
                citations_str = "\n\n**Sources:**\n"
                for s in sources_list:
                    citations_str += f"{s['id']}. *{s['file_name']}* (Page {s['page_label']})\n"
                # We yield this at the END or BEGINNING? Users prefer answer first.
                pass 
                
            # Stream the response text
            for text in streaming_response.response_gen:
                yield text

            # Append sources at the end
            if sources_list:
                yield "\n\n**Sources:**\n"
                for s in sources_list:
                     yield f"{s['id']}. *{s['file_name']}* (Page {s['page_label']})\n> {s['snippet']}...\n\n"

        return StreamingResponse(event_generator(), media_type="text/plain")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
