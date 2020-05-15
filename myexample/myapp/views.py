from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        kwargs['mongo'] = 'myapp/js/mongo.js'
        kwargs['appcache'] = 'appcache.manifest'
        return kwargs
