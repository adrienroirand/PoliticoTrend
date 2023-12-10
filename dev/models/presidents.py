from pydantic import BaseModel
class President(BaseModel):
    name: str
    surname: str
    country: str
    years_in_office: int
    def full_name(self) -> str:
        return f"{self.name} {self.surname}"
    party: str

class Party(BaseModel):
    name: str
    founded: int
    ideology: int

