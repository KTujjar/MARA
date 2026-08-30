from dotenv import load_dotenv

load_dotenv()

from agents.research import run_research_agent


if __name__ == "__main__":
    answer = run_research_agent("What happened at the last Fed meeting?")
    print(answer)
