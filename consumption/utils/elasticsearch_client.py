import os

from elastic_transport import RequestsHttpNode
from elasticsearch import Elasticsearch


class ElasticsearchClient(Elasticsearch):
    """
    This extends the Elasticsearch client to provide proxy support via a custom HTTP node.
    """

    class CustomHttpNode(RequestsHttpNode):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Get the proxies from HTTP_PROXY and HTTPS_PROXY environment variables
            self.session.proxies = {
                "http": os.environ.get("HTTP_PROXY", os.environ.get("http_proxy")),
                "https": os.environ.get("HTTPS_PROXY", os.environ.get("https_proxy")),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, node_class=self.CustomHttpNode)
