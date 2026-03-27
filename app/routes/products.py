from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.cache import delete_product_cache, get_product_cache, set_product_cache
from app.db import get_db_read, get_db_write
from app.models import Product
from app.schemas import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db_write)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return ProductResponse.model_validate(db_product)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db_read)):
    cached_product = get_product_cache(product_id)
    if cached_product:
        print(f"cache hit for product {product_id}")
        return cached_product

    print(f"cache miss for product {product_id}")
    print(f"reading product {product_id} from replica")

    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    response = ProductResponse.model_validate(product)
    set_product_cache(response)

    return response


@router.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db_read)):
    print("reading product list from replica")
    statement = select(Product)
    products = db.execute(statement).scalars().all()
    return [ProductResponse.model_validate(product) for product in products]


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db_write),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_product.name
    product.description = updated_product.description
    product.price = updated_product.price
    product.stock = updated_product.stock
    product.category = updated_product.category

    db.commit()
    db.refresh(product)

    delete_product_cache(product_id)

    return ProductResponse.model_validate(product)


@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: Session = Depends(get_db_write)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    response = ProductResponse.model_validate(product)

    db.delete(product)
    db.commit()

    delete_product_cache(product_id)

    return response
