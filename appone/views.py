from django.shortcuts import render

# Create your views here.
from appone.models import User,FoodItem,AddtoBag,Address,PlaceOrder
from appone.serializers import UserRegistrationSerializer,LoginSerializers,FoodItemSerializer,AddtoBagSerializer,AddressSerializers,PlaceOrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class RegistrationView(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"Registration successfull"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializers(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data["email"]
            password=serializer.validated_data["password"]
            user=authenticate(email=email,password=password)
            if user is not None:   
                login(request,user)
                refresh = RefreshToken.for_user(user)
                return Response( {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'msg':'login successfull'
                    })

            return Response({'msg':'invalid credential'})
        return Response(serializer.errors)


class FoodItemView(APIView):
    def get(self,request):
        items=FoodItem.objects.all()
        serializer=FoodItemSerializer(items,many=True)
        return Response(serializer.data)
    

class AddtoBagView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        id=request.data.get("id")
        food_item=FoodItem.objects.get(id=id)
        quantity=request.data.get("quantity",1)
        price=food_item.price*quantity
        AddtoBag.objects.create(user=user,food_item=food_item,quantity=quantity,price=price)
        return Response({"msg":"added to bag"})
    


class ViewCart(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        data=AddtoBag.objects.filter(user=user)
        serializer=AddtoBagSerializer(data,many=True)
        total_price=10
        for i in data:
            total_price+=i.price
        response_data={"item":serializer.data,"total_price":total_price}
        return Response(response_data)
    

class SaveAddress(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        serializer=AddressSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"msg":"address saved successfilly"})
        return Response(serializer.errors)



# class PlaceOrderView(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         user=request.user
#         serializer=PlaceOrderSerializer(data=request.data)
#         print("hello")
#         if serializer.is_valid():
#             print("hiii")
#             address_id=serializer.data.get("address")
#             address=Address.objects.get(id=address_id)
#             cart=AddtoBag.objects.filter(user=user)
#             for cart_item in cart:
#                 total_price=0
#                 food_item=cart_item.food_item
#                 quantity=cart_item.quantity
#                 order=PlaceOrder.objects.create(user=user,address=address,food_item=food_item,quantity=quantity,total_price=total_price)
#                 total_price=cart_item.price
#                 order.total_price=total_price
#                 order.save()
#                 cart_item.delete()
#             return Response({"msg":"Order placed"})
#         return Response(serializer.errors)



class PlaceOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user 
        address_id=request.data.get("address")
        address=Address.objects.get(id=address_id)
        cart=AddtoBag.objects.filter(user=user)
        for cart_item in cart:
            total_price=0
            food_item=cart_item.food_item
            quantity=cart_item.quantity
            order=PlaceOrder.objects.create(user=user,address=address,food_item=food_item,quantity=quantity,total_price=total_price)
            total_price=cart_item.price
            order.total_price=total_price
            order.save()
            cart_item.delete()
        return Response({"msg":"Order placed"})
