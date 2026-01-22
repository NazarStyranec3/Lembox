from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('h', views.hom, name='hom'),
    path('basket', views.basket, name='basket'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('admin_product', views.admin_product, name='admin_product'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('office', views.office_view, name='office'),
    path('logout', views.logout_view, name='logout'),

    path('close-order/', views.close_order, name='close_order'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('comments/<int:product_id>/', views.get_comments, name='get_comments'),

    path('product_detail_edit/<int:product_id>/', views.product_detail_edit, name='product_detail_edit'),
    path('add_product', views.add_product, name='add_product'),

    path('product_detail_remove/<int:product_id>/', views.product_detail_remove, name='product_detail_remove'),
    path('comment_remove/<int:comment_id>/', views.comment_remove, name='comment_remove'),
    
    
]
