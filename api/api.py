from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse



router = APIRouter()

@router.get('/')
def hello():
    return {'message': 'Hello API!'}

@router.get('/users/{id}/{name}')
def users(id:int, name:str):
    return {'message': 'Hello ID=' + str(id) + ' Name=' + name}

# http://localhost:8000/users/10/somchai


# http://localhost:8000/users/list/?id=10&name=somchai&dept=IT
@router.get('/users/list')
def user_list(id:int=0, name:str='', dept:str=''):
    return {'message': f'ID={id} Name={name} Dept={dept}'}

# http://localhost:8000/login/admin/1234
# http://localhost:8000/login/admin/dadsadsd
@router.get('/login/{user}/{password}')  # Endpoint
def login(user:str,password:str):
    if user=='admin' and password=='1234':
        return {'message': 'Login success'}
    else:
        raise HTTPException(
            status_code=401,  # Unauthorized
            detail='Invalid username or password!'
        )

# http://localhost:8000/text
@router.get('/text', response_class=PlainTextResponse)
def text_response():
    return 'This is a plain text response'


# http://localhost:8000/html
@router.get('/html', response_class=HTMLResponse)
def html_response():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1 style="color:red">HTML Response</h1>
        </body>
        </html>
    """


@router.get('/pdf')
def pdf_response():
    return FileResponse(
        path='report.pdf',
        media_type='application/pdf',
        filename='report.pdf',
    )


from typing import Optional, List
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: float
    type: Optional[str]=None


class OrderItem(BaseModel):
    item: str = Field(..., min_length=3)
    qty: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    amount: float = Field(gt=0)


class Order(BaseModel):
    order_no: str
    cust_name: str
    cust_email: Optional[str]
    items: List[OrderItem]


# http://localhost:8000/product/list
@router.get('/product/list', response_model=List[Product])  
def product_list():
    return [
        Product(name='IPad', price=200),
        Product(name='Macbook', price=25000)
    ]


# http://localhost:8000/product/create
@router.post("/product/create", response_model=Product)
def product_create(product: Product):
    return product



@router.post("/orders/create", response_model=Order)
def order_create(cust_name:str, item:str, qty:int, price:float):
    order = Order(
        order_no='X001', 
        cust_name=cust_name,
        cust_email=cust_name.lower() + '@mail.com',
        items=[
            OrderItem(item=item, qty=qty, unit_price=price, amount=price*qty)
        ]
    )
    return order


