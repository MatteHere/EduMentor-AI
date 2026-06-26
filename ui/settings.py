import streamlit as st

from services.provider_manager import get_available_providers


def render_settings_page():
    st.markdown('<div class="hero-title">Settings</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Configure EduMentor AI behavior and AI provider settings.
        </div>
        """,
        unsafe_allow_html=True
    )

    providers = get_available_providers()

    provider_keys = list(providers.keys())
    provider_labels = [providers[key] for key in provider_keys]

    current_provider = st.session_state["selected_provider"]

    if current_provider in provider_keys:
        current_index = provider_keys.index(current_provider)
    else:
        current_index = 0

    selected_label = st.radio(
        "Choose AI Provider",
        provider_labels,
        index=current_index
    )

    selected_provider = provider_keys[provider_labels.index(selected_label)]
    st.session_state["selected_provider"] = selected_provider

    st.markdown('<div class="section-title">Current Provider</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="premium-card">
        <div class="card-title">⚙ {selected_label}</div>
        <div class="card-text">
            Auto mode uses Groq first for speed and Gemini as backup.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("Provider changes apply to future AI generations.")