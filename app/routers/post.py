from app import oauth2
from ..  import model , schema  , utils , oauth2
from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func


router=APIRouter(
     prefix="/posts",
     tags=["Posts"]
)







@router.get("/" ,response_model=List[schema.PostOut])
async def posts(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user) , Limit:int=10, Skip:int=0 , search:Optional[str]=""):

   #posts=db.query(model.Post).filter(model.Post.title.contains(search)).limit(Limit).offset(Skip).all()
  
   
   posts=db.query(model.Post,func.count(model.Vote.post_id).label("votes")).join(model.Vote , model.Vote.post_id ==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(Limit).offset(Skip).all()
   
   return posts

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schema.Post)
async def create_post(post:schema.PostCreate, db:Session=Depends(get_db), get_current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title, post.content, post.publish))#why not to use raw string? It makes vulnerable to SQL injection
    #new_post=cursor.fetchone()
    #conn.commit()
    
   new_post=model.Post(owner_id=get_current_user.id ,**post.dict())#**post.dict() is used to unpack the dictionary.
   db.add(new_post)
   db.commit()
   db.refresh(new_post)

   return new_post

@router.get("/{id}",response_model=schema.PostOut)
def get_post(id:int, respose:Response, db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    
    #cursor.execute("""SELECT * FROM posts WHERE id= %s""" , str(id))
    #post=cursor.fetchone()
    post=db.query(model.Post,func.count(model.Vote.post_id).label("votes")).join(model.Vote , model.Vote.post_id ==model.Post.id,isouter=True).group_by(model.Post.id).first()
   
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
        #respose.status_code=status.HTTP_404_NOT_FOUND
        #return {"message":f"post  with id {id} not found"} 
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int , db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
            #cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", str(id))
            #deleted_post=cursor.fetchone()
            #conn.commit()



            deleted_post=db.query(model.Post).filter(model.Post.id==id)
            delete_post=deleted_post.first()
            if delete_post.owner_id != get_current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


            if deleted_post == None:
                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
            
            deleted_post.delete(synchronize_session=False)
            db.commit()

            return deleted_post


@router.put("/{id}",response_model=schema.Post)
def update_post(id:int, post:schema.PostCreate , db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.publish, str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    updated_post=db.query(model.Post).filter(model.Post.id==id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    updated_post.update(post.dict(), synchronize_session=False) 
    db.commit()
    return updated_post.first()