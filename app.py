"""
The Investigator — SOC Copilot (Week 6)
A Streamlit app that correlates multiple log sources into one verdict using a
hosted LLM (Groq / Llama 3.3 70B).

You don't have to WRITE this app — but a tool you can't explain is a tool you
can't trust, so read it. The pieces worth understanding are marked  #->
"""

import os

import streamlit as st
from groq import Groq
from datetime import datetime

# #-> The model, and the system prompt that defines the analyst's job. The
#     five numbered sections are exactly what the Copilot must return.
MODEL = "llama-3.3-70b-versatile"

CORRELATION_SYSTEM_PROMPT = """You are a senior SOC analyst. You are given one or
more raw log files from a single environment. Correlate them into ONE incident and
produce a Markdown report with these exact sections:

## 1. Threat Analysis
What happened, the attack chain in order, and the hosts, accounts, and IPs involved.

## 2. MITRE ATT&CK Mapping
For each finding: tactic, technique name, and technique ID (e.g., T1059).

## 3. Severity
One of Low / Medium / High / Critical, with a one-line justification.

## 4. Investigation Plan
Concrete next steps to confirm scope.

## 5. Response Plan
Containment, eradication, and recovery steps.

Cite the specific log evidence for each claim. If something is uncertain, say so —
do not invent technique IDs or events that are not present in the logs."""


# #-> The ONE function that talks to the AI. Both tabs call this.
def ask_groq(messages):
    try:
        resp = client.chat.completions.create(model=MODEL, messages=messages)
        return resp.choices[0].message.content
    except Exception as e:
        err = str(e)
        if "401" in err or "invalid_api_key" in err:
            return (
                "⚠️ Groq rejected the API key (401 Invalid API Key). "
                "Confirm your full key from https://console.groq.com/keys, then reload."
            )
        return f"⚠️ Groq request failed: {e}"


def is_valid_groq_key(key):
    return bool(key and key.startswith("gsk_") and len(key) >= 40)


st.set_page_config(page_title="The Investigator — SOC Copilot", page_icon="🕵️")

# #-> Prefer a valid session key, then st.secrets, then the environment.
groq_api_key = ""
for candidate in (
    st.session_state.get("groq_api_key", ""),
    (st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY") or "").strip(),
):
    if is_valid_groq_key(candidate):
        groq_api_key = candidate
        break

if not is_valid_groq_key(groq_api_key):
    st.warning("Groq API key is missing or incomplete.")
    st.caption(
        "`.streamlit/secrets.toml` in this environment still contains only the `gsk_` prefix. "
        "Paste your **full** key from https://console.groq.com/keys below "
        "(stored for this browser session only)."
    )
    entered = st.text_input("Groq API Key", type="password")
    if entered:
        entered = entered.strip()
        if is_valid_groq_key(entered):
            st.session_state.groq_api_key = entered
            st.rerun()
        else:
            st.error(f"Key looks incomplete ({len(entered)} characters). Paste the full key.")
    st.stop()

client = Groq(api_key=groq_api_key)

st.title("🕵️ The Investigator — SOC Copilot")

tab1, tab2 = st.tabs(["Correlate & Triage", "Ask the Investigator"])

# ---------------------------------------------------------------------------
# TAB 1 — Correlate & Triage
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Correlate & Triage")
    st.caption("Upload one or more logs. The Copilot correlates them into a single verdict.")

    # #-> A counter lets "Start new analysis" reset the uploader by changing its key.
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    uploaded = st.file_uploader(
        "Upload log files",
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.uploader_key}",
    )

    if st.button("Run correlation", disabled=not uploaded):
        # #-> Concatenate every uploaded file, labeled by filename, into one prompt.
        combined = ""
        for f in uploaded:
            text = f.read().decode("utf-8", errors="ignore")
            combined += f"\n\n===== {f.name} =====\n{text}"
        with st.spinner("Correlating across sources..."):
            st.session_state.report = ask_groq([
                {"role": "system", "content": CORRELATION_SYSTEM_PROMPT},
                {"role": "user", "content": combined},
            ])

    # #-> Show the report from session_state so it survives reruns (download/reset).
    if st.session_state.get("report"):
        st.markdown(st.session_state.report)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        st.download_button(
            "⬇️ Download report",
            st.session_state.report,
            file_name=f"triage_report_{stamp}.md",
        )
        if st.button("Start new analysis"):
            st.session_state.pop("report", None)
            st.session_state.uploader_key += 1   # forces a fresh, empty uploader
            st.rerun()

# ---------------------------------------------------------------------------
# TAB 2 — Ask the Investigator (chat)
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Ask the Investigator")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    # #-> Replay the conversation so far.
    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).markdown(msg["content"])

    question = st.chat_input("Ask about the case or SOC analysis...")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        st.chat_message("user").markdown(question)
        with st.spinner("Thinking..."):
            answer = ask_groq(
                [{"role": "system",
                  "content": "You are a senior SOC analyst helping a colleague. Be concise and precise."}]
                + st.session_state.chat
            )
        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").markdown(answer)
