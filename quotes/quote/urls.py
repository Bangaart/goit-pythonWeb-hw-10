from django.urls import path

from quote import views

app_name = 'quote'
urlpatterns = [
    path('add/', views.add_quote, name='add_quote'),
    path('quotes-list', views.QuoteListView.as_view(), name='quote_list'),
    path('tag/<int:pk>', views.TagsQuoteListView.as_view(), name='tags_quotes'),
    path('fill_database', views.fill_database, name='fill_database'),
]
