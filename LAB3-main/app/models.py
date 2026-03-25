from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    username:str = Field(index=True, unique=True)
    email:str = Field(index=True, unique=True)
    password:str

    todos: list['Todo'] = Relationship(back_populates="user")

    def set_password(self, plaintext_password):
        self.password = password_hash.hash(plaintext_password)

    def __str__(self) -> str:
        return f"(User id={self.id}, username={self.username} ,email={self.email})"

class TodoCategory(SQLModel, table=True):
    todo_id: int|None = Field(primary_key=True, foreign_key='todo.id')
    category_id: int|None = Field(primary_key=True, foreign_key='category.id')


class Todo(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id') #set user_id as a foreign key to user.id 
    text: str = Field(max_length=255)
    done: bool = Field(default=False)
    # done: bool = False  # <---- can also be written this way if you prefer a pythonic default

    def toggle(self):
        self.done = not self.done

    user: User = Relationship(back_populates="todos")

    def toggle(self):
        self.done = not self.done
  
    categories: list['Category'] = Relationship(back_populates=("todos"), link_model=TodoCategory)
    
    
class Category(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id') #set user_id as a foreign key to user.id 
    text: str = Field(max_length=255)

    todos: list['Todo'] = Relationship(back_populates=("categories"), link_model=TodoCategory)