from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer

from slides.models import Slide


class SlideShowView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        serializer = SlideSerializer(Slide.objects.active(), many=True)
        context = super().get_context_data(**kwargs)
        context['slides_js'] = mark_safe(JSONRenderer().render(serializer.data))
        return context


class SlideSerializer(ModelSerializer):
    class Meta:
        model = Slide
        fields = ('id', 'title', 'url', 'order')


class SlidesListAPI(ListAPIView):
    serializer_class = SlideSerializer
    queryset = Slide.objects.active()
