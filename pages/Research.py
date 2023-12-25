import datetime
import streamlit as st
from utils import categories
from Component.fetch_arxiv import fetch_arxiv_papers, extract_paper_information
from Component.genai import get_conversational_chain, get_text_chunks, get_vector_store, get_pdf_content_and_parse, user_input
from jinja2 import Environment, FileSystemLoader, select_autoescape
import time
from Component.helper import send_email 
from Component.constants import SENDER_ADDRESS, SENDER_PASSWORD, SMTP_SERVER_ADDRESS, PORT

def show_research():
	st.header("Let's Research")
	env = Environment(
            loader=FileSystemLoader('./templates'),  # Set the path to your templates directory
            autoescape=select_autoescape(['html', 'xml'])
        )
	
	category = st.selectbox(
		"Select a research topic",
		list(categories.keys()),
		format_func=lambda x: categories[x]
	)
	#make a createive temparture slider
	temp = st.slider("LLM Creativity Slider 🎨", 0.0, 1.0, 0.5, 0.1)
	if st.button('Fetch Papers'):
		with st.spinner('Fetching papers...'):
			xml_result = fetch_arxiv_papers(category)
			papers = extract_paper_information(xml_result)
			st.session_state['papers'] = papers  # Store papers in session_state
			
			st.success(f'Fetched top 10 papers on {categories[category]}!')

	if 'papers' in st.session_state:
		st.subheader(f'Top 10 most recent papers on {categories[category]}')
		for i, paper in enumerate(st.session_state['papers'], start=1):
			with st.spinner(f'Retrieving Data from Papers..'):
				with st.expander(f"{i}. {paper['title']}"):
					st.markdown(paper['summary'])
					st.markdown(f"[Read more]({paper['url']})")
					arxiv_id = paper['url'].split('/')[-1]
					# st.write("Ask a Question about the Paper:")
					user_question = st.text_input("Chat With LLM About "+paper['title'])
					if user_question:
						with st.spinner(f'Parsing Research Paper... Retriving from https://arxiv.org/pdf/{arxiv_id}.pdf'):
							#time.sleep(3)
							get_pdf_content_and_parse(f"https://arxiv.org/pdf/{arxiv_id}.pdf")
							user_input(user_question,temp)

	if 'papers' in st.session_state:
		#leave space
		st.write("")
		#markdown about write your email to get the summary
		st.markdown("# Get the Summary of the Papers in your Email 📬")

		with st.form(key='send_email_form'):
			recipient_email = st.text_input("Recipient Email", key='recipient_email_input')
			submit_button = st.form_submit_button(label='Send Email')
			if submit_button and recipient_email:
				st.success('Sending email...')
				# Render the email template
				template = env.get_template('email_template.html')
				email_message = template.render(subject = "Here is Your "+categories[category]+" Research Papers Summary !",
papers=st.session_state.papers, current_year=datetime.datetime.now().year)
				subject = "We Have Prepared The Research Papers Summary !"
				# Send the email
				try:
					send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD,
				receiver=recipient_email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT,
				email_message=email_message, subject=subject, attachment=False, is_html=True)
					st.success('Email sent successfully!')
					st.balloons()
				except Exception as e:
					st.error(f'An error occurred: {e}')

	# Helper to clear the session state when needed
	def clear_state():
		for key in list(st.session_state.keys()):
			del st.session_state[key]

	# Add a button to clear the fetched papers if necessary
	st.button("Clear Papers", on_click=clear_state)

