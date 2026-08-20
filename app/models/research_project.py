from datetime import timezone, datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    owner = relationship("User", back_populates="owned_projects")
    members = relationship("ResearchMember", back_populates="project")
    tasks = relationship("ResearchTask", back_populates="project")

class ResearchMember(Base):
    __tablename__ = "research_members"

    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(Enum("OWNER", "MEMBER"), nullable=False)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    project = relationship("ResearchProject", back_populates="members")
    user = relationship("User", back_populates="memberships")