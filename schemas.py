from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_model = True
        schema_extra = {
            'example': {
                'username': "Bobjon",
                'email': "Boburjon@gmail.com",
                'password': "parol12345",
                'is_active': True,
                'is_staff': False

            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'eba52c9cc05ee42ebcf9141f0cb6f3b8ac893a17af9ccd19c657c82b1cb1371f'


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_statutes: Optional[str] = "PENDING"
    user_id: Optional[int]
    product_id: int

    class Config:
        orm_model = True
        schema_extra = {
            'example': {
                'quantity': 2
            }
        }


class OrderStatusModel(BaseModel):
    order_statutes: Optional[str] = "PENDING"

    class Config:
        orm_model = True
        schema_extra = {
            'example': {
                'order_statuses': "PENDING",
            }
        }


class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    price: int

    class Config:
        orm_model = True
        schema_extra = {
            'example': {
                'name': "Palov",
                'price': 25000
            }
        }
