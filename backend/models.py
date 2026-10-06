from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime, timedelta
import bcrypt

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    name = Column(String)
    avatar = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime, nullable=True)
    language = Column(String, default="en")  # Tanlagan tili
    daily_requests = Column(Integer, default=0)
    last_request_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    queries = relationship("Query", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password: str):
        """Parolni shifrlash"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify_password(self, password: str) -> bool:
        """Parolni tekshirish"""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def can_make_request(self) -> bool:
        """Bugungi uchun so'rov qilish imkoniyatini tekshirish"""
        if self.is_admin:
            return True  # Admin cheksiz
        
        if self.is_premium:
            return True  # Premium cheksiz
        
        # Bugunning sanasini tekshir
        today = datetime.utcnow().date()
        last_request = self.last_request_date.date() if self.last_request_date else None
        
        if last_request != today:
            self.daily_requests = 0
        
        if self.daily_requests >= 10:  # 10 so'rov limitasi
            return False
        
        return True
    
    def increment_request_count(self):
        """So'rovlar sonini oshirish"""
        today = datetime.utcnow().date()
        last_request = self.last_request_date.date() if self.last_request_date else None
        
        if last_request != today:
            self.daily_requests = 0
            self.last_request_date = datetime.utcnow()
        
        self.daily_requests += 1


class Query(Base):
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    query_text = Column(Text)  # User yozgan so'rov
    response_data = Column(JSON)  # AI javob (full data)
    language = Column(String, default="en")  # Query tilida saqlash
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="queries")


class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)  # "delete_user", "activate_premium" kabi
    target_user_id = Column(Integer, nullable=True)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
