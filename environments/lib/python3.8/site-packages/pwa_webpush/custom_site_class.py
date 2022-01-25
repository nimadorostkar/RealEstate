from urllib.parse import urlsplit, parse_qs

from django.urls import reverse


class CustomSite(object):
    protocol = "http"
    domain = None
    request_path = None
    fragment = None
    query = None
    params = None
    port = None

    site_url = None  # Without Slash
    base_url = None  # With Slash
    canonical_url = None

    def __init__(self, request):
        request_uri = request.build_absolute_uri()

        url = urlsplit(request_uri)

        self.protocol = url.scheme
        self.domain = url.hostname
        self.port = url.port
        self.request_path = url.path
        self.fragment = url.fragment
        self.query = url.query
        self.params = parse_qs(self.query)

        # Without Slash
        if self.port and self.port not in [80, 443]:
            self.site_url = "%s://%s:%s" % (self.protocol, self.domain, str(self.port))
        else:
            self.site_url = "%s://%s" % (self.protocol, self.domain)

        self.base_url = "%s/" % self.site_url  # With slash
        self.canonical_url = self.get_external_url(self.request_path)

    def get_external_url(self, resource_path):
        """
        Returns a fully qualified web address fo a resource.

        :param resource_path: A site relative path.
        :return: A url that includes the full site url to the resource
        """

        if resource_path[0] in ["/", "\\"]:
            urlbase = self.site_url
        else:
            urlbase = self.base_url

        external_url = "%s%s" % (urlbase, resource_path)

        return external_url

    def external_reverse(self, url_slug, **kwargs):

        return self.get_external_url(reverse(url_slug))
