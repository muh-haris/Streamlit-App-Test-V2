import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000" # our FastAPI server

st.set_page_config(
    page_title = "Student Predictor",
    page_icon = "■",
    layout = "centered"
)

st.title("■ Student Pass / Fail Predictor")
st.markdown("Enter the student's details below to predict their result.")
st.markdown("---")


col1, col2 = st.columns(2)

with col1:
    study_hours = st.slider(
        label = "Study Hours Per Day",
        min_value = 0.0,
        max_value = 10.0,
        value = 4.0,
        step = 0.5,
        help = "How many hours the student studies each day"
)

with col2:
    prev_score = st.slider(
        label = "Previous Exam Score",
        min_value = 0.0,
        max_value = 100.0,
        value = 60.0,
        step = 1.0,
        help = "Score from the most recent exam (out of 100)"
)
    
st.markdown("---")


# prediction button
if st.button("■ Predict Result", use_container_width=True):
    # Call the FastAPI prediction endpoint
    response = requests.post(
        f"{API_URL}/predict",
        json={"study_hours": study_hours, "prev_score": prev_score}
    )
    
    if response.status_code == 200:
        result = response.json()
        
        # Display the result prominently
        if result["prediction"] == 1:
            st.success(f"■ Prediction: **{result['result_label']}**")
        else:
            st.error(f"■ Prediction: **{result['result_label']}**")

        # Show confidence
        st.metric(
            label = "Model Confidence",
            value = f"{result['confidence'] * 100:.1f}%"
        )

        # Show the raw data that was sent
        with st.expander("See what was sent to the API"):
            st.json({
                "study_hours": study_hours,
                "prev_score": prev_score
            })
            st.json(result)
    else:
        st.error("Could not reach the prediction API. Is FastAPI running?")


# live summary
# This updates live as the user moves the sliders — no button click needed
st.markdown("---")
st.subheader("Current Input Summary")

m1, m2 = st.columns(2)
m1.metric("Study Hours", f"{study_hours} hrs/day")
m2.metric("Previous Score", f"{prev_score}/100")


# two separate windows
# Terminal 1 — start FastAPI
# uvicorn main:app --reload
# → Running on http://127.0.0.1:8000
# Terminal 2 — start Streamlit
# streamlit run streamlit_app.py
# → Running on http://localhost:8501
# (browser opens automatically)