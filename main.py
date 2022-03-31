from importlib.metadata import requires
from turtle import title
import graphene
from fastapi import FastAPI
from schemas import PostSchema
from starlette.graphql import GraphQLApp
from schemas import PostSchema
from db_conf import db_session

db = db_session.session_factory()
app = FastAPI()

@app.get("/")
def index():
    return "Hi"

class CreateNewPost(graphene.Mutation):
    class Arguements:
        title:graphene.String(required=True)
        content=graphene.String(required=True)
    ok=graphene.Boolean()

    @staticmethod
    def mutate(root,info,title,content):
        post = PostSchema(title=title,content=content)
        db_post = models.Post(title=post.title,content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        ok = True
        return CreateNewPost(ok=ok)
    



class PostMutations(graphene.ObjectType):
    create_new_post=CreateNewPost().Field()

app.add_route("/graphql",GraphQLApp(schemma=graphene.Schema()))

