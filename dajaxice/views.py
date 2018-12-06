import logging
import django
from django.conf import settings
import json
from django.views.generic.base import View
from django.http import HttpResponse, Http404

from dajaxice.exceptions import FunctionNotCallableError
from dajaxice.core import dajaxice_functions, dajaxice_config

log = logging.getLogger('dajaxice')


class DajaxiceRequest(View):
    """ Handle all the dajaxice xhr requests.
    """
    def dispatch(self, request, *args, **kwargs):
        name = kwargs.get('name')

        if not name and len(args) == 1:
            name = args[0]

        if not name:
            raise Http404

        # Check if the function is callable
        if dajaxice_functions.is_callable(name, request.method):
            function = dajaxice_functions.get(name)
            data = getattr(request, function.method).get('argv', '')

            # Clean the argv
            if data != 'undefined':
                try:
                    data = json.loads(data, encoding='utf-8')
                except Exception as ex:
                    log.error(ex)
                    data = {}
            else:
                data = {}

            # Call the function. If something goes wrong, handle the Exception
            try:
                response = function.call(request, **data)
            except Exception as ex:
                log.error(ex)

                if settings.DEBUG:
                    raise

                response = dajaxice_config.DAJAXICE_EXCEPTION

            return HttpResponse(response, content_type="application/x-json")
        else:
            raise FunctionNotCallableError(name)
