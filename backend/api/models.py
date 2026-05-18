import enum
import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, JSON, Enum, Index, func
from database import Base

class PriorityEnum(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class AssigneeEnum(str, enum.Enum):
    tecnicos = "Técnicos IT"
    comercial = "Gerencia Comercial"
    finanzas = "Gerencia Finanzas"
    rrhh = "Gerencia RRHH"

class ColumnStatusEnum(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    in_review = "in_review"
    done = "done"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=True)
    firstName = Column("first_name", String, nullable=True)
    lastName = Column("last_name", String, nullable=True)
    profileImageUrl = Column("profile_image_url", String, nullable=True)
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "profileImageUrl": self.profileImageUrl
        }

class Session(Base):
    __tablename__ = "sessions"
    sid = Column(String, primary_key=True)
    sess = Column(JSON, nullable=False)
    expire = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("IDX_session_expire", "expire"),
    )

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum(PriorityEnum, name="priority", native_enum=True), default=PriorityEnum.medium, nullable=False)
    assignee = Column(Enum(AssigneeEnum, name="assignee", native_enum=True), nullable=False)
    columnStatus = Column("column_status", Enum(ColumnStatusEnum, name="column_status", native_enum=True), default=ColumnStatusEnum.todo, nullable=False)
    dueDate = Column("due_date", DateTime(timezone=True), nullable=True)
    userId = Column("user_id", String, nullable=False)
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value if hasattr(self.priority, "value") else self.priority,
            "assignee": self.assignee.value if hasattr(self.assignee, "value") else self.assignee,
            "columnStatus": self.columnStatus.value if hasattr(self.columnStatus, "value") else self.columnStatus,
            "dueDate": self.dueDate.isoformat() if self.dueDate else None,
            "userId": self.userId,
            "createdAt": self.createdAt.isoformat() if self.createdAt else None,
            "updatedAt": self.updatedAt.isoformat() if self.updatedAt else None,
        }
