import uvicorn
from fastapi import FastAPI
from settings import get_settings

app = FastAPI()


def run_server():
    uvicorn.run(
        'main:app',
        host=get_settings().host,
        port=get_settings().port,
        reload=True
    )


if __name__ == '__main__':
    run_server()
