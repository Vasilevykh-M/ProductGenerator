
from fastapi import FastAPI

from app.modules.DataBase.postgre import Postgre
from app.modules.NeuralNetworks.generation import Generator
from app.modules.NeuralNetworks.promt import ClipModule
from app.modules.Server.server import GenerateApi

from fastapi.middleware.cors import CORSMiddleware

from app.utils.readConf import read_conf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Добавьте порты, которые вы используете
    # Другие домены
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


config = read_conf("app/config.toml")


generation_module = Generator(
    config['background'],
    config['inpainting'],
    config['blip'],
)

base = Postgre(
    config['database']['url'],
    config['database']['port'],
    config['database']['user'],
    config['database']['password'],
    config['database']['database'],
)

clip_module = ClipModule(
    base,
    config['clip'],
)

hello = GenerateApi(generation_module, clip_module)
app.include_router(hello.router)
