"""
Lightweight, session-based login and role selection.

This is NOT a production authentication system — there is no password
database or persistent storage. It captures who is using the app in this
session (name + role + a couple of context questions) so the UI and
workflow can adapt to Student vs. Recruiter needs. Swap in a real auth
provider (e.g. OAuth, a users table) for production use.
"""

import streamlit as st

ROLE_STUDENT = "Student / Job Seeker"
ROLE_RECRUITER = "Recruiter / Hiring Manager"


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def logout():
    for key in ["authenticated", "user_name", "user_role", "user_context"]:
        st.session_state.pop(key, None)


def render_login(job_titles: list):
    """Render the login / onboarding form. Sets session state on submit."""

    st.markdown(
        """
        <div class="login-hero">
            <h1>🌸 Welcome to SkillMatch AI</h1>
            <p>Explainable AI-powered resume screening &amp; job matching</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 2, 1])
    with center:
        with st.form("login_form", border=True):
            st.markdown("#### Let's get to know you")
            name = st.text_input("Your name", placeholder="e.g. Ananya Sharma")
            email = st.text_input("Email (optional)", placeholder="you@example.com")

            role = st.radio(
                "I am here as a...",
                [ROLE_STUDENT, ROLE_RECRUITER],
                horizontal=True,
            )

            context = {}
            if role == ROLE_STUDENT:
                context["target_role"] = st.selectbox(
                    "Which job role are you targeting?", job_titles
                )
                context["experience_level"] = st.radio(
                    "Experience level", ["Fresher / Student", "Experienced"], horizontal=True
                )
            else:
                context["company_name"] = st.text_input(
                    "Company / Organization name", placeholder="e.g. Acme Corp"
                )
                context["hiring_for"] = st.selectbox(
                    "Which role are you hiring for?", job_titles
                )

            submitted = st.form_submit_button("Continue →", use_container_width=True, type="primary")

            if submitted:
                if not name.strip():
                    st.warning("Please enter your name to continue.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.user_name = name.strip()
                    st.session_state.user_email = email.strip()
                    st.session_state.user_role = role
                    st.session_state.user_context = context
                    st.rerun()
