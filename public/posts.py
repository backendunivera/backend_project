from fastapi import APIRouter, Response
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from db import make_session
from models.common import ErrorModel, SuccessModel
from models.posts import PostModel, PostCreateModel, PostPatchModel
from orm.entities import posts

posts_router = APIRouter(tags=['posts'], prefix='/api/posts')


@posts_router.get('/')
async def list_all_posts() -> list[PostModel]:
    """
    Получить список всех известных системе постов
    """
    async with make_session() as session:
        query = await session.execute(select(posts).order_by(posts.postid))
        out = []
        for post, in query:
            out.append(post)
    return out


@posts_router.get('/{post_id}')
async def get_post(post_id: int, response: Response) -> PostModel | ErrorModel:
    """
    Получить информацию об одном конкретном посте
    """
    async with make_session() as session:
        query = select(posts).where(posts.postid == post_id)
        selection = await session.execute(query)
        try:
            return selection.scalar_one()
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error="Post doesn't exist")


@posts_router.put('/{post_id}')
async def override_post(post_id: int, post_body: PostCreateModel, response: Response) -> PostModel | ErrorModel:
    """
    Заменить информацию об одном конкретном посте
    """
    async with make_session() as session:
        query = update(posts).where(posts.postid == post_id)\
            .values(**post_body.model_dump())
        await session.execute(query)
        await session.commit()
    return await get_post(post_id, response)


@posts_router.patch('/{post_id}')
async def patch_post(post_id: int, post_body: PostPatchModel, response: Response) -> PostModel | ErrorModel:
    """
    Заменить часть информации об одном конкретном посте
    """
    async with make_session() as session:
        query = update(posts).where(posts.postid == post_id)\
            .values(**post_body.get_values())
        await session.execute(query)
        await session.commit()
    return await get_post(post_id, response)


@posts_router.post('/')
async def create_post(post_model: PostCreateModel) -> PostModel | ErrorModel:
    """
    Добавить носовой пост
    """
    async with make_session() as session:
        post = posts(**post_model.model_dump())
        session.add(post)
        await session.commit()
        return PostModel(post_title=post.post_title,
                        description=post.description,
                        postid=post.postid)


@posts_router.delete('/{post_id}')
async def delete_post(post_id: int, response: Response) -> SuccessModel | ErrorModel:
    """
    Удаляет пост
    """
    async with make_session() as session:
        try:
            query = delete(posts).where(posts.postid == post_id)
            await session.execute(query)
            await session.commit()
            return SuccessModel(success=True)
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error="Post can't de deleted")
