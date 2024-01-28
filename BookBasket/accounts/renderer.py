from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    ## default render function template
    def render(self, data, accepted_media_type=None, renderer_context=None):

        response = ''
        ## Whenever an error is raised it has the errordetail string in it, so we look for this string and if found
        # , we return response as the error itself, else we return the data we get in response.
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else :
            response = json.dumps(data)

        return response