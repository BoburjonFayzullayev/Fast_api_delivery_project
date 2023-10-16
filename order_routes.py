from fastapi import APIRouter, Depends, status
from models import User, Product, Order
from fastapi_jwt_auth import AuthJWT
from database import session, engine
from schemas import OrderModel, OrderStatusModel
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

order_router = APIRouter(
    prefix='/order'
)


@order_router.get('/')
async def welcome_page(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    return {
        'message': " bu order router sahifa"
    }


@order_router.post('/make')
async def order_make(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        quantity=order.quantity,
        product_id=order.product_id,
    )
    new_order.users = user
    session.add(new_order)
    session.commit()

    data = {
        "success": True,
        "code": 200,
        "message": "Order created successfauly",
        "data": {
            "id": new_order.id,
            "product": {
                'id': new_order.products.id,
                'name': new_order.products.name,
                'price': new_order.products.price
            },
            "quantity": new_order.quantity,
            "order_statuses": new_order.order_statutes.value,
            "total_price": new_order.quantity * new_order.products.price
        }
    }

    respone = data

    return jsonable_encoder(respone)


@order_router.get('/list')
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        orders = session.query(Order).all()
        custom_data = [
            {
                "id": order.id,
                "user": {
                    "id": order.users.id,
                    "username": order.users.username,
                    "email": order.users.email
                },
                "product": {
                    'id': order.products.id,
                    'name': order.products.name,
                    'price': order.products.price
                         },
                "quantity": order.quantity,
                "order_statuses": order.order_statutes.value,
                "total_price": order.quantity * order.products.price
            }
            for order in orders
        ]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Siz super admin emassiz. Faqat superadminlar uchun mumkin')


@order_router.get('/{id}')
async def get_order_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        if order:
            custom_order = {
                "id": order.id,
                "user": {
                    "id": order.users.id,
                    "username": order.users.username,
                    "email": order.users.email
                },
                "product": {
                    'id': order.products.id,
                    'name': order.products.name,
                    'price': order.products.price
                         },
                "quantity": order.quantity,
                "order_statuses": order.order_statutes.value,
                "total_price": order.quantity * order.products.price
            }
            return jsonable_encoder(custom_order)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ushbu {id} raqamli order topilmadi")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Siz super admin emassiz. Faqat superadminlar uchun mumkin')


@order_router.get('/user/order/{id}', status_code=status.HTTP_200_OK)
async def get_user_order_by_id(id: int, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    username = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == username).first()
    order = session.query(Order).filter(Order.id == id, Order.users == current_user).first()

    # orders = current_user.orders # bu usulni yuqoridagi order bilan soddalashtirib oldik
    # for order in orders:
    #     if order.id == id:
    if order:
        order_data = {
            "id": order.id,
            "user": {
                "id": order.users.id,
                "username": order.users.username,
                "email": order.users.email
            },
            "product": {
                'id': order.products.id,
                'name': order.products.name,
                'price': order.products.price
            },
            "quantity": order.quantity,
            "order_statuses": order.order_statutes.value,
            "total_price": order.quantity * order.products.price

        }
        return jsonable_encoder(order_data)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Bunday {id} ID lik order topilmadi')

@order_router.put('/{id}/update', status_code=status.HTTP_200_OK)
async def update_order_id(id: int, order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token yaroqsiz')

    username = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == username).first()

    order_to_update = session.query(Order).filter(Order.id == id).first()
    if order_to_update.users != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Kechirasiz, Siz boshqa foydalanuvchilarni buyurtmalarini o`zgartira olmaysiz')

    order_to_update.quantity =order.quantity
    order_to_update.product_id = order.product_id
    session.commit()

    custom_response = {
        'success': True,
        'code': 200,
        'message': "Sizning buyurtmangiz muvaffaqiyatli o`zgartirildi",
        'data': {
            "id": order.id,
            "quantity": order.quantity,
            "product": order.product_id,
            "order_statusses": order.order_statutes
                }
    }
    return jsonable_encoder(custom_response)

@order_router.patch('/{id}/update-status', status_code=status.HTTP_200_OK)
async def order_update_status(id: int, order: OrderStatusModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token yaroqsiz')

    username = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == username).first()

    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()
        order_to_update.order_statutes = order.order_statutes
        session.commit()

        custom_respone = {
            "success": True,
            "code": 200,
            "message": "Order status muvaffaqiyatli o`gartirildi",
            "data": {
                'id': order_to_update.id,
                'order_statuses': order_to_update.order_statutes
            }
        }
        return jsonable_encoder(custom_respone)
@order_router.delete('/{id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token yaroqsiz')

    username = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == username).first()

    order = session.query(Order).filter(Order.id == id).first()
    if order.users != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Kechirasiz, Siz boshqa foydalanuvchilarni buyurtmalarini o`chira olmaysiz')

    if order.order_statutes != 'PENDING':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Kechirasiz, Siz yo`lga chiqgan va yetkazib berilgan buyurtmalarni o`chira olmaysiz')

    session.delete(order)
    session.commit()
    custom_respone = {
        "success": True,
        "code": 200,
        "message": "Order status muvaffaqiyatli o`gartirildi",
        "data": None
    }
    return jsonable_encoder(custom_respone)