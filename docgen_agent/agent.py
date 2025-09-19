from typing import List
from .researcher import researcher_node
from .author import Section, SectionWriterState, author_node

class Agent:
    def __init__(self, topic: str):
        self.topic = topic
        self.sections = [
            Section(name="Introduction", description="Overview and importance"),
            Section(name="Technical Architecture", description="How it works technically"),
            Section(name="Real-World Applications", description="Case studies and examples"),
            Section(name="Future Trends", description="What's coming in 2025 and beyond")
        ]
        self.report = ""

    async def run(self):
        """Run full agent workflow"""
        print(f"🚀 Starting Report Agent for: {self.topic}")
        
        # Step 1: Initial research
        print("🔎 Performing initial research...")
        research_context = await researcher_node(f"Comprehensive overview of {self.topic}")
        
        # Step 2: Write each section
        for section in self.sections:
            state = SectionWriterState(
                topic=self.topic,
                section=section,
                research_context=research_context
            )
            updated_section = await author_node(state)
            self.sections[self.sections.index(section)] = updated_section
        
        # Step 3: Compile report
        self.report = f"# Report: {self.topic}\n\n"
        for section in self.sections:
            self.report += f"{section.content}\n\n"
        
        return self.report
