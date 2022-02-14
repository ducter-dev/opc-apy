from fastapi import Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from ..tokenServices import validate_token

class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            try:
                token = request.headers["Authorization"].split(" ")[1]
                print(token)
                validation_response = validate_token(token, output=False)
                print(validation_response)

                if validation_response == None:
                    return await original_route(request)
                else:
                    return validation_response
            except Exception as ex:
                return JSONResponse(content={"error": f'Error: {ex}'}, status_code=401)

            
        return verify_token_middleware