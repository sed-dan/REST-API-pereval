from rest_framework.views import APIView
from .serializers import PerevalSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Pereval


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer


class SubmitDataView(APIView):
    def post(self, request):
        try:
            serializer = PerevalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Запись успешно создана',
                        'id': serializer.instance.id
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': serializer.errors,
                        'id': None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': f"Ошибка сервера: {str(e)}",
                    "id": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        email = request.query_params.get('user__email')

        if not email:
            return Response(
                {"message": "Не указан email пользователя", "status": 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval_list = Pereval.objects.filter(user__email=email)

            if not pereval_list.exists():
                return Response(
                    {"message": "Нет записей для указанного пользователя", "status": 404},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PerevalSerializer(pereval_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": f"Ошибка сервера: {str(e)}", "status": 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SubmitDataDetailView(APIView):
    def get(self,request,id):
        try:
            pereval = Pereval.objects.get(id=id)
            serializer = PerevalSerializer(pereval)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pereval.DoesNotExist:
            return Response(
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': "Перевал не найден",
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, id):
        try:
            pereval = Pereval.objects.get(id=id)
        except Pereval.DoesNotExist:
            return Response(
                {"state": 0, "message": "Запись не найдена."},
                status=status.HTTP_404_NOT_FOUND
            )

        if pereval.status != 'new':
            return Response(
                {"state": 0, "message": "Запись нельзя редактировать в данном статусе"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if 'user' in request.data:
            return Response({"state": 0, "message": "Нельзя редактировать данные пользователя"},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        serializer = PerevalSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"state": 1, "message": "Запись успешно обновлена."})
        else:
            return Response(
                {"state": 0, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
