import json

from rest_framework.renderers import JSONRenderer


class SenderJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super(SenderJSONRenderer, self).render(data)

        return json.dumps({
            'user': data
        })

class CreateChatJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super(CreateChatJSONRenderer, self).render(data)

        return json.dumps({
            'chat': data
        })