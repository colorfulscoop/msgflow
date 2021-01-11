from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pkg_resources
from typing import Any


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
    text: str
    dialog_id: str = 0
    data: dict[str, Any] = None


class Response(BaseModel):
    texts: list[str]
    request: Request


class Handler:
    def __init__(self, bot):
        self._bot = bot

    def handle(self, req: Request):
        msg = WebapiMessage(text=req.text, dialog_id=req.dialog_id, req=req)
        self._bot.handle(msg)
        return Response(texts=msg.msgs, request=req)


class WebapiMessage:
    def __init__(self, text: str, dialog_id: str, req):
        """"""
        self._text = text
        self._cid = dialog_id
        self._req = req
        self._msgs = []

    @property
    def text(self):
        return self._text

    @property
    def dialog_id(self) -> str:
        # In CliService, a conversation is identified by the user's name
        return self._cid

    def respond(self, text):
        self._msgs.append(text)

    @property
    def source(self) -> Any:
        return self._req

    @property
    def msgs(self):
        return self._msgs


class WebapiService:
    def __init__(self, config):
        """
        Args:
            config (Dict[str, Any])
        """
        # Set attributes
        self._config = config

    @classmethod
    def from_config(cls, config: dict[str, object]):
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
