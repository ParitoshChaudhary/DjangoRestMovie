from rest_framework import viewsets, status
from api.models import Movie, Rating
from api.serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print(f"Title of the movie is {movie.title} with {stars} stars by {user}")

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serilizer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating Update',
                    'result': serilizer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serilizer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating Created',
                    'result': serilizer.data
                }
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {
                'message': 'You need to provide stars'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {
            'message': 'You cant update rating through this process'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {
            'message': 'You cant create the rating through this process'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
