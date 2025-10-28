#type:ignore

import streamlit as st
import pickle as pickle
import google.generativeai as genai
import json as js
import re
import pandas as pd
import ast
import os
from huggingface_hub import InferenceClient

genai.configure(api_key=st.secrets["gemini_api"])



client = InferenceClient(
    provider="nebius",
    api_key=st.secrets["hugging_face_api"],
)



prompt_model = genai.GenerativeModel("gemini-2.0-flash")


model = pickle.load(open("Models/Nutrition_model_Random_forest.pkl","rb"))

recipe_url = 'https://drive.google.com/file/d/18xaw_nR3q8BPlD4M96_1YVUIJhzMe7ox/view?usp=sharing'
recipe_file_id = recipe_url.split('/d/')[1].split('/')[0]
recipe_download_url = f'https://drive.google.com/uc?id={recipe_file_id}'


food_url = 'https://drive.google.com/file/d/1ovt05RW5CxBcl_YXQWeMVkdKqct2nqvq/view?usp=sharing'
food_file_id = food_url.split('/d/')[1].split('/')[0]
food_download_url = f'https://drive.google.com/uc?id={food_file_id}'



def gemini_model(meals):
    response = prompt_model.generate_content("give me the total sum of avg_calories', 'protein_g', 'carbs_g', 'fat_g', 'fiber_g', 'sugar_g', 'calcium_mg', 'iron_mg', 'vitamin_c_mg','vitamin_d_IU', 'vitamin_b12_mcg' " + meals + ".i want the output in a single structure with each nutrient havng the combined nutrients amount in all meals. strictly return only valid json and no explanation or text other than json ")
    raw = response.text.strip()
    match = re.search(r"\{.*\}",raw,re.DOTALL)
    if match:
        clean_response = match.group(0)
        nutrients = js.loads(clean_response)
    return nutrients



def grocery_selection(food_df, l):
    shuffled_df = food_df.sample(frac=1).reset_index(drop=True)
    for _, row in shuffled_df.iterrows():
        try:
            nutrients = ast.literal_eval(row['nutrient_name'])
        except:
            nutrients = []
        if any(l.lower() in n.lower() for n in nutrients):
            return row['food_name']
        
def recipe_selection(grocery):
    completion = client.chat.completions.create(
    model="google/gemma-2-2b-it",
    messages=[
        {
            "role": "user",
            "content": f"""
You are a professional Indian chef and recipe generator.

Task:
Given a list of grocery ingredients, create an authentic Indian recipe using them. 
Always focus on Indian flavors, spices, and cooking methods.

Input Ingredients: {grocery}

**Ingredient Understanding Rules:**
- If you find text that looks like a **batch code**, **barcode**, **product ID**, or **serial number** (e.g., "NFY120DHB", "CO,CT", "ABC-1234"), **ignore or replace** it.
- If the line includes a **brand or packaged food name** (e.g., "SARGENTO", "Kraft", "Heinz", "Trader Joe’s"), 
  identify what the actual **food ingredient** is (e.g., SARGENTO → cheese, Heinz → tomato ketchup).
- Assume these brands are from the US or other countries, and replace them with the most **common equivalent ingredient** if available in indian cusine.
  For example:
  - “SARGENTO” → “Cheddar cheese”
  - “Heinz ketchup” → “Tomato sauce”
  - “Trader Joe’s Almond Butter” → “Almond butter”

**Example Input:**
SARGENTO (CO,CT) - NFY120DHB

**Example Replacement:**
Cheddar cheese

---
IMPORTANT:
- Do NOT include any introduction or commentary.
- Respond ONLY in the following exact format.
- Do NOT add extra text before or after.
- if any unrelated data such as brand names, batch codes, product IDs, serial numbers, or packaging info (e.g., "SARGENTO (CO,CT) - NFY120DHB") is found, search for these .
- Focus only on meaningful ingredients and Indian food items.
- IF no usable ingredients is found politely say "Please Try again with another food! Confusion with some ingredients!"

Strict Output Format (use this exact structure every time):

**Dish Name: <name of the Indian dish>**

**Cuisine: Indian**

**Regional Style:** <North Indian / South Indian / Bengali / etc.>

**Ingredients:**
- <ingredient 1>
- <ingredient 2>
- <ingredient 3>

**Cooking Instructions:**
1. <step 1>
2. <step 2>
3. <step 3>

Preparation Time: <in minutes>
Cooking Time: <in minutes>
Servings: <number>

**Nutritional Info (approximate):**
- Calories: <value>
- Protein: <value>
- Fat: <value>
- Carbohydrates: <value>

**Serving Suggestion:**
<Describe how to serve the dish (e.g., with rice, roti, chutney)>
"""
            }
        ],
    )

    return completion.choices[0].message



st.title("Smart Grocery and Recipe Recommendation ")

st.write("Enter the details below")

age = st.number_input("Age",18,80)
height = st.number_input("Height in cm",100)
weight = st.number_input("Weight in Kg",25)
sleep_hours = st.number_input("Average Sleep Hour per day",0,10,6)
activity_level_inp = st.selectbox("Activity Level",['Sedentary', 'Moderate', 'Active'])
water_level = st.number_input("Water Intake per day in Litre")
diet_inp = st.selectbox("Diet Type",['Vegetarian','Non-Vegetarian','Vegan'])
gender_inp = st.selectbox("Gender",['Male','Female'])
sun_exp = st.number_input("Sun Exposure per day in hours")*60




bmi = weight/((height/100)**2)

meals = st.text_input("Mention some meals/drinks you have regularly  "," (eg: Rice,Orange smoothie, Dosa Sambar )")


if 'deficit' not in st.session_state:
    st.session_state.deficit = None

if 'food' not in st.session_state:
    try:
        st.session_state.food = pd.read_csv(food_download_url)
    except Exception as e:
        st.error(f"Failed to load food data: {e}")
        st.stop()

if "rec_food" not in st.session_state:
    st.session_state.rec_food = None



if st.button("Find Deficit"):
    nutrients = gemini_model(meals)

    for key, value in nutrients.items():
        globals()[key] = value


    gender = 1 if gender_inp =='Male' else 0
    activity_moderate = 1 if activity_level_inp == 'Moderate' else 0
    activity_sedentary = 1 if activity_level_inp == 'Sedentary' else 0
    diet_veg = 1 if diet_inp == 'Vegetarian' else 0
    diet_vegan = 1 if diet_inp == 'Vegan' else 0

    vitamin_d_IU = sun_exp * 66.7

    df = pd.DataFrame([[
        age, bmi, sleep_hours, avg_calories, protein_g, carbs_g, fat_g, fiber_g,
        sugar_g, calcium_mg, iron_mg, vitamin_c_mg, vitamin_d_IU, vitamin_b12_mcg,
        water_level, sun_exp, gender, activity_moderate, activity_sedentary, diet_veg, diet_vegan
    ]], columns=[
        "age","bmi","avg_sleep_hours","avg_calories","protein_g","carbs_g","fat_g",
        "fiber_g","sugar_g","calcium_mg","iron_mg","vitamin_c_mg","vitamin_d_IU",
        "vitamin_b12_mcg","avg_water_intake_l","sun_exposure_min","gender_Male",
        "activity_level_Moderate","activity_level_Sedentary","diet_type_Veg","diet_type_Vegan"
    ])
    pred_enc = model.predict(df)
    st.session_state.deficit = pred_enc[0].split("_")[0]
    if st.session_state.deficit == 'Balanced':
        st.write("You have a balanced diet. No deficiencies !!")
    else:
        st.write(f"You are deficit in {st.session_state.deficit} !!")
    


    st.write("Recommended food ")
    st.session_state.rec_food = grocery_selection(st.session_state.food,st.session_state.deficit)
    st.write(st.session_state.rec_food)


if st.session_state.deficit and st.session_state.rec_food:
    if st.button("Recommend another"):
        st.session_state.rec_food  = grocery_selection(st.session_state.food, st.session_state.deficit)
        if st.session_state.rec_food:
            st.write(f"Recommended food: **{st.session_state.rec_food }**")
        else:
            st.warning("No food found for this deficiency.")
if st.session_state.rec_food:
    if st.button("Proceed with the recommended food?"):
        st.session_state.recipe = recipe_selection(st.session_state.rec_food)
        st.markdown(st.session_state.recipe['content'])