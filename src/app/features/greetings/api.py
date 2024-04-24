from src.app.features.greetings.endpoints import hello_world_multi_auth, hello_world, graph
from fastapi import APIRouter

api_router_azure_auth = APIRouter(tags=['hello'])
api_router_azure_auth.include_router(hello_world.router)
api_router_multi_auth = APIRouter(tags=['hello'])
api_router_multi_auth.include_router(hello_world_multi_auth.router)
api_router_graph = APIRouter(tags=['graph'])
api_router_graph.include_router(graph.router)
