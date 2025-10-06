
# Add comprehensive error handling
import logging
import sys
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def handle_errors(func):
    """Decorator for error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


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
