from pydantic import BaseModel


class SummaryBase(BaseModel):
    content: str


class SummaryCreateDB(SummaryBase):
    article_id: int


class SummaryResponse(SummaryBase):
    id: int


class SummaryUpdateDB(BaseModel):
    pass
