from typing import TypedDict
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from .researcher import llm

class Section(BaseModel):
    name: str
    description: str
    content: str = ""

class SectionWriterState(TypedDict):
    topic: str
    section: Section
    research_context: str

async def author_node(state: SectionWriterState) -> Section:
    """Write section using research context"""
    section = state["section"]
    context = state["research_context"]
    
    write_prompt = f"""
    Write a detailed markdown section titled "{section.name}".
    Description: {section.description}
    
    Research Context:
    {context}
    
    Write in professional, technical tone. Use bullet points, headers, and examples.
    """
    
    print(f"✍️ Writing section: {section.name}")
    response = await llm.ainvoke([HumanMessage(content=write_prompt)])
    section.content = response.content
    return section
