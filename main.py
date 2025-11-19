import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import db, create_document, get_documents
from schemas import BlogPost, ContactMessage

app = FastAPI(title="QByte IT API", description="Backend for QByte IT website", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "QByte IT API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Basic schema endpoint for the CMS viewer
@app.get("/schema")
def get_schema():
    return {
        "collections": [
            {
                "name": "blogpost",
                "fields": list(BlogPost.model_fields.keys()),
            },
            {
                "name": "contactmessage",
                "fields": list(ContactMessage.model_fields.keys()),
            },
        ]
    }

# Blog endpoints
@app.get("/api/blogs", response_model=List[BlogPost])
def list_blogs(tag: Optional[str] = None, featured: Optional[bool] = None, limit: int = 20):
    filter_dict = {}
    if tag:
        filter_dict["tags"] = {"$in": [tag]}
    if featured is not None:
        filter_dict["featured"] = featured
    docs = get_documents("blogpost", filter_dict, limit)
    # Convert Mongo docs to Pydantic-compatible dicts
    cleaned = []
    for d in docs:
        d.pop("_id", None)
        cleaned.append(BlogPost(**d))
    return cleaned

@app.post("/api/contact")
def create_contact(msg: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", msg)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
