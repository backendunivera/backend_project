from typing import Optional

from pydantic import BaseModel, Field


class PostCreateModel(BaseModel):
    post_title: str
    description: str


class PostModel(PostCreateModel):
    postid: int


class PostPatchModel(BaseModel):
    post_title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)

    def get_values(self):
        return dict((k, v) for k, v in self.model_dump().items() if v is not None)
