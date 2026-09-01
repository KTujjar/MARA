from typing import TypedDict, List

class _RequiredState(TypedDict):
    query:str

class ResearchState(_RequiredState, total=False):
    plan: str                   #orchestrator's research plan
    findings: List[str]         #accumulated research summaries, one per round
    critique_notes: str         #kwhat the critique agent flagged as missing
    needs_more_research: bool   #loop-control flag set by critique
    research_rounds: int        #guards ggainst infinite critique <-> research loops
    report: str                 #final synthesized report from the writer
    
