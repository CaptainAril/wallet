from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class StatusView(APIView):
    """
    A simple view to check the status of the API.
    """

    def get(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{get} response from {users} service"}, 
                status=status.HTTP_200_OK)

    def post(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{post} response from {users} service"}, 
                status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{put} response from {users} service"}, 
                status=status.HTTP_200_OK)
    
    def delete(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{delete} response from {users} service"}, 
                status=status.HTTP_200_OK)
    
    def patch(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{patch} response from {users} service"}, 
                status=status.HTTP_200_OK)
    
    def head(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{head} response from {users} service"}, 
                status=status.HTTP_200_OK)
    
    def options(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return Response(
            {
                "status": "ok",
                "message": "{options} response from {users} service"}, 
                status=status.HTTP_200_OK)
