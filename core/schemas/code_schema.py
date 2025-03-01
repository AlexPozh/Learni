
from pydantic import BaseModel


class EmailScheme(BaseModel):
    email: str

class CodeScheme(EmailScheme):
    code: str