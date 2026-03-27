from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db import get_db_read, get_db_write
from app.models import Product

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/sync-replica")
def sync_replica(
    db_write: Session = Depends(get_db_write),
    db_read: Session = Depends(get_db_read),
):
    primary_products = db_write.execute(select(Product)).scalars().all()

    db_read.execute(delete(Product))
    db_read.commit()

    for product in primary_products:
        replica_product = Product(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=product.category,
        )
        db_read.add(replica_product)

    db_read.commit()

    return {
        "status": "ok",
        "synced_products": len(primary_products),
    }
