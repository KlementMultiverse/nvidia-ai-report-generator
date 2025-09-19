import asyncio
from docgen_agent.agent import Agent

async def main():
    # Initialize agent
    agent = Agent(topic="AI Agents in Healthcare 2025")
    
    # Run agent
    report = await agent.run()
    
    # Print and save
    print("\n" + "="*80)
    print("📊 FINAL REPORT:")
    print("="*80)
    print(report)
    
    # Save to file
    with open("generated_report.md", "w") as f:
        f.write(report)
    print("\n✅ Report saved to generated_report.md")

if __name__ == "__main__":
    asyncio.run(main())
