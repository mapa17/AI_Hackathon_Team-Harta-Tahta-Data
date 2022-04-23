from enum import Enum
import os
import dataclasses
from typing import List

import numpy as np
import streamlit as st
import streamlit_pydantic as sp

import openai


st.set_page_config(page_title="AI-Hackathon Salzburg", page_icon=":magic_wand:")
st.title("Agriculture Decision Support System - ADSS")
st.markdown(
    """[More info here](https://github.com/mapa17/AI_Hackathon_Team-Harta-Tahta-Data)"""
)
  
class RainOptions(str, Enum):
    little = "little"
    average = "an average"
    alot = "a high"

# Create a list of 3 high-yield crops that I can plant in [Location] with [little/an average/a lot] amount of rain.
@dataclasses.dataclass
class CropSelectionForm:
    location: str = ""
    #rain_amount: RainOptions = dataclasses.field(default_factory=lambda :RainOptions)
    rain_amount: str = "" 

    def get_query(self) -> str :
        return f"Create a list of 3 high-yield crops that I can plant in {self.location} with {self.rain_amount} amount of rain."

# TODO: Add template for best practice prompt
@dataclasses.dataclass
class BestPracticeForm:
    plant_type: str = ""
    location: str = ""
    location_characteristics: str = ""

    def get_query(self) -> str :
        return ""


# Create a thorough income-efficient and sustainable farming plan for a [plant type] plantation in [location] with [location characteristics e.g. weather, climate]
@dataclasses.dataclass
class FarmingPlanForm:
    plant_type: str = ""
    location: str = ""
    location_characteristics: str = ""

    def get_query(self) -> str :
        return f"Create a thorough income-efficient and sustainable farming plan for a {self.plant_type} plantation in {self.location} with {self.location_characteristics}"


# Create a thorough income-efficient and sustainable farming plan for a [plant type] plantation in [location] with [location characteristics e.g. weather, climate]
@dataclasses.dataclass
class GenericQuestionForm:
    question: str = ""
    def get_query(self) -> str :
        return f"{self.question}"



usecases = {
    "Crop Selection": CropSelectionForm,
    "Crop Best Practice": BestPracticeForm,
    "Create Farming Plan": FarmingPlanForm,
    "General Questions": GenericQuestionForm,
}

# NOTE: set the OPEN_API_KEY you get from openai with `export OPEN_API_KEY=XXXXXXXXXXX`
#openai.api_key = os.getenv("OPENAI_API_KEY")
api_key = st.text_input('Insert OpenAI API Key', '')
openai.api_key = api_key

selected_usecase = st.selectbox("Select a problem that you want to solve", options=usecases.keys(), index=0)
selected_form = usecases[selected_usecase]

form_results = sp.pydantic_form(key=f"form_{selected_usecase}", model=selected_form)

if form_results:
    with st.spinner('Asking GPT-3'):
        prompt = form_results.get_query()
        st.write(f"GPT-3 Prompt: {prompt}")

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.8,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        #st.write(f"GPT-3 Response\n{response}")
        text_result = response['choices'][0]["text"]
    st.write(f"GPT-3 Response\n{text_result}")
