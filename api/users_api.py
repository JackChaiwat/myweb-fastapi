from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Product, Category
from sqlalchemy import or_, func
from fastapi import Depends
from fastapi.security import HTTPBearer
from jwt_auth import verify_token

router = APIRouter()
security = HTTPBearer()

ENDPOINT = '/api/v1'

# http://localhost:8000/api/v1/users
@router.get(ENDPOINT + "/users")
def user_list(user=Depends(verify_token)):
    return {
        "message": "List of users"
    }


@router.get("/item/{id}")
def get_item(id: int):
    if id <= 0:
        raise HTTPException(status_code=400, detail="Invalid id")
    
    salary = 1000000
    try:
        hr_salary = 0  # ดึงจาก database แล้วได้ 0
        x = salary / hr_salary
    except Exception as e:
        raise HTTPException(status_code=500, detail='เกิดความผิดพลาด โปรดติดต่อทีม')
    return {"id": id}


# localhost:8000/products/list
@router.get('/products/list')
def product_list():
    db = SessionLocal()
    products = db.query(Product).order_by(Product.price.desc()).all()
    # products = db.query(Product)\
    #     .filter(Product.price > 200, Product.category_id == 4)\
    #     .all()
    # products = db.query(Product)\
    #     .filter( or_(Product.price < 200, Product.price > 500) )\
    #     .all()
    for p in products:
        print(p.name, p.price)

    total_price = db.query(func.sum(Product.price)).scalar()
    print(total_price)

    products = db.query(Product)\
        .join(Category)\
        .filter(Category.name == 'นิยาย')\
        .all()
    
    # โจทย์: ต้องการนับสินค้าตามหมวดหมู่
    # หมวดหมู่ 4 มีสินค้า 2 ตัว
    # หมวดหมู่ 1 มีสินค้า 1 ตัว
    # หมวดหมู่ 2 มีสินค้า 1 ตัว

    count_category = db.query(Category.name, func.count(Product.id))\
        .join(Category)\
        .group_by(Category.name)\
        .order_by(func.count(Product.id).desc())\
        .limit(5)\
        .all()
    
    print(count_category)

    db.close()
    return products
    # return total_price

