import pickle
import streamlit as st
import time

from pathlib import Path
import xgboost as xgb

#st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

footerText = """
<style>
#MainMenu {
visibility:hidden ;
}

footer {
visibility : hidden ;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>

<div class='footer'>
<p> Copyright @ 2023 Center for Digital Health <a href="mailto:iceanon1@khu.ac.kr"> iceanon1@khu.ac.kr </a></p>
</div>
"""

st.markdown(str(footerText), unsafe_allow_html=True)

@st.cache_data
#suicidalthinking_finalized_model_adb predict_suicidalthinking_model
def model_file():
    mfile = str(Path(__file__).parent) + '/suicialthinking_finalized_model.pkl'
    with open(mfile, 'rb') as file:
        model = pickle.load(file)
    return model

# predict_suicidal thinking_model
# suicidalthinking_finalized_model_lgb


def prediction(X_test):
    model = model_file()
    result = model.predict_proba([X_test])

    return result[0][1]


def set_bmi(BMI):
    x = 4
    if   BMI <  18.5           : x = 1
    elif BMI >= 18.5 and BMI < 23: x = 2
    elif BMI >= 23   and BMI < 25: x = 3
    elif BMI >= 25             : x = 4
    else : x = 0

    return x


def input_values():
    region  = st.radio('Region of regidence', ('Urban','Rural'), horizontal=True)
    regionDict = {'Urban':1,'Rural':2}
    region  = regionDict[region]

    Age   = st.radio('Age(year)',(13,14,15,16,17,18), horizontal=True)

    SEX     = st.radio('Sex',('Male','Female'), horizontal=True)
    SEXDict = {'Male':1,'Female':2}
    SEX = SEXDict[SEX]

    height  = st.number_input('Height (cm)', min_value=80, max_value=190, value=130)
    weight  = st.number_input('Weight (kg)', min_value=30, max_value=100, value=50)
    bmiv = weight/((height/100)**2)
    bmi_2 = set_bmi(bmiv)
    bmiDict = {1:'Underweight',2:'Normal',3:'Overweight',4:'Obese'}
    st.write('BMI: ', bmiDict[bmi_2], round(bmiv,2))
    
    study    = st.radio('Academic achievement', ('Low','Low-middle','Middle','Upper-middle','Upper'), horizontal=True)
    studyDict = {'Low':1, 'Low-middle':2,'Middle':3,'Upper-middle':4,'Upper':5}
    study = studyDict[study]

    household_income  = st.radio('Household income', ('Low','Low-middle','Middle','Upper-middle','Upper'), horizontal=True)
    household_incomeDict = {'Low':1, 'Low-middle':2,'Middle':3,'Upper-middle':4,'Upper':5}
    household_income  = household_incomeDict[household_income]

    smoking   = st.radio('Smoking status', ('No','Yes'), horizontal=True)
    smokingDict = {'No':0,'Yes':1}
    smoking   = smokingDict[smoking]
    
    alcoholic_consumption = st.radio('Acohol consumption Status', ('No','Yes'), horizontal=True)
    alcoholic_consumptionDict = {'No':0,'Yes':1}
    alcoholic_consumption = alcoholic_consumptionDict[alcoholic_consumption]
    
    stress  = st.radio('Stress status', ('Low to moderate','High to severe'), horizontal=True)
    stressDict = {'Low to moderate':1,'High to severe':2}
    stress = stressDict[stress]

    depression = st.radio('Depression', ('Low to moderate','High to severe'), horizontal=True)
    depressionDict = {'Low to moderate':0,'High to severe':1}
    depression = depressionDict[depression]

    exercise = st.radio('Exercise status', ('Not enough','Enough'), horizontal=True)
    exerciseDict = {'Not enough':0,'Enough':1}
    exercise = exerciseDict[exercise]

    suicidalthinking = st.radio('Suicidal thinking', ('No','Yes'), horizontal=True)
    suicidalthinkingDict = {'No':0,'Yes':1}
    suicidalthinking = suicidalthinkingDict[suicidalthinking]

    screentime = st.radio('Screentime status', ('Low to moderate','High to severe'), horizontal=True)
    screentimeDict = {'Low to moderate':0,'High to severe':1}
    screentime = screentimeDict[screentime]
    
    X_test = [region, Age, SEX, bmi_2, study, household_income, smoking, alcoholic_consumption, stress, depression, exercise, suicidalthinking, screentime]

    result = prediction(X_test)

    return result


def main():
    result = input_values()    
    
    with st.sidebar:
        st.markdown(f'# Probability for suicidal thinking')
        
        if result*100 < 50:
            danger_level = 'Barely'
        elif result*100 < 75:  # 50% 이상 75% 미만
            danger_level = 'Moderately'
            st.markdown(f'# {result*100:.2f} %')
        elif result*100 < 90:  # 75% 이상 90% 미만
            danger_level = 'Considerably'
            st.markdown(f'# {result*100:.2f} %')
        elif result*100 <= 100 :  # 90% 이상
            danger_level = 'Extremely'
            print(result*100, )
            st.markdown(f'# {result*100:.2f} %')
        
        st.markdown(f'## {danger_level}')

    now = time.localtime()
    print(time.strftime('%Y-%m-%d %H:%M:%S', now))


        

if __name__ == '__main__':
    main()
