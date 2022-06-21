from django.urls import path
from app01 import views

urlpatterns = [
    path('add_book/', views.add_book),
    path('book_list/', views.book_list),
    path('edit_book/', views.edit_book),
    path('delete_book/', views.delete_book),
    path('author_list/', views.author_list),
    path('edit_author/', views.edit_author),
    path('delete_author/', views.delete_author),
    path('publisher_list/', views.publisher_list),
    path('edit_publisher/', views.edit_publisher),
    path('delete_publisher/', views.delete_publisher),
    path('add_book_isbn/', views.add_book_isbn),
    path('make_csv_view/', views.make_csv_view),
    # path('book_search_list/', views.book_search_list),
]