from imports import *


class Team(BaseModel):
    name: str = Field(example="Real Madrid", default="Barcelona")
    formation: str = Field(example="4-4-2", default="4-3-3")
