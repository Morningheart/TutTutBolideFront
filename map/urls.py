from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("graphql", GraphQLView.as_view(graphiql=True)),
]