# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TEXT

Base = declarative_base()
metadata = Base.metadata


class Complexity(Base):
    __tablename__ = 'complexity'

    id = Column(Integer, primary_key=True)
    complexity = Column(String(45), nullable=False)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    item_type = Column(ForeignKey(u'item_type.id'), primary_key=True, nullable=False, index=True)

    item_type1 = relationship(u'ItemType')

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(45), nullable=False)
    login = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    role = Column(ForeignKey(u'user_role.id'), primary_key=True, nullable=False, index=True)

    user_role = relationship(u'UserRole')



class ItemType(Base):
    __tablename__ = 'item_type'

    id = Column(Integer, primary_key=True)
    type = Column(String(45), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(45), nullable=False)
    rating = Column(String(45))
    author = Column(ForeignKey(u'user.id'), primary_key=True, nullable=False, index=True)
    complexity = Column(ForeignKey(u'complexity.id'), primary_key=True, nullable=False, index=True)
    description = Column(String(45), nullable=False)

    user = relationship(u'User')
    complexity1 = relationship(u'Complexity')


class RecipeItem(Base):
    __tablename__ = 'recipe_item'
    
    id = Column(Integer, primary_key=True, nullable=False)

    recipe_id = Column(ForeignKey(u'recipe.id'), primary_key=True, index=True)
    item_id = Column(ForeignKey(u'item.id'), index=True)
    ingredient = Column(String(45), nullable=False)

    item = relationship(u'Item')


class RecipeCategory(Base):
    __tablename__ = 'recipe_category'

    id = Column(Integer, primary_key=True)
    category = Column(String(45), nullable=False)

    recipes = relationship(u'Recipe', secondary='recipe_category_has_recipe')


t_recipe_category_has_recipe = Table(
    'recipe_category_has_recipe', metadata,
    Column('category_id', ForeignKey(u'recipe_category.id'), primary_key=True, nullable=False, index=True),
    Column('recipe_id', ForeignKey(u'recipe.id'), primary_key=True, nullable=False, index=True)
)


class Step(Base):
    __tablename__ = 'step'

    id = Column(Integer, primary_key=True, nullable=False)
    recipe_id = Column(ForeignKey(u'recipe.id'), primary_key=True, nullable=False, index=True)
    description = Column(TEXT(charset='latin1'), nullable=False)

    recipe = relationship(u'Recipe')


class UserRole(Base):
    __tablename__ = 'user_role'

    id = Column(Integer, primary_key=True)
    role = Column(String(45), nullable=False)
