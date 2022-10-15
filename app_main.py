"""
Miguel Antonio H. Germar, 2022
"""

import streamlit as st

# Custom imports for app features
from app_havel_hakimi import feature_havel_hakimi


if __name__ == "__main__":

    emoji = ":books:"

    st.set_page_config(
        page_title = "Graph Theory Examples",
        page_icon = emoji,
        initial_sidebar_state = "expanded",
    )

    st.markdown(f"Graph Theory Examples {emoji}")

    with st.sidebar:
        # Radio buttons to select feature
        feature = st.radio(
            "App Feature",
            options = [
                "Havel-Hakimi Technique",
                "Credits"
            ]
        )

    if feature == "Havel-Hakimi Technique":
        feature_havel_hakimi()
    elif feature == "Credits":
        st.markdown("## Credits\n\nThis app was programmed by Miguel Antonio H. Germar in 2022.\n\nThe logic of the app's features was based on this book:\n\nBataller, R., Buot, J., De Lara-Tuprio, E., Garces, I., Garciano, A., & Sarmiento, J. (2019). Chapter 10: Graph Theory and Networks. In Mathematical Ideas and Tools for the Modern World. Vibal Group, Inc.")