from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from ebag.views import add_category, add_to_cart, checkout, confirm_purchase, login_view, product_detail, register_request, logout_view, home, add_product, edit_product, delete_product,product_list,index_home, remove_from_cart, thank_you_page,view_cart,first

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/', delete_product, name='delete_product'),
    path('products/', product_list, name='product_list'),
    path("register", register_request, name="register"),
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('index/', index_home, name='index'),
    path('', first, name='first'),
    path('admin/', admin.site.urls),
    path('data/login/',home),
    path('login/',login_view),
    path('add-product/',add_product),
    path('edit/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/',delete_product),
    path("register/", register_request, name="register"),
    path('cart/', view_cart, name='view_cart'),
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('add_category/', add_category, name='add_category'),
    path('confirm-purchase/', confirm_purchase, name='confirm_purchase'),
    path('thank-you/', thank_you_page, name='thank_you_page'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

