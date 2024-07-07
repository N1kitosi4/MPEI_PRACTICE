from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app import schemas, models, oauth2
from app.database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              offset: int = 0,
              search: str | None = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post_by_id(post_id: int,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).
            filter(models.Post.id == post_id).first())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} was not found")
    return post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    upd_posts = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = upd_posts.first()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} was not found")
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    upd_posts.update(post.dict())
    db.commit()
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    del_posts = db.query(models.Post).filter(models.Post.id == post_id)
    deleted_post = del_posts.first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} was not found")
    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    del_posts.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
