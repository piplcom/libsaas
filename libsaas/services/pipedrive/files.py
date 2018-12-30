from libsaas import http, parsers
from libsaas.services import base


class FilesResource(base.RESTResource):

    path = 'files'

    @base.apimethod
    def create(self, file, user_id=None, deal_id=None, person_id=None, org_id=None):
        params = base.get_params(None, locals())
        params.pop('file', None)

        return http.Request('POST', self.get_url(), params, files={
            "file": file
        }), parsers.parse_json


class Files(FilesResource):

    @base.apimethod
    def get(self, start=None, limit=None):
        """
        Returns data about all files.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Files
        """
        params = base.get_params(None, locals())
        return http.Request('GET', self.get_url(), params), parsers.parse_json


class File(FilesResource):
    pass
