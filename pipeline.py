
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


def show_step(step: int, message: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"STEP {step} - {message}")
    print("=" * 50)


def run_research_pipeline(topic: str) -> dict:
    """Run the complete research and report pipeline."""

    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    state = {}

    try:
        # Step 1: Search
        show_step(1, "Search Agent")

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable, and detailed information about: {topic}")
            ]
        })

        state["search_results"] = search_result["messages"][-1].content
        print(state["search_results"])

        # Step 2: Read and scrape
        show_step(2, "Reader Agent")

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [
                ("user",
                 f"Research topic: {topic}\n"
                 "Choose the most relevant URL from these search results "
                 "and extract useful details from the page.\n\n"
                 f"Search results:\n{state['search_results'][:800]}")
            ]
        })

        state["scraped_content"] = reader_result["messages"][-1].content
        print(state["scraped_content"])

        # Combine research
        research = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"SCRAPED CONTENT:\n{state['scraped_content']}"
        )

        # Step 3: Write report
        show_step(3, "Writing Report")

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research,
        })

        print(state["report"])

        # Step 4: Critique
        show_step(4, "Reviewing Report")

        state["feedback"] = critic_chain.invoke({
            "report": state["report"],
        })

        print(state["feedback"])

        return state

    except Exception as error:
        print(f"\nResearch pipeline failed: {error}")
        raise


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip()

    if topic:
        result = run_research_pipeline(topic)
    else:
        print("Please enter a valid topic.")


