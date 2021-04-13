from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, schema
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from .models import Resource
from .serializers import ResourceSerializer


@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def resources_view(request):

    # GET request
    if request.method == 'GET':
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response({
            "resources": serializer.data,
            "total_count": Resource.objects.count()
        })

    # POST request
    elif request.method == 'POST':
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except IntegrityError:
                return Response(
                    {"detail": "Resource with entered title already exist"},
                    status=status.HTTP_409_CONFLICT
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    elif request.method == 'DELETE':
        # Возвращаем 204, если удалено успешно; 422 если запрос синтаксический правильный,
        # но id не существует, 400 если запрос неверный синтаксически
        if 'id' in request.data and request.content_type == 'application/x-www-form-urlencoded':
            try:
                res = Resource.objects.get(id=request.data['id'])
                res.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist as e:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # PUT & PATCH request
    # PUT требует все поля модели, PATCH - любое количество
    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            pk = request.data['id']
        except KeyError:
            return Response(
                {
                    "detail": "You need to enter integer resource id in request body."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        resource = get_object_or_404(Resource.objects.all(), pk=pk)

        # Различия в методах достигаются с помощью опции partial
        if request.method == 'PUT':
            serializer = ResourceSerializer(instance=resource, data=request.data)
        elif request.method == 'PATCH':
            serializer = ResourceSerializer(instance=resource, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
def total_cost_view(request):
    total_cost = Resource.objects.aggregate(Sum('price'))
    return Response(
        {"total_cost": total_cost}
    )
