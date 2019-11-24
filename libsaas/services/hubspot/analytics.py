from libsaas import http, parsers
from libsaas.services import base


class AnalyticsResource(base.RESTResource):

    path = '/analytics/v2'


class Analytics(AnalyticsResource):

    @base.apimethod
    def get(self, user_id=None, start=None, limit=None, start_date=None,
            end_date=None):
        """
        Returns all activities assigned to a particular user

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Activities
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple activities as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Activities
        """
        params = base.get_params(None, locals())

        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class Activity(AnalyticsResource):
    pass
