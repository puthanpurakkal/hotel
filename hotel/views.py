# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from hotel.models import Dishes, Review
from hotel.serializers import DishSerializer, DishesModelSerializer, UserSerializer, ReviewSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions, authentication
from rest_framework.decorators import action


# Create your views here.


class DishesView(APIView):

    def get(self, request, *args, **kwargs):
        all_dishes = Dishes.objects.all()
        serializer = DishSerializer(all_dishes, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            category = serializer.validated_data.get("category")
            price = serializer.validated_data.get("price")
            Dishes.objects.create(name=name,
                                  category=category,
                                  price=price)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class DishDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        serializer = DishSerializer(dish)
        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.validated_data.get("category")
            name = serializer.validated_data.get("name")
            price = serializer.validated_data.get("price")
            instance.name = name
            instance.price = price
            instance.category = category
            instance.save()
            return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        dish.delete()
        return Response({"msg": "deleted"})


class MenuItemsView(APIView):
    serializer_class = DishesModelSerializer

    def get(self, request, *args, **kwargs):
        all_dishes = Dishes.objects.all()
        serializer = self.serializer_class(all_dishes, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class MenuItemDetailsView(APIView):
    serializer_class = DishesModelSerializer

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        serializer = DishesModelSerializer(dish)
        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        dish.delete()
        return Response(data=request.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer = self.serializer_class(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class SignUpView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # User.objects.create_user(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class DishViewsetView(viewsets.ViewSet):
    serializer_class = DishesModelSerializer

    def list(self, request, *args, **kwargs):
        qs = Dishes.objects.all()
        if "category" in request.quert_params:
            category = request.quert_params.get("category")
            qs = qs.filter(category=category)
        if "price_lt" in request.quert_params:
            price = request.quert_params.get("price_lt")
            qs = qs.filter(price__lte=price)
        serializer = DishesModelSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = DishesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs = Dishes.objects.get(id=id)
        serializer = DishesModelSerializer(qs)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        instance = Dishes.objects.get(id=id)
        serializer = DishesModelSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs = Dishes.objects.get(id=id)
        qs.delete()
        return Response({"message": "deleted"})


class DishModelViewsetView(viewsets.ModelViewSet):
    serializer_class = DishesModelSerializer
    queryset = Dishes.objects.all()
    model = Dishes

    # authentication_classes = [authentication.BaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_reviews(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        dish = Dishes.objects.get(id=id)
        qs = Review.objects.filter(dish=dish)
        serializer = ReviewSerializer(qs, many=True)
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'])
    def add_review(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        dish = Dishes.objects.get(id=id)
        user = request.user
        serializer = ReviewSerializer(data=request.data, context={"user": user, "dish": dish})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



