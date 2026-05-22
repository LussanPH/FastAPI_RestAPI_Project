from pydantic import BaseModel
from typing import Optional

class UsuariosSchemas(BaseModel):
    nome : str
    email : str
    senha : str
    ativo : Optional[bool]
    admin : Optional[bool]