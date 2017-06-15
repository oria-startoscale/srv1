from sqlalchemy import Column, String, Text

from strato_common.service_utils.db.mysql.model_base import Base as ModelBase

from srv1.db import common


class MyEndpointModel(ModelBase):
    """My Endpoint data model."""
    __tablename__ = 'my_endpoint'

    id = Column(String(common.UUID_LENGTH), default=common.generate_uuid, primary_key=True)
    name = Column(String(common.STRING_LENGTH), nullable=False)
    status = Column(String(common.STRING_LENGTH), nullable=False)
    result = Column(Text, nullable=True, default=None)
