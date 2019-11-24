from libsaas import http, parsers
from libsaas.services import base

"""
{
  "portalId": 62515,
  // Integer; The Hub ID that the company belongs to.
  "companyId": 184896670,
  // Integer; The unique ID of the company record.
  "isDeleted": false,
  // Boolean; Whether or not the record is deleted. In practice this will always be false as deleted records will not appear in the API.
  "properties": {
  // A set of objects representing the values for the set company properties.
  // Only populated properties will be included; properties that have never been set for the record will not be included.
    "country": {
    // String; The internal name of the property.
      "value": "United States",
      // String; The current value of the property.
      "timestamp": 1457708103906,
      // Integer; A Unix timestamp (in milliseconds) of the time the property was last set.
      "source": "BIDEN",
      // String; The method by which the value was set. See the contacts overview page (linked above) for more details
      "sourceId": "country",
      // String or null; Additional details for the source.
      // This may not be set for all source types.
      "versions": [
      // A list of previous versions of the property.
      // The first item in the list will be the current version
        {
          "name": "country",
          // String; The internal name of the property
          "value": "United States",
          // String; The value of the property for this version
          "timestamp": 1457708103906,
          // Integer; A Unix timestamp (in milliseconds) of the time when this version was set
          "source": "BIDEN",
          // String; The method by which this version was set. See the contacts overview page (linked above) for more details
          "sourceId": "country",
          // String or null; Additional details for the source of the change.
          // This may not be set for all source types
          "sourceVid": [
          // If the value was changed as the result of a change to a related contact record, this will be a list of vids for the changed contact.
          ]
        }
      ]
    },
    "city": {
      "value": "Cambridge",
      "timestamp": 1457708103906,
      "source": "BIDEN",
      "sourceId": "city",
      "versions": [
        {
          "name": "city",
          "value": "Cambridge",
          "timestamp": 1457708103906,
          "sourceId": "city",
          "source": "BIDEN",
          "sourceVid": [
            
          ]
        }
      ]
    }
  },
  "additionalDomains": []
  // This is a deprecated field and is not currently used.
}
"""


class CompaniesResource(base.RESTResource):
    path = "companies/v2/companies"


class Companies(CompaniesResource):
    @base.apimethod
    def get(self, limit=None, offset=None):
        """
        Returns all organizations

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """

        params = base.get_params(None, locals())
        url = "{0}/paged".format(self.get_url())
        return http.Request("GET", url, params), parsers.parse_json


class Company(CompaniesResource):
    @base.apimethod
    def get(self):
        """
        Returns all organizations

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        return http.Request("GET", self.get_url()), parsers.parse_json

    @base.apimethod
    def contacts(self):
        """
        Returns all contact related to company

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Company
        """
        url = "{0}/contacts".format(self.get_url())
        return http.Request("GET", url), parsers.parse_json


class CompaniesResource(base.RESTResource):
    path = "companies/v2/domains"


class CompaniesDomain(CompaniesResource):
    @base.apimethod
    def get(
        self,
        properties=("domain", "createdate", "name", "hs_lastmodifieddate"),
        limit=None,
        offset=None,
    ):
        """
        Upstream documentation:
        https://developers.hubspot.com/docs/methods/companies/search_companies_by_domain
        """

        params = base.get_params(['limit', 'offset'], locals())
        params.update({"requestOptions": {"properties": list(properties)}})

        url = "{0}/companies".format(self.get_url())
        return http.Request("POST", url, params), parsers.parse_json
