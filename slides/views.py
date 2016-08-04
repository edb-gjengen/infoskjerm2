from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer

from slides.models import Slide


class SlideShowView(TemplateView):
    template_name = 'index.html'


class SlideSerializer(ModelSerializer):
    class Meta:
        model = Slide


class SlidesListAPI(ListAPIView):
    serializer_class = SlideSerializer
    queryset = Slide.objects.active()
