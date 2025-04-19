import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views import View
from middlewares.service_proxy import ServiceProxy, ServiceUnavailableError

logging = logging.getLogger(__name__)

class GatewayView(View):

    service_name = None

    def dispatch(self, request, *args, **kwargs):
        if self.service_name is None:
            return JsonResponse({"error": "Service not configured"}, status=500)
        
        try:
            proxy = ServiceProxy(self.service_name)

            path = request.path.split(f'/{self.service_name}/')[-1]

            response = proxy.forward_request(
                request_path=path,
                method=request.method,
                headers=request.headers,
                body=request.body,
                params=request.GET
            )

            proxy_response = JsonResponse(
                data=response['content'],
                status=response['status_code'],
                safe=False
            ) if response['headers'].get('Content-Type') == 'application/json' else HttpResponse(
                content=response['content'],
                status=response['status_code'],
                content_type=response['headers'].get('Content-Type')
            )

            for header, value in response['headers'].items():
                if header.lower() not in ['content-length', 'transfer-encoding']:
                    proxy_response[header] = value
            
            return proxy_response
            
            
        except ServiceUnavailableError as e:
            logging.error(f"Service unavailable: {str(e)}")
            return JsonResponse({"error": "Service unavailable"}, status=503)
        except Exception as e:
            logging.error(f"Gateway error: {str(e)}")
            return JsonResponse({"error": "Internal gateway error"}, status=500)


class StatusView(View):
    """
    A simple view to check the status of the API.
    """

    def get(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{get} response from {gateway} service"}, 
                status=200)

    def post(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{post} response from {gateway} service"}, 
                status=200)
    
    def put(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{put} response from {gateway} service"}, 
                status=200)
    
    def delete(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{delete} response from {gateway} service"}, 
                status=200)
    
    def patch(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{patch} response from {gateway} service"}, 
                status=200)
    
    def head(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{head} response from {gateway} service"}, 
                status=200)
    
    def options(self, request):
        """
        Returns a simple JSON response indicating that the API is up and running.
        """
        return JsonResponse(
            {
                "status": "ok",
                "message": "{options} response from {gateway} service"}, 
                status=200)


class AuthServiceView(GatewayView):
    """
    A view to handle requests to the Auth service.
    """
    service_name = "auth"


class UsersServiceView(GatewayView):
    """
    A view to handle requests to the Users service.
    """
    service_name = "users"


class WalletServiceView(GatewayView):
    """
    A view to handle requests to the Wallet service.
    """
    service_name = "wallet"

