from django.urls import path
from . import views

app_name = "cards"
urlpatterns = [
    path('', views.CardListView.as_view(), name='all'),
    path('card/<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
    path('card/create', views.CardCreateView.as_view(), name='card_create'),
    path('confectioner', views.update_profile, name='confectioner'),
]
