from pydantic import BaseModel, ConfigDict


class UniversityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    state: str
    institution_type: str
