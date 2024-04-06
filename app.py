import streamlit as st
from lida import Manager,TextGenerationConfig,llm
from dotenv import load_dotenv
import os 
import openai
import io
from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai


load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def base64_to_image(base64_string):
    #decode the base64 string 
    byte_data=base64.b64decode(base64_string)

    #use BytesIo to convert the byte data to image
    return Image.open(BytesIO(byte_data))


lida=Manager(text_gen=llm('Google'))
#to load a open source model
# lida=llm(provider='provider_name',model='model_name', device_map='auto')

textgen_config=TextGenerationConfig(n=1,temperature=0.5,model='gemini-pro',use_cache=True)

menu= st.sidebar.selectbox("Chooes an option",["Summarize","Question based Graph"])

if menu == "Summarize":
    st.subheader("Summarization of your data")
    file_uploader = st.file_uploader("Upload your file",type='csv')
    if file_uploader is not None:
        path_to_file="filename.csv"
        with open(path_to_file,'wb') as f:
            f.write(file_uploader.getvalue())
        summary = lida.summarize('filename.csv',summary_method='default',  textgen_config = textgen_config)
        st.write(summary)
        goals = lida.goals(summary,n=2,textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)

        i = 0
        library = 'seaborn'
        textgen_config=TextGenerationConfig(n=1,temperature=0.2, use_cache =True)
        charts = lida.visualize(summary=summary,goal=goals[i],textgen_config=textgen_config,library=library)
        img_base64_string = charts[0].raster
        img = base64_to_image(img_base64_string)
        st.image(img)

elif menu == "Question based Graph":
    st.subheader("Queury your Data to generate Graph")
    file_uploader = st.file_uploader("Upload your file",type='csv')
    if file_uploader is not None:
        path_to_file="filename1.csv"
        with open(path_to_file,'wb') as f:
            f.write(file_uploader.getvalue())
        text_area = st.text_area("Query your data to generate Graph", height=200)
        if st.button("Generate Graph"):
            if len(text_area) > 0 :
                st.info("Your Query" + text_area)
                lida=Manager(text_gen=llm('google'))
                textgen_config=TextGenerationConfig(n=1,model='gemini-pro',temperature=0.2, use_cache =True)
                summary = lida.summarize('filename1.csv',summary_method='default',  textgen_config = textgen_config)
                user_query = text_area
                charts = lida.visualize(summary=summary, goal=user_query,textgen_config=textgen_config)
                img_base64 = charts[0].raster
                img=base64_to_image(img_base64)
                st.image(img)


