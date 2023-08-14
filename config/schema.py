from drf_spectacular.extensions import OpenApiAuthenticationExtension


class TokenAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "knox.auth.TokenAuthentication"
    match_subclasses = True
    priority = 1
    name = "Wave Token"

    def get_security_definition(self, auto_schema):
        return {"type": "Token", "in": "header", "name": "Auth Token"}
