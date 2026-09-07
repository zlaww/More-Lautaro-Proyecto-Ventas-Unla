from datetime import date, time
from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    precio: float

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True

class VentaBase(BaseModel):
    fecha: date
    hora: time
    id_producto: int
    cantidad: int

class VentaCreate(VentaBase):
    pass

class VentaResponse(BaseModel):
    id: int
    fecha: date
    hora: time
    producto: Producto
    cantidad: int
    precio_total: float

    class Config:
        from_attributes = True