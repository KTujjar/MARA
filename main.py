from exa_py import Exa
from dotenv import load_dotenv
import os

load_dotenv()

exa = Exa()

result = exa.search(
    "blog post about artificial intelligence",
    type="auto",
    contents={"highlights": True},
)

print(result)
