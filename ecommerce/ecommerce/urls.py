from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from store.views import (
    home,
    dashboard,
    add_to_cart,
    remove_from_cart,
    cart,
    product_detail,
    register_user,
    login_user,
    logout_user,
    checkout,
    payment
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', login_user),
    path('login/', login_user, name='login'),  # ✅ ADD THIS

    path('register/', register_user),

    path('home/', dashboard),
    path('products/', home, name='products'),

    path('product/<int:product_id>/', product_detail),

    path('cart/', cart),
    path('add-to-cart/<int:product_id>/', add_to_cart),
    path('remove-from-cart/<int:product_id>/', remove_from_cart),

    path('checkout/', checkout),
    path('payment/', payment),

    path('logout/', logout_user),
]

# ✅ MEDIA FILE SERVING (THIS FIXES YOUR ISSUE)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)