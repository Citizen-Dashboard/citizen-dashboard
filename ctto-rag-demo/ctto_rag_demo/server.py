#!/usr/bin/env python
from typing import List
import uvicorn

from fastapi import FastAPI
from langserve import add_routes

from .rag import getChain




def startApp():
    # 4. App definition
    app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
    )

    chain = getChain()

    # 5. Adding chain route

    add_routes(
        app,
        chain,
        path="/dashboard",
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)

