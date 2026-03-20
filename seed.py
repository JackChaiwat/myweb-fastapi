from database import SessionLocal, engine, Base
from models import Category, User, Product, Customer, Order, OrderDetail

db = SessionLocal()

def reset_database():
    print("Droping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

def run_seed():
    db.add_all([
        Category(name='นิยาย'),
        Category(name='การ์ตูน'),
        Category(name='เกษตร'),
        Category(name='คอมพิวเตอร์'),
    ])
    db.commit()

    db.add_all([
        Product(name='เดอะลอร์ดออฟเดอะริงส์', price=100, category_id=1),
        Product(name='ซึบาสะ', price=200, category_id=2),
        Product(name='สร้าง Frontend ด้วย Next.js', price=300, category_id=4),
        Product(name='เรียนรู้การทำ API ด้วย FastAPI', price=400, category_id=4),
    ])
    db.commit()

    db.add_all([
        User(name='admin'),
        User(name='user1'),
    ])
    db.commit()

    db.add_all([
        Customer(name='ร้านต้นอ้อ'),
        Customer(name='คุณสมชาย'),
        Customer(name='คุณสุพิชยา'),
    ])
    db.commit()

    db.add_all([
        Order(
            order_no='X001',
            user_id=1,
            customer_id=1,
            amount_untaxed=93.46,
            amount_tax=6.54,
            amount_total=100,
        )
    ])
    db.commit()

    db.add_all([
        OrderDetail(
            order_id=1,
            product_id=1,
            qty=1,
            price=100,
            amount=100,
        )
    ])
    db.commit()


if __name__ == '__main__':
    reset_database()
    run_seed()
