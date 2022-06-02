from django.urls import path, re_path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('navbar', views.NavbarView.as_view(), name='navbar'),
    re_path(r'category/(?P<category_slug>[-\w]+)/', views.CategoryFilterView.as_view(), name='category_filter'),
    re_path(r'like/(?P<product_slug>[-\w]+)', views.ProductLikeView.as_view(), name='product_like'),
    re_path(r'save/(?P<product_slug>[-\w]+)', views.ProductSaveView.as_view(), name='product_save'),
    path('products_like/', views.ProductsLikeView.as_view(), name='products_like'),
    path('products_save/', views.ProductsSaveView.as_view(), name='products_save'),
    path('search/', views.SearchProductsView.as_view(), name='product_search'),
    re_path(r'product/(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'comment_reply/(?P<comment_id>[0-9]+)/(?P<slug>[-\w]+)/', views.CreateReplyCommentView.as_view(), name='create_reply_comment'),
]

