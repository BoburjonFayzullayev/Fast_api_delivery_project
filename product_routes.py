from fastapi import APIRouter, Depends, status
from models import User, Product
from fastapi_jwt_auth import AuthJWT
from database import session, engine
from schemas import ProductModel
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

product_router = APIRouter(
    prefix='/product'
)


@product_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        new_product = Product(
            name=product.name,
            price=product.price
        )

        session.add(new_product)
        session.commit()
        data = {
            'success': True,
            'code': 201,
            'message': "Product created successfully",
            "data": {
                'id': new_product.id,
                'name': new_product.name,
                'price': new_product.price,

            }
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='faqat adminlar product qushishi mumkin')


@product_router.get('/list')
async def list_all_product(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        products = session.query(Product).all()
        response = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
            for product in products
        ]
        return jsonable_encoder(response)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Faqat superadminlar kurishi mukin')


@product_router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_product_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            custom_product = {
                'id': product.id,
                'name': product.name,
                'price': product.price
            }
            return jsonable_encoder(custom_product)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Ushbu {id} ID raqamli product topilmadi")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Siz super admin emassiz. Faqat superadminlar uchun mumkin')


@product_router.delete('/{id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            session.delete(product)
            session.commit()
            data = {
                'success': True,
                'code': 200,
                "message": f"{id} ID lik product o`chirildi",
                'data': None
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Ushbu {id} ID raqamli product topilmadi")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Siz super admin emassiz. Faqat superadminlar o`chirish mumkin')


@product_router.put('/{id}/update', status_code=status.HTTP_200_OK)
async def update_product_id(id: int, update_data: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(product, key, value)
            session.commit()
            data = {
                'success': True,
                'code': 200,
                "message": f"{id} ID lik product yangilandi",
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Ushbu {id} ID raqamli product topilmadi")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Siz super admin emassiz. Faqat superadminlar yangilashi mumkin')


@product_router.patch('/{id}/update', status_code=status.HTTP_200_OK)
async def update_product_id(id: int, update_data: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Enter access token')

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:

            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(product, key, value)

            session.commit()
            data = {
                'success': True,
                'code': 200,
                "message": f"{id} ID lik product yangilandi",
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price
                }
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Ushbu {id} ID raqamli product topilmadi")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Siz super admin emassiz. Faqat superadminlar yangilashi mumkin')
