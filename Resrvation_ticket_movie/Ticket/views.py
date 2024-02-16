import dataclasses
from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Geust, Movie, Post,Resrvation
from rest_framework.decorators import api_view
from .serialzers import GeustSerializers,MovieSerilazers, PostSerializer ,ResrvationSerializers  
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .premissions import IsAuthorOrReadOnly
#from .permissions import IsAuthorOrReadOnly


#1 without REST and no model query FBV
def noresete_nomodel(request):
    guests =[
        {
            "id" : 22,
            "name": "Larbi",
            "mobile":33043,
        },
        {
           "id" : 2,
           "name": "Modi",
           "mobile":98743, 
        }
    ]
    return JsonResponse(guests ,safe=False)

#2 model data default django without rest
def norest_frommodel(request):
    data = Geust.objects.all()
    response ={
        'gustes' : list(data.values('name','mobile'))
    }
    return JsonResponse(response)

# List == GET
# Create == POST
# pk query == GET 
# Update == PUT
# Delete destroy == DELETE

#3 Function based views 
#3.1 GET POST

@api_view(['GET','POST'])
def FBV_list(request):
    #GET
    if request.method == 'GET':
        guest = Geust.objects.all()
        serializers = GeustSerializers(guest,many=True)
        return Response(serializers.data)
    #POST
    elif request.method == 'POST':
        serializers = GeustSerializers(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guset=Geust.objects.get(pk=pk)
    except Geust.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serilalizers=GeustSerializers(guset,many=False)
        return Response(serilalizers.data)
    elif request.method =='PUT':
        serilalizers = GeustSerializers(guset,data=request.data)
        if serilalizers.is_valid():
            serilalizers.save()
            return Response(request.data)
        return Response(serilalizers.errors , status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guset.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

# CBV Class based views
#4.1 List and Create == GET and POST
class CBv_List(APIView):
    def get(self,request):
        guest = Geust.objects.all()
        serializers = GeustSerializers(guest,many=True)
        return Response(serializers.data)
    def post(self,request):
        serializers= GeustSerializers(data =request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(
                serializers.data,
                status=status.HTTP_201_CREATED
                            )
        return Response(
            serializers.data,
            status= status.HTTP_400_BAD_REQUEST
                        )



#4.2 GET PUT DELETE cloass based views -- pk 
class CBv_pk(APIView):

    def get_object(self ,pk):
        try:
            return Geust.objects.get(pk=pk)
        except Geust.DoesNotExist:
            raise Http404
    def get(self ,request ,pk):
        geust = self.get_object(pk)
        serializers = GeustSerializers(geust)
        return Response(serializers.data)
    def put(self , request ,pk):
        geust = self.get_object(pk)
        serializers = GeustSerializers(geust,data=request.data)
        if serializers.is_valid():
            geust.save()
            return Response(serializers.data)
        return Response(serializers.data , status=status.HTTP_400_BAD_REQUEST)
    def delete(self , request , pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
#5 Mixins 
#5.1 mixins list
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Geust.objects.all()
    serializers_class = GeustSerializers

    def get(self,request):
        return self.list(request)
    def post(self ,request):
        return self.create(request)
class mixnis_pk(mixins.DestroyModelMixin, mixins.UpdateModelMixin ,mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Geust.objects.all()
    serializer_class = GeustSerializers
    def get(self , request ,pk):
        return self.retrieve(request)
    def put(self, request ,pk):
        return self.update(request)
    def delete(self , request ,pk):
        return self.delete(request)
# 6 Generics 
#6.1 get and post

class generics_list(generics.ListCreateAPIView):
    queryset = Geust.objects.all()
    serializer_class = GeustSerializers
    authentication_classes ={TokenAuthentication}

#6.2 get put and delete 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Geust.objects.all()
    serializer_class = GeustSerializers
    authentication_classes ={TokenAuthentication}

#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Geust.objects.all()
    serializer_class = GeustSerializers

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerilazers
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Resrvation.objects.all()
    serializer_class = Resrvation

@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall =request.data['hall'],
        movie = request.data['movie']
    )
    serializers = MovieSerilazers(movies,many=True)
    return Response(serializers.data)
def new_resrvation(request):
    movie =Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie']
    )
    geust =Geust()
    geust.name= request.data['name']
    geust.mobile = request.data['mobile']
    geust.save()

    resrvation = Resrvation()
    resrvation.geust =geust
    resrvation.movie = movie
    resrvation.save()
    return Response(status=status.HTTP_201_CREATED)

#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    