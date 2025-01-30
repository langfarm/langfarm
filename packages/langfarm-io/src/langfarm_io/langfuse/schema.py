import datetime as dt

from sqlalchemy import DateTime, Numeric, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.types import TypeDecorator


class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(dt.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=dt.timezone.utc).astimezone()
        return value


class TableBase(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ApiKey(TableBase):
    __tablename__ = "api_keys"
    __table_args__ = (
        UniqueConstraint("hashed_secret_key", name="uq_hashed_secret_key"),
        UniqueConstraint("fast_hashed_secret_key", name="uq_fast_hashed_secret_key"),
        UniqueConstraint("public_key", name="uq_public_key"),
    )

    id = mapped_column(Text, primary_key=True)
    created_at = mapped_column(TZDateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    note = mapped_column(Text)
    public_key = mapped_column(Text, nullable=False, index=True)
    hashed_secret_key = mapped_column(Text, nullable=False, index=True)
    display_secret_key = mapped_column(Text, nullable=False)
    last_used_at = mapped_column(TZDateTime)
    expires_at = mapped_column(TZDateTime)
    project_id = mapped_column(Text, nullable=False, index=True)
    fast_hashed_secret_key = mapped_column(Text, index=True)


class Model(TableBase):
    __tablename__ = "models"
    __table_args__ = (
        UniqueConstraint(
            "project_id", "model_name", "start_date", "unit", name="models_project_id_model_name_start_date_unit_key"
        ),
    )

    id = mapped_column(Text, primary_key=True)
    created_at = mapped_column(TZDateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at = mapped_column(TZDateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    project_id = mapped_column(Text)
    model_name = mapped_column(Text, nullable=False, index=True)
    match_pattern = mapped_column(Text, nullable=False)
    start_date = mapped_column(TZDateTime)
    input_price = mapped_column(Numeric)
    output_price = mapped_column(Numeric)
    total_price = mapped_column(Numeric)
    unit = mapped_column(Text)
    tokenizer_config = mapped_column(Text)
    tokenizer_id = mapped_column(Text)
