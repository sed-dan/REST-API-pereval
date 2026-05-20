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
