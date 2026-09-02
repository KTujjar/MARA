from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

"""
from graph.build_graph import build_graph


if __name__ == "__main__":
    query = input("What would you like to research?\n")

    app = build_graph()
    result = app.invoke({"query":query})
    print(result["report"])
"""
