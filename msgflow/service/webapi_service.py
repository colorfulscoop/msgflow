from pydantic import BaseModel, validator
from fastapi import FastAPI
import uvicorn
import pkg_resources
from typing import Any, List, Dict


def build_api(handler, endpoint):
    def get_version():
        pkg_name = "msgflow"
        try:
            version = pkg_resources.get_distribution(pkg_name).version
        except pkg_resources.DistributionNotFound:
            print(f"Package name not found: {pkg_name}")
            version = "package version info not found"
        return version

    app = FastAPI(
        title="msgFlow",
        description="",
        version=get_version(),
    )
    app.add_api_route(endpoint, handler.handle, methods=["POST"])

    return app


class Request(BaseModel):
    context: List[str]
    data: Dict[str, Any] = None

    @validator("context")
    def context_not_empty(cls, v):
        if not v:
            raise Exception("Context should have at least one value")
        return v


class Response(BaseModel):
    texts: List[str]
    request: Request


class Handler:
    def __init__(self, bot):
        self._bot = bot

    def handle(self, req: Request):
        context = [WebapiMessage(text=text, req=req) for text in req.context]
        self._bot.handle(context=context)
        return Response(texts=context[0].responses, request=req)


class WebapiMessage:
    def __init__(self, text: str, req):
        """"""
        self._text = text
        self._req = req
        self._responses = []

    @property
    def text(self):
        return self._text

    def respond(self, text):
        self._responses.append(text)

    @property
    def source(self) -> Any:
        return self._req

    @property
    def responses(self) -> List[str]:
        """This property is specific to WebapiMessage."""
        return self._responses


class WebapiService:
    def __init__(self, config):
        """
        Args:
            config (Dict[str, Any])
        """
        # Set attributes
        self._config = config

    @classmethod
    def from_config(cls, config: Dict[str, object]):
        cfg = WebapiConfig(**config)
        return cls(config=cfg)

    def flow(self, bot):
        handler = Handler(bot=bot)
        app = build_api(
            handler,
            endpoint=self._config.endpoint,
        )
        uvicorn.run(app=app, host=self._config.host, port=self._config.port)

    def post(self, text):
        raise NotImplementedError()


class WebapiConfig(BaseModel):
    host: str
    port: int
    endpoint: str = "/handle"
