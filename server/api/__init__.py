from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import viewsets


class CSRFProtectedModelViewSet(viewsets.ModelViewSet):
    @method_decorator(ensure_csrf_cookie)
    def create(self, request):
        return super(CSRFProtectedModelViewSet, self).create(request)

    @method_decorator(ensure_csrf_cookie)
    def update(self, request, **kwargs):
        return super(CSRFProtectedModelViewSet, self).update(request, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def partial_update(self, request, **kwargs):
        return super(CSRFProtectedModelViewSet, self).partial_update(request, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def destroy(self, request, **kwargs):
        return super(CSRFProtectedModelViewSet, self).destroy(request, **kwargs)
