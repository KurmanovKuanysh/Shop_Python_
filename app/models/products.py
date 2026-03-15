from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    cost: float
    remains: int