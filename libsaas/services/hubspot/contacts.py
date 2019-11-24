from libsaas import http, parsers
from libsaas.services import base


class ContactsResource(base.RESTResource):
    path = "contacts/v1/lists/all/contacts/all"


class Contacts(ContactsResource):
    @base.apimethod
    def get(self, count=None, vidOffset=None):
        """
        Returns all Contacts

        Upstream documentation:
        https://developers.hubspot.com/docs/methods/contacts/get_contacts
        """
        params = base.get_params(None, locals())

        return http.Request("GET", self.get_url(), params), parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple Contacts as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Contacts
        """
        params = base.get_params(None, locals())
        request = http.Request("DELETE", self.get_url(), params)
        return request, parsers.parse_json


class ContactsResource(base.RESTResource):
    path = "contacts/v1/contact"


class Contact(ContactsResource):
    @base.apimethod
    def get(self):
        """
        Returns all Contacts

        Upstream documentation:
        https://developers.hubspot.com/docs/methods/contacts/get_contacts
        """
        url = "{0}/{1}/vid/{2}/profile".format(
            self.parent.get_url(), self.path, self.object_id
        )

        return http.Request("GET", url), parsers.parse_json

    @base.apimethod
    def find(self, email):
        """
        Searches all Contacts by their name.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Contacts
        """
        url = "{0}/profile".format(self.get_url())
        return http.Request("GET", url), parsers.parse_json
