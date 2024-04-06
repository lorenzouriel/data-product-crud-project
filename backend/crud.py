from sqlalchemy.orm import Session
from schemas import ProductUpdate, ProductCreate
from models import ProductModel

# SELECT *
def get_products(db: Session):
    """
    funcao que retorna todos os elementos
    """
    return db.query(ProductModel).all()

# SELECT with WHERE
def get_product(db: Session, product_id: int):
    """
    funcao que recebe um id e retorna somente ele
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

# INSERT INTO
def create_product(db: Session, product: ProductCreate):
    # Transformar a minha view para ORM
    db_product = ProductModel(**product.model_dump())
    # Adicionar na tabelas
    db.add(db_product)
    # Commitar na tabela
    db.commit()
    # Refresh do banco
    db.refresh(db_product)
    # Retornar dados
    return db_product

# DELETE with WHERE
def delete_product(db: Session, product_id: int):
    # Busca o db Product seleciona o produto
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    # Deleta o produto
    db.delete(db_product)
    # Commita no banco
    db.commit()
    # Retorne o valor
    return db_product

# UPDATE
def update_product(db: Session, product_id: int, product: ProductUpdate):
    # Busca o db Product seleciona o produto
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None:
        return None

    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.price is not None:
        db_product.price = product.price
    if product.category is not None:
        db_product.category = product.category
    if product.email_partner is not None:
        db_product.email_partner = product.email_partner

    db.commit()
    db.refresh(db_product)
    return db_product