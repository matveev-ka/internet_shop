from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeShop.as_view(), name='home'),
    path('catalog/', BookCatalog.as_view(), name='catalog'),
    path('category/<int:category_id>/', BooksByCategory.as_view(), name='category'),
    path('book/<int:pk>/', view_book, name='view_book'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('author/<str:author>/', BooksByAuthor.as_view(), name='author'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('order_by/<str:order>/', BookOrdering.as_view(), name='book_ordering'),
    path('profile/<int:pk>/', Profile.as_view(), name='profile'),
    path('change_profile/', change_profile, name='change_profile'),
    path('edit_comment/<int:pk>/', edit_comment, name='edit_comment'),
]
