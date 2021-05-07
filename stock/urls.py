from django.urls import path
from stock import views
from stock.views import StockDetail, ToDoItemList, ToDoItemCreate, ToDoItemDetail, ToDoItemUpdate, ToDoItemDelete

urlpatterns = [
    path('', views.home, name="home"),
    path('stock_list/', views.stock_list, name="stock_list"),
    path('add_stock/', views.add_stock, name="add_stock"),
    path('delete/<stock_id>', views.delete_stock, name="delete_stock"),
    path('stock/<int:pk>/', StockDetail.as_view(), name='stock_detail_url'),
    path('todoitem_list/', ToDoItemList.as_view(), name='to_do_item_list_url'),
    path('to_do_item/<int:pk>/', ToDoItemDetail.as_view(), name='to_do_item_detail_url'),
    path('to_do_item/create/', ToDoItemCreate.as_view(), name='to_do_item_create_url'),
    path('to_do_item/<int:pk>/update/', ToDoItemUpdate.as_view(), name='to_do_item_update_url'),
    path('to_do_item/<int:pk>/delete/', ToDoItemDelete.as_view(), name='to_do_item_delete_url'),
    path('about/', views.about, name="about"),
]
