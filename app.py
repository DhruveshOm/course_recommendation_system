# import streamlit as st
# import pickle 
# import pandas as pd
# import requests



# # def fetch_poster(course_id):
# #     requests.get()



# def recommend(course):
#     coursse_index = coursse[coursse['Course'] == course].index[0] # find the index as given by user
#     distance = similarity[coursse_index]   #distance btw courses
#     coursse_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:11] 
    
#     recommended_courses = []
#     for i in coursse_list:
#         course_id = i[0]
#         # fetch poster from api
#         recommended_courses.append(coursse.iloc[i[0]].Course)
#     return recommended_courses

# similarity = pickle.load(open('similarity.pkl','rb'))
# coursse_dict = pickle.load(open('Courses_dict.pkl','rb'))
# coursse = pd.DataFrame(coursse_dict)


# st.title('Course Recommender System')
# Selected_Course_name = st.selectbox(
# 'How would you like to be contacted?',
# (coursse['Course'].values)
# )
# if st.button('Recommend'):
#     recommendations = recommend(Selected_Course_name)
#     for i in recommendations:
#         st.write(i)

import streamlit as st
import pickle
import pandas as pd
import requests

# Unsplash API setup
UNSPLASH_ACCESS_KEY = 'E6QD6R57gQ1CiNndk8MrGuK_48_ftSqXEjs-OnT65Uc'  # Replace with your actual Unsplash Access Key
UNSPLASH_URL = 'https://api.unsplash.com/search/photos'

# Function to fetch poster from Unsplash API
def fetch_poster(course_name):
    """Fetch an image based on the course name."""
    params = {
        'query': course_name,
        'client_id': UNSPLASH_ACCESS_KEY,
        'orientation': 'landscape',
        'per_page': 1
    }

    response = requests.get(UNSPLASH_URL, params=params)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['urls']['regular']
    return "https://via.placeholder.com/400?text=No+Image"

# Function to recommend courses
def recommend(course):
    """Recommend similar courses."""
    course_index = coursse[coursse['Course'] == course].index[0]
    distance = similarity[course_index]
    course_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_courses = []
    recommended_posters = []

    for i in course_list:
        course_name = coursse.iloc[i[0]].Course
        poster_url = fetch_poster(course_name)
        
        recommended_courses.append(course_name)
        recommended_posters.append(poster_url)

    return recommended_courses, recommended_posters

# Load similarity matrix and course data
similarity = pickle.load(open('similarity.pkl', 'rb'))
coursse_dict = pickle.load(open('Courses_dict.pkl', 'rb'))
coursse = pd.DataFrame(coursse_dict)

# Streamlit UI
st.title('🎓 Course Recommender System')

# Course selection dropdown
selected_course_name = st.selectbox(
    '🔍 Select a course to get recommendations:',
    coursse['Course'].values
)

# Show recommendations when button is clicked
if st.button('🚀 Recommend'):
    recommendations, posters = recommend(selected_course_name)

    # Display two courses side by side in each row
    for i in range(0, len(recommendations), 2):
        col1, col2 = st.columns(2)

        # First card
        with col1:
            if i < len(recommendations):
                st.markdown(
                    f"""
                    <div style='border: 2px solid #4CAF50; border-radius: 15px; padding: 15px; text-align: center;'>
                        <h3>{recommendations[i]}</h3>
                        <img src="{posters[i]}" width="300" style='border-radius: 10px;' />
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Second card
        with col2:
            if i + 1 < len(recommendations):
                st.markdown(
                    f"""
                    <div style='border: 2px solid #2196F3; border-radius: 15px; padding: 15px; text-align: center;'>
                        <h3>{recommendations[i+1]}</h3>
                        <img src="{posters[i+1]}" width="300" style='border-radius: 10px;' />
                    </div>
                    """,
                    unsafe_allow_html=True
                )

