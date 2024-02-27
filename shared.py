import urllib.parse

class Shared:
    def __init__(self, rss=None):
        self.rss = None
        if rss != None:
            self.rss=rss
    def get_request_headers_json(self):
        if hasattr(self, "rss") and self.rss != None:
            return {
                d1: d2 for d1, d2 in self.rss.headers.items()
            }
    def set_request_headers(self, name :str=None, value :str=None):
        if hasattr(self, "rss") and self.rss != None:
            if name != None and value != None:
                self.rss.headers[name] = value
                return self.get_request_headers_json()
    def remove_request_headers(self, name :str=None):
        if hasattr(self, "rss") and self.rss != None:
            if name != None and name in self.get_request_headers_json():
                return {
                    "name": name,
                    "value": self.rss.headers.pop(name)
                }
    def convert_json_to_values(self, config :dict=None):
        if config != None and isinstance(config, dict):
            return (
                config["method"] if "method" in config and config["method"] != None else None,
                config["url"] if "url" in config and config["url"] != None else None,
                config["params"] if "params" in config and config["params"] != None else None,
                config["data"] if "data" in config and config["data"] != None else None,
                config["headers"] if "headers" in config and config["headers"] != None else None,
                config["cookies"] if "cookies" in config and config["cookies"] != None else None,
                config["files"] if "files" in config and config["files"] != None else None,
                config["auth"] if "auth" in config and config["auth"] != None else None,
                config["timeout"] if "timeout" in config and config["timeout"] != None else None,
                config["allow_redirects"] if "allow_redirects" in config and config["allow_redirects"] != None and isinstance(config["allow_redirects"], bool) else True,
                config["proxies"] if "proxies" in config and config["proxies"] != None else None,
                config["hooks"] if "hooks" in config and config["hooks"] != None else None,
                config["stream"] if "stream" in config and config["stream"] != None and isinstance(config["stream"], bool) else False,
                config["verify"] if "verify" in config and config["verify"] != None else None,
                config["cert"] if "cert" in config and config["cert"] != None else None,
                config["json"] if "json" in config and config["json"] != None else None,
            )
    def dtsup(self, d1ct :dict=None):
        if d1ct != None and isinstance(d1ct, dict):
            return urllib.parse.urlencode(query=d1ct)