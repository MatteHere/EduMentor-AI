import streamlit as st

from services.database_service import (
    create_workspace,
    get_workspaces,
    create_subject,
    get_subjects,
)


def reset_workspace_navigation():
    st.session_state["workspace_id"] = None
    st.session_state["workspace_name"] = ""
    st.session_state["subject_id"] = None
    st.session_state["subject_name"] = ""
    st.session_state["unit_id"] = None
    st.session_state["unit_name"] = ""


def open_workspace(workspace_id, workspace_name):
    st.session_state["workspace_id"] = workspace_id
    st.session_state["workspace_name"] = workspace_name
    st.session_state["subject_id"] = None
    st.session_state["subject_name"] = ""
    st.session_state["unit_id"] = None
    st.session_state["unit_name"] = ""


def open_subject(subject_id, subject_name):
    st.session_state["subject_id"] = subject_id
    st.session_state["subject_name"] = subject_name
    st.session_state["unit_id"] = None
    st.session_state["unit_name"] = ""


def render_breadcrumb():
    st.markdown(
        """
        <div style="margin-bottom:20px;color:#475569;font-size:16px;">
            📂 Workspace Browser
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.get("workspace_name"):
        st.markdown(
            f"""
            <div style="margin-bottom:10px;color:#334155;font-size:17px;">
                <b>Workspace:</b> {st.session_state["workspace_name"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.get("subject_name"):
        st.markdown(
            f"""
            <div style="margin-bottom:10px;color:#334155;font-size:17px;">
                <b>Subject:</b> {st.session_state["subject_name"]}
            </div>
            """,
            unsafe_allow_html=True
        )


def render_workspace_card(workspace):
    workspace_id, name, university, stream, semester, created_at = workspace

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">🎓 {name}</div>
            <div class="card-text">
                {university or "University not specified"} • {stream or "Stream not specified"}<br>
                {semester or "Semester not specified"}<br><br>
                <b>Created:</b> {created_at}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Open Workspace", key=f"open_workspace_{workspace_id}"):
        open_workspace(workspace_id, name)
        st.rerun()


def render_subject_card(subject):
    subject_id, subject_name, created_at = subject

    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">📘 {subject_name}</div>
            <div class="card-text">
                Study subject inside <b>{st.session_state["workspace_name"]}</b><br><br>
                <b>Created:</b> {created_at}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Open Subject", key=f"open_subject_{subject_id}"):
        open_subject(subject_id, subject_name)
        st.rerun()


def render_create_workspace():
    with st.expander("➕ Create New Workspace", expanded=False):
        workspace_name = st.text_input(
            "Workspace Name",
            placeholder="Example: Semester III",
            key="new_workspace_name"
        )

        university = st.text_input(
            "University",
            placeholder="Example: SPPU",
            key="new_workspace_university"
        )

        stream = st.text_input(
            "Stream",
            placeholder="Example: AI & DS",
            key="new_workspace_stream"
        )

        semester = st.text_input(
            "Semester",
            placeholder="Example: Semester III",
            key="new_workspace_semester"
        )

        if st.button("Create Workspace", key="create_workspace_button"):
            if not workspace_name.strip():
                st.warning("Please enter a workspace name.")
                return

            workspace_id = create_workspace(
                workspace_name.strip(),
                university.strip(),
                stream.strip(),
                semester.strip()
            )

            open_workspace(workspace_id, workspace_name.strip())
            st.success("✅ Workspace created successfully!")
            st.rerun()


def render_create_subject():
    with st.expander("➕ Add Subject", expanded=False):
        subject_name = st.text_input(
            "Subject Name",
            placeholder="Example: Computer Organization",
            key="new_subject_name"
        )

        if st.button("Create Subject", key="create_subject_button"):
            if not subject_name.strip():
                st.warning("Please enter a subject name.")
                return

            subject_id = create_subject(
                st.session_state["workspace_id"],
                subject_name.strip()
            )

            open_subject(subject_id, subject_name.strip())
            st.success("✅ Subject created successfully!")
            st.rerun()


def render_workspace_list():
    st.markdown('<div class="hero-title">My Workspaces</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-subtitle">
            Choose a semester workspace or create a new one.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_create_workspace()

    workspaces = get_workspaces()

    if not workspaces:
        st.info("No workspaces found. Create your first workspace above.")
        return

    st.markdown('<div class="section-title">Available Workspaces</div>', unsafe_allow_html=True)

    for workspace in workspaces:
        render_workspace_card(workspace)


def render_subject_list():
    st.markdown(
        f'<div class="hero-title">{st.session_state["workspace_name"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Select a subject inside this workspace.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("⬅ Back to Workspaces"):
        reset_workspace_navigation()
        st.rerun()

    render_breadcrumb()
    render_create_subject()

    subjects = get_subjects(st.session_state["workspace_id"])

    if not subjects:
        st.info("No subjects found. Add your first subject above.")
        return

    st.markdown('<div class="section-title">Subjects</div>', unsafe_allow_html=True)

    for subject in subjects:
        render_subject_card(subject)


def render_subject_placeholder():
    st.markdown(
        f'<div class="hero-title">{st.session_state["subject_name"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            Unit and document library will be added in the next step.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("⬅ Back to Subjects"):
        st.session_state["subject_id"] = None
        st.session_state["subject_name"] = ""
        st.rerun()

    render_breadcrumb()

    st.markdown(
        """
        <div class="premium-card">
            <div class="card-title">📄 Next Step</div>
            <div class="card-text">
                We will add Unit Cards and Document Upload here next.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_upload_page():
    if st.session_state.get("subject_id"):
        render_subject_placeholder()
    elif st.session_state.get("workspace_id"):
        render_subject_list()
    else:
        render_workspace_list()