from dotenv import load_dotenv

load_dotenv()

from graph.build_graph import build_graph


if __name__ == "__main__":
    query = input("What would you like to research?\n")

    app = build_graph()
    result = app.invoke({"query":query})
    print(result["report"])
