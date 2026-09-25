import streamlit as st
import pandas as pd
from iwt_dispute_data import PCA_TIMELINE, INDIA_RELATED_PROJECTS, DISPUTED_METRICS

def render_dispute_tab():
    st.subheader("India-related water infrastructure & IWT dispute")
    st.info("This section records documented proceedings and clearly attributed positions. The requested phrase 'indian atrocities' is not used as a factual characterization.")

    st.markdown("### Chenab-related hydroelectric projects")
    st.dataframe(pd.DataFrame(INDIA_RELATED_PROJECTS), use_container_width=True, hide_index=True)

    st.markdown("### Engineering issues in the Kishanganga/Ratle proceedings")
    st.dataframe(pd.DataFrame(DISPUTED_METRICS), use_container_width=True, hide_index=True)

    st.markdown("### PCA / IWT timeline")
    st.dataframe(pd.DataFrame(PCA_TIMELINE), use_container_width=True, hide_index=True)

    st.markdown("### Party-position fields")
    st.caption("Use these fields for claims such as 'Pakistan argues...' or 'India's position is...' rather than presenting contested allegations as established facts.")

    st.text_area(
        "Pakistan position / source-backed note",
        value="Pakistan's position should be entered with a primary-source citation.",
        height=90,
        key="pakistan_position_note"
    )
    st.text_area(
        "India position / source-backed note",
        value="India's position should be entered with a primary-source citation.",
        height=90,
        key="india_position_note"
    )
