from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn


def build_api(handler):
    app = FastAPI(
        title="msgFlow",
        description="",
        version="0.0.0",
    )
    app.add_api_route("/handle", handler.handle, methods=["POST"])
    return app


class Request(BaseModel):
    text: str
    conversation_id: str = 0


class Response(BaseModel):
    texts: list[str]
    request: Request


class Handler:
    def __init__(self, bot):
        self._bot = bot

    def handle(self, req: Request):
        msg = WebapiMessage(text=req.text, conversation_id=req.conversation_id)
        self._bot.handle_background(msg)
        return Response(texts=msg.msgs, request=req)


class WebapiMessage:
    def __init__(self, text: str, conversation_id: str):
        """"""
        self._text = text
        self._cid = conversation_id
        self._msgs = []

    @property
    def text(self):
        return self._text

    @property
    def conversation_id(self) -> str:
        # In CliService, a conversation is identified by the user's name
        return self._cid

    def respond(self, text):
        self._msgs.append(text)

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
        self._config = WebapiConfig(**config)

    def start_msg_stream(self, bot):
        handler = Handler(bot=bot)
        app = build_api(handler)
        uvicorn.run(app=app, host=self._config.host, port=self._config.port)

    def post(self, text):
        raise NotImplementedError()


class WebapiConfig(BaseModel):
    host: str
    port: int
