import streamlit as st
from streamlit.logger import get_logger
from streamlit_navigation_bar import st_navbar
import pages as pg


LOGGER = get_logger(__name__)
st.set_page_config(
      page_title="Research Radar AI",
      page_icon=":satellite:",
      initial_sidebar_state="collapsed"
  )

styles = {
	"nav": {
		"background-color": "#ffb900",
	},
	"active": {
		"background-color": "#efaa05",
		"color": "var(--text-color)",
		"font-weight": "normal",
		"padding": "14px",
	}
}

def run():
   
    page = st_navbar(["Home", "Research"],styles=styles)
    functions = {
      "Research": pg.show_research
    }
    go_to = functions.get(page)
    if go_to:
      go_to()
    else:
      st.write("# Welcome ! 👋")
      st.image("static/logo/Research_Radar.png")
      st.markdown(
        f"""
        <style>
        img {{
            border-radius: 15px;
            box-shadow: 0 0 10px #000000;
            height: auto;
            width: 50%;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
      st.write("Research Radar AI ")
      markdown_text = """
      # Research Radar AI :satellite:
      Welcome to **Research Radar AI**, an innovative application designed by Aviral 👨‍💻 - [Check out my GitHub](https://github.com/error9098x)

      Are you on a quest for the latest research papers? :mag_right: Look no further, because **Research Radar AI** is here to assist you! 

      Explore the freshest scholarly articles from [arXiv.org](https://arxiv.org), an authoritative source for scientific papers. Our app doesn't just find cutting-edge research; it also bridges the conversation with the very papers that pique your interest. :speech_balloon:

      Leveraging the power of the **Gemini Pro model**, you can interact with the research papers at a level of detail that feels like chatting with the authors themselves! Adjust the slider to tweak the Gemini Pro's response 'temperature' for more or less creativity in the responses. :thermometer:

      But wait, there's more! :sparkles:

      Want to keep a collection of these intriguing papers? We understand the importance of saving them for later review. With our seamless email feature, you can have all the selected research summaries delivered directly to your inbox. :inbox_tray:

      Get started on your scholarly exploration with **Research Radar AI** today! :rocket:
      """

      st.markdown(markdown_text)


if __name__ == "__main__":
    run()
