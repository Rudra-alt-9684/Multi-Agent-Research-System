
import streamlit as st
from datetime import datetime

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


st.set_page_config(
    page_title="ORBIT AI",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #0b1020;
    color: #e5e7eb;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #26334d;
}

.hero {
    padding: 30px;
    border: 1px solid #373568;
    border-radius: 20px;
    background: linear-gradient(120deg, #171b38, #111a30, #20163b);
    margin-bottom: 24px;
}

.hero h1 {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
    color: #ffffff;
}

.hero p {
    color: #a5b4fc;
    font-size: 15px;
}

.metric-card {
    background: #111a2e;
    border: 1px solid #283550;
    border-radius: 14px;
    padding: 18px;
    min-height: 100px;
}

.metric-card small {
    color: #9ca3af;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 25px 0 14px 0;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: linear-gradient(90deg, #7c3aed, #6366f1);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    border: 1px solid #a78bfa;
    color: white;
}

.stTextArea textarea,
.stTextInput input {
    background: #111a2e;
    color: #e5e7eb;
    border: 1px solid #34415e;
    border-radius: 10px;
}

[data-testid="stExpander"] {
    border: 1px solid #283550;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    color: #c4b5fd;
}

hr {
    border-color: #26334d;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "result" not in st.session_state:
    st.session_state.result = None


def show_step(number: int, message: str):
    st.markdown(
        f"### Step {number}/4 — {message}"
    )


def run_research_pipeline(topic: str):
    """Run the search, reader, writer, and critic agents."""

    state = {"topic": topic}

    progress = st.progress(0)
    status = st.empty()

    try:
        show_step(1, "Search Agent")

        with st.status(
            "Searching for reliable information...",
            expanded=True,
        ) as step:
            search_agent = build_search_agent()

            search_result = search_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"Research this topic: {topic}\n"
                        "Find recent, reliable, detailed information. "
                        "Include source URLs, dates, and relevant facts. "
                        "Do not invent sources."
                    )
                ]
            })

            state["search_results"] = (
                search_result["messages"][-1].content
            )

            step.update(
                label="Search completed",
                state="complete",
                expanded=False,
            )

        progress.progress(25)

        show_step(2, "Reader Agent")

        with st.status(
            "Reading relevant sources...",
            expanded=True,
        ) as step:
            reader_agent = build_reader_agent()

            reader_result = reader_agent.invoke({
                "messages": [
                    (
                        "user",
                        f"Research topic: {topic}\n\n"
                        "Select the most relevant URLs from the "
                        "search results below. Extract useful facts, "
                        "dates, evidence, and source URLs. "
                        "Clearly mention inaccessible sources. "
                        "Do not invent facts.\n\n"
                        f"Search results:\n"
                        f"{state['search_results'][:8000]}"
                    )
                ]
            })

            state["scraped_content"] = (
                reader_result["messages"][-1].content
            )

            step.update(
                label="Source reading completed",
                state="complete",
                expanded=False,
            )

        progress.progress(50)

        research = (
            f"TOPIC:\n{topic}\n\n"
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SOURCE CONTENT:\n{state['scraped_content']}"
        )


        show_step(3, "Writing Report")

        with st.status(
            "Generating the research report...",
            expanded=True,
        ) as step:
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research,
            })

            step.update(
                label="Report generated",
                state="complete",
                expanded=False,
            )

        progress.progress(75)

        show_step(4, "Critic Agent")

        with st.status(
            "Reviewing the report...",
            expanded=True,
        ) as step:
            state["feedback"] = critic_chain.invoke({
                "report": state["report"],
            })

            step.update(
                label="Review completed",
                state="complete",
                expanded=False,
            )

        progress.progress(100)
        status.success("Research completed successfully!")

        state["created_at"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return state

    except Exception as error:
        status.error(f"Research failed: {error}")
        st.exception(error)
        return None


def display_report(result: dict):
    """Display report, source results, and critique."""

    st.divider()

    st.markdown("## 📄 Research Results")
    st.caption(
        f"Topic: {result['topic']} · "
        f"Created: {result.get('created_at', 'Unknown')}"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📑 Final Report",
        "🔎 Search Results",
        "📚 Reader Output",
        "🧠 Critic Feedback",
    ])

    with tab1:
        st.markdown(result["report"])

        markdown_report = (
            f"# {result['topic']}\n\n"
            f"{result['report']}\n\n"
            f"## Critic Feedback\n\n{result['feedback']}"
        )

        st.download_button(
            label="⬇️ Download Report (.md)",
            data=markdown_report,
            file_name="orbit_research_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

        full_report = (
            f"ORBIT AI RESEARCH REPORT\n"
            f"Topic: {result['topic']}\n"
            f"Created: {result.get('created_at', '')}\n\n"
            f"{'=' * 50}\n"
            f"SEARCH RESULTS\n{'=' * 50}\n"
            f"{result['search_results']}\n\n"
            f"{'=' * 50}\n"
            f"READER OUTPUT\n{'=' * 50}\n"
            f"{result['scraped_content']}\n\n"
            f"{'=' * 50}\n"
            f"FINAL REPORT\n{'=' * 50}\n"
            f"{result['report']}\n\n"
            f"{'=' * 50}\n"
            f"CRITIC FEEDBACK\n{'=' * 50}\n"
            f"{result['feedback']}"
        )

        st.download_button(
            label="⬇️ Download Full Research (.txt)",
            data=full_report,
            file_name="orbit_full_research.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with tab2:
        st.markdown(result["search_results"])

    with tab3:
        st.markdown(result["scraped_content"])

    with tab4:
        st.markdown(result["feedback"])



with st.sidebar:
    st.markdown("## 🔭 ORBIT AI")
    st.caption("MULTI-AGENT RESEARCH SYSTEM")

    st.divider()

    page = st.radio(
        "Navigation",
        ["New Research", "Research History", "About"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### ⚙️ Workflow")
    st.markdown("""
    🔎 Search Agent

    📚 Reader Agent

    ✍️ Writer

    🧠 Critic
    """)

    st.caption("Powered by Python, Streamlit and LangChain.")

    if st.button("🗑️ Clear Research History"):
        st.session_state.research_history = []
        st.session_state.result = None
        st.rerun()



if page == "New Research":

    # Static app branding — never uses the research topic
    st.markdown("""
    <div class="hero">
        <h1>🔭 ORBIT AI</h1>
        <p>Your intelligent multi-agent research workspace.</p>
        <p>Search. Read. Synthesize. Review.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔎 Search</h3>
            <small>Discover relevant information</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 Read</h3>
            <small>Explore detailed sources</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>✍️ Write</h3>
            <small>Generate a research report</small>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🧠 Review</h3>
            <small>Evaluate report quality</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Start a Research Task</div>',
        unsafe_allow_html=True,
    )

    with st.form("research_form"):
        topic = st.text_area(
            "What would you like to research?",
            placeholder=(
                "Example: The impact of AI agents on data "
                "engineering in 2026"
            ),
            height=110,
        )

        submitted = st.form_submit_button(
            "🚀 Start Research",
            use_container_width=True,
        )

    if submitted:
        if not topic.strip():
            st.warning("Please enter a research topic.")
        else:
            result = run_research_pipeline(topic.strip())

            if result:
                st.session_state.result = result
                st.session_state.research_history.insert(0, result)

    if st.session_state.result:
        display_report(st.session_state.result)



elif page == "Research History":

    st.markdown("""
    <div class="hero">
        <h1>📚 Research History</h1>
        <p>Review reports generated during this session.</p>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.research_history

    if not history:
        st.info("No research reports yet. Start a new research task.")
    else:
        st.caption(f"{len(history)} research task(s)")

        for index, item in enumerate(history):
            with st.expander(
                f"📄 {item['topic']} — "
                f"{item.get('created_at', '')}"
            ):
                st.markdown(item["report"])

                st.download_button(
                    "⬇️ Download this report",
                    data=(
                        f"# {item['topic']}\n\n"
                        f"{item['report']}\n\n"
                        f"## Critic Feedback\n\n"
                        f"{item['feedback']}"
                    ),
                    file_name=f"orbit_report_{index + 1}.md",
                    mime="text/markdown",
                    key=f"download_history_{index}",
                )

                if st.button(
                    "Open this report",
                    key=f"open_history_{index}",
                ):
                    st.session_state.result = item
                    st.session_state.open_history_report = True
                    st.success(
                        "Report selected. Open New Research "
                        "to view its complete tabs."
                    )


elif page == "About":

    st.markdown("""
    <div class="hero">
        <h1>🔭 About ORBIT AI</h1>
        <p>A multi-agent system for structured research and reporting.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### How it works")

    st.markdown("""
    **1. Search Agent**

    Finds relevant information using your configured search tools.

    **2. Reader Agent**

    Selects relevant URLs and extracts deeper information.

    **3. Writer**

    Combines the available research into a structured report.

    **4. Critic**

    Reviews the generated report and provides feedback.
    """)

    st.markdown("### Technology Stack")

    st.markdown("""
    - Python
    - Streamlit
    - LangChain
    - Groq or another supported LLM provider
    - Web search and webpage scraping tools
    """)

    st.info(
        "ORBIT AI displays the output produced by your agents. "
        "Source accuracy depends on the underlying search and reader tools."
    )
