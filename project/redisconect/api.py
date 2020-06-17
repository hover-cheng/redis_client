from rest_framework import serializers, status, permissions
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from redisconect.models import redisInfo, UserProfile


class RedisInfoSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = redisInfo
        fields = '__all__'
        depth = 1


@authentication_classes((JWTAuthentication,))
class GetUserName(APIView):
    def get(self, request):
        if request.successful_authenticator:
            # 获取token中的用户名
            user = request.user
            username = UserProfile.objects.get(belong_to=user).name
            ser = {"username": username}
            return Response(ser)
        else:
            ser = {"message": "Token is invalid or expired"}
            return Response(ser, status=status.HTTP_403_FORBIDDEN)


@authentication_classes((JWTAuthentication,))
class RedisInfo(APIView):
    def get(self, request):
        # 判断用户是否使用token认证成功
        if request.successful_authenticator:
            # 获取token中的用户名
            user = request.user
            username = UserProfile.objects.get(belong_to=user)
            sqlprotype = redisInfo.objects.filter(director=username).order_by('projectname')
            ser = RedisInfoSerizlizer(sqlprotype, many=True)
            return Response(ser.data)
        else:
            ser = {"message": "Token is invalid or expired"}
            return Response(ser, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if request.successful_authenticator:
            user = request.user
            director = UserProfile.objects.get(belong_to=user)
            redisname = request.data["redisname"]
            redistype = request.data["redistype"]
            nodelist = request.data["nodelist"]
            password = request.data["password"]
            mastername = request.data["mastername"]
            projectname = request.data["projectname"]
            createcontent = redisInfo.objects.create(
                redisname=redisname,
                redistype=redistype,
                nodelist=nodelist,
                password=password,
                mastername=mastername,
                projectname=projectname,
                director=director,
            )
            return Response({'post': "create completed"})
        else:
            ser = {"message": "Token is invalid or expired"}
            return Response(ser, status=status.HTTP_403_FORBIDDEN)


@authentication_classes((JWTAuthentication,))
class RedisId(APIView):
    def get(self, request, id):
        if request.successful_authenticator:
            sqlprotype = redisInfo.objects.get(id=id)
            ser = RedisInfoSerizlizer(sqlprotype)
            return Response(ser.data)
        else:
            ser = {"message": "Token is invalid or expired"}
            return Response(ser, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, id):
        if request.successful_authenticator:
            redisInfo.objects.get(id=id).delete()
            return Response({'msg': "delete completed"})
        else:
            ser = {"message": "Token is invalid or expired"}
            return Response(ser, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, id):
        if request.successful_authenticator:
            user = request.user
            director = UserProfile.objects.get(belong_to=user).name
            redisname = request.data["redisname"]
            redistype = request.data["redistype"]
            nodelist = request.data["nodelist"]
            password = request.data["password"]
            mastername = request.data["mastername"]
            projectname = request.data["projectname"]
            redis_ = redisInfo.objects.get(id=id)
            redis_.redisname = redisname
            redis_.redistype = redistype
            redis_.nodelist = nodelist
            redis_.password = password
            redis_.mastername = mastername
            redis_.projectname = projectname
            redis_.director = director
            redis_.save()
            return Response({'msg': "update completed"})
        else:
            ser = {"message": "Token is invalid or expired"}
            return Response(ser, status=status.HTTP_403_FORBIDDEN)
