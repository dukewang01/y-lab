"""投诉数据模型"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Optional


class CaseStatus(Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"


class ComplaintSource(Enum):
    PHONE = "phone"
    ONLINE = "online"
    EMAIL = "email"
    IN_PERSON = "in_person"
    SOCIAL_MEDIA = "social_media"
    THIRD_PARTY = "third_party"


@dataclass
class Complaint:
    """投诉工单"""
    case_id: str
    customer_name: str
    description: str
    source: str = "phone"
    status: str = "new"
    category: Optional[str] = None
    subcategory: Optional[str] = None
    approval_level: Optional[str] = None
    handler: Optional[str] = None
    emotion_score: float = 5.0       # 1-10 情绪激烈程度
    risk_score: float = 0.0          # 0-10 风险等级
    repeat_count: int = 0            # 该客户重复投诉次数
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    resolved_at: Optional[str] = None
    notes: list = field(default_factory=list)
