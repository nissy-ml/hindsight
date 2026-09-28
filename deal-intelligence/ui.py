import streamlit as st

from database import (
    create_database,
    create_user,
    login_user
)

from deal_engine import (
    search_deal,
    generate_report,
    learn_from_user,
    answer_question
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Deal Intelligence Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

create_database()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "signup"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "theme" not in st.session_state:
    st.session_state.theme = "light"

if "company" not in st.session_state:
    st.session_state.company = ""

if "memories" not in st.session_state:
    st.session_state.memories = []

if "report" not in st.session_state:
    st.session_state.report = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "deal_loaded" not in st.session_state:
    st.session_state.deal_loaded = False


# ============================================================
# THEME
# ============================================================

def apply_theme():

    if st.session_state.theme == "dark":

        st.markdown(
            """
            <style>

            .stApp {
                background-color: #0e1117;
                color: #ffffff;
            }

            [data-testid="stSidebar"] {
                background-color: #161b22;
            }

            [data-testid="stHeader"] {
                background-color: #0e1117;
            }

            .deal-card {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 14px;
                padding: 20px;
                margin-bottom: 20px;
            }

            .profile-card {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 14px;
                padding: 20px;
            }

            h1, h2, h3, h4, h5, h6 {
                color: #ffffff !important;
            }

            p, label, span, div {
                color: #f5f5f5;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <style>

            .stApp {
                background-color: #f7f9fc;
                color: #111827;
            }

            [data-testid="stSidebar"] {
                background-color: #ffffff;
            }

            [data-testid="stHeader"] {
                background-color: #f7f9fc;
            }

            .deal-card {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 14px;
                padding: 20px;
                margin-bottom: 20px;
            }

            .profile-card {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 14px;
                padding: 20px;
            }

            h1, h2, h3, h4, h5, h6 {
                color: #111827 !important;
            }

            p, label, span, div {
                color: #111827;
            }

            </style>
            """,
            unsafe_allow_html=True
        )


apply_theme()


# ============================================================
# SIGNUP PAGE
# ============================================================

def signup_page():

    st.markdown(
        "<h1 style='text-align:center;'>🤖 Deal Intelligence Agent</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Create your account to manage and analyze sales deals</p>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 6 characters"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        st.write("")

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.error(
                    "Please fill in all required fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                success = create_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Account created successfully! 🎉"
                    )

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    st.error(
                        "An account with this email already exists."
                    )

        st.write("")

        if st.button(
            "Already have an account? Login",
            use_container_width=True
        ):

            st.session_state.page = "login"

            st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.markdown(
        "<h1 style='text-align:center;'>🤖 Deal Intelligence Agent</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>Welcome back</p>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("Login")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        st.write("")

        if st.button(
            "Login",
            type="primary",
            use_container_width=True
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_name = user[1]
                st.session_state.user_email = email
                st.session_state.page = "dashboard"

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

        st.write("")

        if st.button(
            "Don't have an account? Sign Up",
            use_container_width=True
        ):

            st.session_state.page = "signup"

            st.rerun()


# ============================================================
# PROFILE + SETTINGS
# ============================================================

def profile_section():

    st.sidebar.markdown("## 👤 Profile")

    st.sidebar.markdown(
        f"**Name:** {st.session_state.user_name}"
    )

    st.sidebar.markdown(
        f"**Email:** {st.session_state.user_email}"
    )

    st.sidebar.divider()

    st.sidebar.markdown("## 🎨 Appearance")

    if st.session_state.theme == "light":

        if st.sidebar.button(
            "🌙 Switch to Dark Mode",
            use_container_width=True
        ):

            st.session_state.theme = "dark"

            st.rerun()

    else:

        if st.sidebar.button(
            "☀️ Switch to Light Mode",
            use_container_width=True
        ):

            st.session_state.theme = "light"

            st.rerun()

    st.sidebar.divider()

    st.sidebar.markdown("### 🤖 Agent")

    st.sidebar.caption(
        "Your selected deal, conversation history "
        "and current session are kept while you work."
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.page = "login"

        st.session_state.company = ""
        st.session_state.memories = []
        st.session_state.report = ""
        st.session_state.chat_history = []
        st.session_state.deal_loaded = False

        st.rerun()


# ============================================================
# DEAL SEARCH
# ============================================================

def deal_search_section():

    st.header("🔎 Select a Deal")

    st.write(
        "Enter the company name or deal name to retrieve "
        "the information stored in the agent's memory."
    )

    company = st.text_input(
        "Company / Deal Name",
        value=st.session_state.company,
        placeholder="Example: Acme Corporation"
    )

    if st.button(
        "🔎 Load Deal",
        type="primary",
        use_container_width=True
    ):

        company = company.strip()

        if not company:

            st.error(
                "Please enter a company or deal name."
            )

            return

        with st.spinner(
            "🔎 Searching the deal memory..."
        ):

            memories = search_deal(company)

        if not memories:

            st.error(
                f"No relevant information was found "
                f"for '{company}'."
            )

            st.session_state.deal_loaded = False

            return

        st.session_state.company = company
        st.session_state.memories = memories
        st.session_state.chat_history = []
        st.session_state.deal_loaded = True

        with st.spinner(
            "🧠 Building the deal intelligence report..."
        ):

            report = generate_report(
                company,
                memories
            )

        if report:

            st.session_state.report = report

        else:

            st.session_state.report = ""

        st.success(
            f"✅ {company} loaded successfully."
        )

        st.rerun()


# ============================================================
# DEAL REPORT
# ============================================================

def show_deal_report():

    if not st.session_state.deal_loaded:
        return

    st.divider()

    st.header(
        f"📊 Deal Intelligence Report — "
        f"{st.session_state.company}"
    )

    # --------------------------------------------------------
    # RETRIEVED MEMORY
    # --------------------------------------------------------

    with st.expander(
        "🔎 View Retrieved Deal Memory",
        expanded=False
    ):

        if st.session_state.memories:

            for index, memory in enumerate(
                st.session_state.memories,
                start=1
            ):

                st.markdown(
                    f"### Memory {index}"
                )

                st.write(memory)

        else:

            st.info(
                "No previous memory was retrieved."
            )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    st.subheader(
        "🤖 AI Deal Analysis"
    )

    if st.session_state.report:

        st.markdown(
            st.session_state.report
        )

    else:

        st.warning(
            "The AI report could not be generated right now. "
            "The deal memory is still available below."
        )


# ============================================================
# CHAT WITH DEAL AGENT
# ============================================================

def deal_chat():

    if not st.session_state.deal_loaded:
        return

    st.divider()

    st.header(
        "💬 Talk to Your Deal Intelligence Agent"
    )

    st.write(
        "Ask questions about the selected deal. "
        "You can ask about pricing, risks, customer needs, "
        "competitors, buying signals, next actions and more."
    )

    st.info(
        "💡 If your message contains useful new deal "
        "information, the agent will attempt to remember it."
    )

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    for chat in st.session_state.chat_history:

        if chat["role"] == "user":

            with st.chat_message("user"):

                st.write(
                    chat["content"]
                )

        else:

            with st.chat_message("assistant"):

                st.markdown(
                    chat["content"]
                )

    # --------------------------------------------------------
    # QUESTION INPUT
    # --------------------------------------------------------

    question = st.chat_input(
        f"Ask anything about {st.session_state.company}..."
    )

    if not question:
        return

    question = question.strip()

    # --------------------------------------------------------
    # STORE USER MESSAGE IN SESSION
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.write(question)

    # --------------------------------------------------------
    # LEARN FROM USER MESSAGE
    # --------------------------------------------------------

    learned = False

    with st.spinner(
        "🧠 Checking for useful new deal information..."
    ):

        try:

            learned = learn_from_user(
                st.session_state.company,
                question
            )

        except Exception as e:

            st.warning(
                "The agent could not update its long-term "
                "memory right now."
            )

    # --------------------------------------------------------
    # REFRESH MEMORY IF SOMETHING NEW WAS LEARNED
    # --------------------------------------------------------

    if learned:

        with st.spinner(
            "🔄 Refreshing deal memory..."
        ):

            try:

                updated_memories = search_deal(
                    st.session_state.company
                )

                if updated_memories:

                    st.session_state.memories = updated_memories

            except Exception:

                pass

    # --------------------------------------------------------
    # ANSWER QUESTION
    # --------------------------------------------------------

    answer = None

    with st.spinner(
        "🤖 Preparing your answer..."
    ):

        try:

            answer = answer_question(
                st.session_state.company,
                st.session_state.memories,
                question
            )

        except Exception:

            answer = None

    # --------------------------------------------------------
    # FALLBACK IF LLM IS UNAVAILABLE
    # --------------------------------------------------------

    if not answer:

        if st.session_state.memories:

            answer = (
                "⚠️ I couldn't generate an AI response "
                "right now. This can happen if the LLM "
                "provider has temporarily reached its quota.\n\n"
                "Here is the relevant information currently "
                "stored in the deal memory:\n\n"
            )

            for memory in st.session_state.memories[:8]:

                answer += f"• {memory}\n\n"

        else:

            answer = (
                "I couldn't find relevant information "
                "for this deal."
            )

    # --------------------------------------------------------
    # STORE ASSISTANT RESPONSE
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        st.markdown(answer)

    # --------------------------------------------------------
    # LEARNING NOTIFICATION
    # --------------------------------------------------------

    if learned:

        st.success(
            "🧠 New useful deal information was detected "
            "and stored in the agent's memory."
        )


# ============================================================
# FINAL INSIGHTS
# ============================================================

def final_insights():

    if not st.session_state.deal_loaded:
        return

    if len(st.session_state.chat_history) == 0:
        return

    st.divider()

    st.header(
        "📌 Deal Summary"
    )

    st.write(
        "You have finished interacting with the current "
        "deal. Use the report and conversation above to "
        "review the most important information."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 🧠 Key Insights

            Review the **Key Insights** section of the
            generated deal report for the most important
            observations supported by the available memory.
            """
        )

    with col2:

        st.markdown(
            """
            ### 🚀 Recommended Next Actions

            Review the **Recommended Next Actions** section
            of the report for practical actions based on
            the available deal information.
            """
        )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    profile_section()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.title(
            "🎯 Deal Intelligence Dashboard"
        )

        st.write(
            "Your AI-powered sales memory and deal "
            "intelligence workspace."
        )

    with col2:

        st.markdown(
            f"""
            <div style="
                text-align:right;
                padding-top:25px;
                font-size:18px;
                font-weight:600;
            ">
                👤 {st.session_state.user_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------------
    # DEAL SEARCH
    # --------------------------------------------------------

    deal_search_section()

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    show_deal_report()

    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------

    deal_chat()

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    final_insights()


# ============================================================
# PAGE ROUTING
# ============================================================

if not st.session_state.logged_in:

    if st.session_state.page == "signup":

        signup_page()

    else:

        login_page()

else:

    dashboard_page()