import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from app.models import Tag, MentionsInFile, Excerpt, Version

class TagObject(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node, )

class MentionsInFileObject(SQLAlchemyObjectType):
    class Meta:
        model = MentionsInFile
        interfaces = (graphene.relay.Node, )

class ExcerptObject(SQLAlchemyObjectType):
    class Meta:
        model = Excerpt
        interfaces = (graphene.relay.Node, )

class VersionObject(SQLAlchemyObjectType):
    class Meta:
        model = Version
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_tags = SQLAlchemyConnectionField(TagObject)
    all_mentions_in_files = SQLAlchemyConnectionField(MentionsInFileObject)
    all_excerpts = SQLAlchemyConnectionField(ExcerptObject)
    all_versions = SQLAlchemyConnectionField(VersionObject)

schema = graphene.Schema(query=Query)