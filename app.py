import streamlit as st
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="FileVault | File Handling System",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

WORKDIR = Path("user_files")
WORKDIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# STYLING
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    #MainMenu, footer, header {visibility: hidden;}

    .hero {
        padding: 1.6rem 2rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.25);
    }
    .hero h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
    }
    .hero p {
        color: rgba(255,255,255,0.9);
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.8rem 1rem;
        border-radius: 12px;
    }

    .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.04);
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        color: #cbd5e1;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(139, 92, 246, 0.25) !important;
        color: white !important;
        font-weight: 600;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        border: none;
        padding: 0.55rem 1.2rem;
        transition: transform 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
    }

    section[data-testid="stSidebar"] {
        background: #0b1120;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def list_files():

    
    return sorted([p for p in WORKDIR.iterdir() if p.is_file()])


def human_size(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def flash(msg, kind="success"):
    getattr(st, kind)(msg)


# ---------------------------------------------------------------------------
# HERO HEADER
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🗂️ FileVault</h1>
        <p>A simple, elegant Streamlit UI for Create • Read • Update • Delete file operations</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SIDEBAR — FILE EXPLORER
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📁 Workspace")
    st.caption(f"All files live in `./{WORKDIR}/`")

    files = list_files()
    c1, c2 = st.columns(2)
    c1.metric("Files", len(files))
    c2.metric("Total Size", human_size(sum(f.stat().st_size for f in files)) if files else "0 B")

    st.markdown("---")
    st.markdown("### 📄 Files")
    if files:
        for f in files:
            stat = f.stat()
            with st.expander(f"📄 {f.name}"):
                st.caption(f"Size: {human_size(stat.st_size)}")
                st.caption(f"Modified: {datetime.fromtimestamp(stat.st_mtime):%Y-%m-%d %H:%M}")
    else:
        st.info("No files yet — create one to get started!")

    st.markdown("---")
    st.caption("Built with ❤️ using Python & Streamlit")

# ---------------------------------------------------------------------------
# MAIN TABS
# ---------------------------------------------------------------------------
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["✨ Create", "👀 Read", "✏️ Update", "🗑️ Delete"]
)

# --- CREATE -----------------------------------------------------------------
with tab_create:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Create a new file")

    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="create_name")
    content = st.text_area("File content", placeholder="Start typing...", height=200, key="create_content")

    if st.button("🚀 Create File", type="primary"):
        if not filename.strip():
            flash("Please enter a file name.", "warning")
        else:
            path = WORKDIR / filename.strip()
            if path.exists():
                flash(f"⚠️ A file named '{filename}' already exists.", "error")
            else:
                try:
                    path.write_text(content)
                    flash(f"✅ '{filename}' created successfully!")
                    st.rerun()
                except Exception as err:
                    flash(f"Error occurred: {err}", "error")
    st.markdown("</div>", unsafe_allow_html=True)

# --- READ ---------------------------------------------------------------
with tab_read:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Read a file")

    files = list_files()
    if not files:
        st.info("No files available to read yet.")
    else:
        choice = st.selectbox("Select a file", [f.name for f in files], key="read_choice")
        if choice:
            path = WORKDIR / choice
            try:
                text = path.read_text()
                st.code(text if text.strip() else "(this file is empty)", language=None)
                st.download_button("⬇️ Download", data=text, file_name=choice)
            except Exception as err:
                flash(f"Error occurred: {err}", "error")
    st.markdown("</div>", unsafe_allow_html=True)

# --- UPDATE -------------------------------------------------------------
with tab_update:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Update a file")

    files = list_files()
    if not files:
        st.info("No files available to update yet.")
    else:
        choice = st.selectbox("Select a file", [f.name for f in files], key="update_choice")
        operation = st.radio(
            "Choose operation",
            ["Rename", "Append text", "Overwrite"],
            horizontal=True,
        )
        path = WORKDIR / choice

        if operation == "Rename":
            new_name = st.text_input("New file name", key="rename_input")
            if st.button("✏️ Rename", type="primary"):
                new_path = WORKDIR / new_name.strip()
                if not new_name.strip():
                    flash("Please enter a new name.", "warning")
                elif new_path.exists():
                    flash("A file with that name already exists.", "error")
                else:
                    try:
                        path.rename(new_path)
                        flash(f"✅ Renamed to '{new_name}'")
                        st.rerun()
                    except Exception as err:
                        flash(f"Error occurred: {err}", "error")

        elif operation == "Append text":
            extra = st.text_area("Text to append", height=140, key="append_input")
            if st.button("➕ Append", type="primary"):
                try:
                    with open(path, "a") as f:
                        f.write("\n" + extra)
                    flash("✅ Appended successfully!")
                except Exception as err:
                    flash(f"Error occurred: {err}", "error")

        elif operation == "Overwrite":
            st.warning("This will replace the entire file content.")
            new_content = st.text_area("New content", height=180, key="overwrite_input")
            if st.button("♻️ Overwrite", type="primary"):
                try:
                    path.write_text(new_content)
                    flash("✅ File overwritten successfully!")
                except Exception as err:
                    flash(f"Error occurred: {err}", "error")
    st.markdown("</div>", unsafe_allow_html=True)

# --- DELETE ---------------------------------------------------------------
with tab_delete:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Delete a file")

    files = list_files()
    if not files:
        st.info("No files available to delete yet.")
    else:
        choice = st.selectbox("Select a file to delete", [f.name for f in files], key="delete_choice")
        confirm = st.checkbox(f"I confirm I want to permanently delete '{choice}'")
        if st.button("🗑️ Delete File", type="primary", disabled=not confirm):
            try:
                (WORKDIR / choice).unlink()
                flash(f"✅ '{choice}' deleted successfully!")
                st.rerun()
            except Exception as err:
                flash(f"Error occurred: {err}", "error")
    st.markdown("</div>", unsafe_allow_html=True)
