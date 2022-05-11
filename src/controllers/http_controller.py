import json
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic.json import pydantic_encoder

from src.business_layer.activate_user.use_case import (
    ActivateUserRequest,
    ActivateUserUseCase,
)
from src.business_layer.create_user.use_case import CreateUserRequest, CreateUserUseCase
from src.business_layer.errors import Error, ErrorCode
from src.business_layer.get_user.use_case import GetUserRequest, GetUserUseCase


# This is the HTTP response model
class JSONResponsePydantic(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            default=pydantic_encoder,
            ensure_ascii=False,
            indent=None,
        ).encode("utf-8")


# This is the output adapter injected in the use-case's output port
class HttpOutputAdapter:
    def __call__(self, response: Any) -> JSONResponsePydantic:
        # Convert the domain response model to http response model
        http_response = JSONResponsePydantic(response)
        return http_response


def make_http_controller(
    user_creator: CreateUserUseCase[JSONResponsePydantic],
    activate_user: ActivateUserUseCase[JSONResponsePydantic],
    get_user: GetUserUseCase[JSONResponsePydantic],
) -> FastAPI:
    app = FastAPI()

    @app.exception_handler(Error)
    async def error_handler(_: Request, e: Error):
        status_code = 400
        if e.error_codes:
            if e.error_codes[0] == ErrorCode.system_error:
                status_code = 500
            if e.error_codes[0] == ErrorCode.user_not_found:
                status_code = 404

        return JSONResponse(
            status_code=status_code,
            content={"errors": f"{e.error_codes}"},
        )

    @app.post("/users/")
    def _create_user(request: CreateUserRequest):
        # First, convert the HTTP request model to domain request model,
        # this is done automatically by FastAPI

        # Then call the interactor.
        # This returns the http response created by the output adapter.
        response: JSONResponsePydantic = user_creator.create_user(request)

        # Because of the way FastAPI works, we have to return the
        # HTTP Response from the controller, but the heavy work
        # is done in the output adapter, not in the controller.
        return response

    @app.post("/user/activate")
    def _activate_user(request: ActivateUserRequest):
        response = activate_user(request)
        return response

    @app.get("/user")
    def _get_user_by_email(request: GetUserRequest = Depends()):
        response = get_user(request)
        return response

    return app
