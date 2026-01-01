# from starlette.applications import Starlette, Request
# from starlette.authentication import (
#     AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
# )

# # Authentication Backend Class
# class BearerTokenAuthBackend(AuthenticationBackend):
#     """
#     This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
#     a tuple
#     """
#     async def authenticate(self, request: Request):
#         # This function is inherited from the base class and called by some other class
#         if "Authorization" not in request.headers:
#             return

#         auth = request.headers["Authorization"]
#         try:
#             scheme, token = auth.split()
#             if scheme.lower() != 'bearer':
#                 return
#             decoded = jwt.decode(
#                 token,
#                 settings.JWT_SECRET,
#                 algorithms=[settings.JWT_ALGORITHM],
#                 options={"verify_aud": False},
#             )
#         except (ValueError, UnicodeDecodeError, JWTError) as exc:
#             raise AuthenticationError('Invalid JWT Token.')

#         username: str = decoded.get("sub")
#         token_data = TokenData(username=username)
#         # This is little hack rather making a generator function for get_db
#         db = LocalSession()
#         user = User.objects(db).filter(User.id == token_data.username).first()
#         # We must close the connection
#         db.close()
#         if user is None:
#             raise AuthenticationError('Invalid JWT Token.')
#         return auth, user
