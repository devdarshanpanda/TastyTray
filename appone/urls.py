from django.urls import path,include
from appone import views
urlpatterns = [
    path("registration/",views.RegistrationView.as_view()),
    path("login/",views.LoginView.as_view()),
    path("fooditem/",views.FoodItemView.as_view()),
    path("addtobag/",views.AddtoBagView.as_view()),
    path("viewcart/",views.ViewCart.as_view()),
    path("saveaddress/",views.SaveAddress.as_view()),
    path("placeorder/",views.PlaceOrderView.as_view()),

]