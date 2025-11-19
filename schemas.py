"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
- ContactMessage -> "contactmessage" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (kept for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# QByte IT specific schemas
class BlogPost(BaseModel):
    title: str = Field(..., description="Post title")
    slug: str = Field(..., description="URL-friendly slug")
    excerpt: Optional[str] = Field(None, description="Short summary")
    content: str = Field(..., description="Rich content (Markdown supported)")
    cover_image: Optional[str] = Field(None, description="URL to cover image")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering")
    author: Optional[str] = Field("QByte IT", description="Author name")
    published_at: Optional[datetime] = Field(None, description="Publish datetime; null means draft")
    featured: bool = Field(False, description="Feature on homepage")

class ContactMessage(BaseModel):
    name: str = Field(..., min_length=2, description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    company: Optional[str] = Field(None, description="Company name")
    phone: Optional[str] = Field(None, description="Phone number")
    message: str = Field(..., min_length=10, description="Message body")
    source: Optional[str] = Field("website", description="Lead source")
