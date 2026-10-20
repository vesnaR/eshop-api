from pydantic import BaseModel, ConfigDict


class CategorySummary(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)