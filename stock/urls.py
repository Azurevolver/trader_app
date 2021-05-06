from django.urls import path
from stock import views
from stock.views import StockDetail

urlpatterns = [
    path('', views.home, name="home"),
    path('stock_list/', views.stock_list, name="stock_list"),
    path('add_stock/', views.add_stock, name="add_stock"),
    path('delete/<stock_id>', views.delete_stock, name="delete_stock"),
    path('stock/<int:pk>/', StockDetail.as_view(), name='stock_detail_url'),
    path('about/', views.about, name="about"),
]