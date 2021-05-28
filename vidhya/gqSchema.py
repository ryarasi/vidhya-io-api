import graphene
from .gqQueries import Query
from .gqMutations import Mutation


schema = graphene.Schema(query=Query, mutation=Mutation)
