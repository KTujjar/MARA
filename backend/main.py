from dotenv import load_dotenv

load_dotenv()

from agents.research import run_research_agent

query = input("What would you like to research?\n")

if __name__ == "__main__":
    answer = run_research_agent(query)
    print(answer)
