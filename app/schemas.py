import graphene
from app.models import Tag, MentionsInFile, Excerpt, Version
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

# ==========================================
# Filters
# ==========================================

class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = {
            'tag_name': [...]
        }

class VersionFilter(FilterSet):
    class Meta:
        model = Version
        fields = {
            'version_name': [...]
        }

class MentionsInFileFilter(FilterSet):
    class Meta:
        model = MentionsInFile
        fields = {
            'file_name': [...]
        }

class CustomField(FilterableConnectionField):
    filters = {
        Tag: TagFilter(),
        Version: VersionFilter(),
        MentionsInFile: MentionsInFileFilter()
    }

# ==========================================
# Nodes
# ==========================================

class MentionsInFileNode(SQLAlchemyObjectType):
    class Meta:
        model = MentionsInFile
        interfaces = (graphene.relay.Node, )
        connection_field_factory = CustomField.factory

class ExcerptNode(SQLAlchemyObjectType):
    class Meta:
        model = Excerpt
        interfaces = (graphene.relay.Node, )
        connection_field_factory = CustomField.factory

class VersionNode(SQLAlchemyObjectType):
    class Meta:
        model = Version
        interfaces = (graphene.relay.Node, )
        connection_field_factory = CustomField.factory

class TagNode(SQLAlchemyObjectType):
    class Meta:
        model = Tag
        interfaces = (graphene.relay.Node, )
        connection_field_factory = CustomField.factory

# ==========================================
# Connections
# ==========================================

class TagConnection(graphene.Connection):
    class Meta:
        node = TagNode

class MentionsInFileConnection(graphene.Connection):
    class Meta:
        node = MentionsInFileNode

class ExcerptConnection(graphene.Connection):
    class Meta:
        node = ExcerptNode

class VersionConnection(graphene.Connection):
    class Meta:
        node = VersionNode

# ==========================================
# Query
# ==========================================

class Query(graphene.ObjectType):
    all_tags = CustomField(TagConnection)
    all_mentions_in_files = CustomField(MentionsInFileConnection)
    all_excerpts = CustomField(ExcerptConnection)
    all_versions = CustomField(VersionConnection)

schema = graphene.Schema(query=Query)