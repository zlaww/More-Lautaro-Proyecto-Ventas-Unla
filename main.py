from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/productos", response_model=schemas.Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = models.Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@app.get("/productos", response_model=List[schemas.Producto])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

@app.get("/productos/{id}", response_model=schemas.Producto)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{id}", response_model=schemas.Producto)
def actualizar_producto(id: int, datos: schemas.ProductoCreate, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for clave, valor in datos.model_dump().items():
        setattr(producto, clave, valor)
    db.commit()
    db.refresh(producto)
    return producto

@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()

@app.post("/ventas", response_model=schemas.VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == venta.id_producto).first()
    if not producto:
        raise HTTPException(status_code=400, detail="El producto especificado no existe")
    
    precio_calculado = producto.precio * venta.cantidad
    nueva_venta = models.Venta(
        fecha=venta.fecha,
        hora=venta.hora,
        id_producto=venta.id_producto,
        cantidad=venta.cantidad,
        precio_total=precio_calculado
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta

@app.get("/ventas", response_model=List[schemas.VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()

@app.get("/ventas/{id}", response_model=schemas.VentaResponse)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@app.put("/ventas/{id}", response_model=schemas.VentaResponse)
def actualizar_venta(id: int, datos: schemas.VentaCreate, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    producto = db.query(models.Producto).filter(models.Producto.id == datos.id_producto).first()
    if not producto:
        raise HTTPException(status_code=400, detail="El producto especificado no existe")
    
    venta.fecha = datos.fecha
    venta.hora = datos.hora
    venta.id_producto = datos.id_producto
    venta.cantidad = datos.cantidad
    venta.precio_total = producto.precio * datos.cantidad

    db.commit()
    db.refresh(venta)
    return venta

@app.delete("/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    db.delete(venta)
    db.commit()