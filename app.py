import streamlit as st 
import base64

st.set_page_config(page_title="Ultimate FPL Analyzer", layout="wide")

#region 1.Background cu Base64 local
def add_local_video_bg(video_file_path):
    try:
        # Citim videoclipul local de pe computerul tău
        with open(video_file_path, "rb") as f:
            video_bytes = f.read()
        # Îl transformăm în cod Base64
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")
    except FileNotFoundError:
        # Mesaj de siguranță în caz că fișierul nu este găsit în folder
        st.warning("Fișierul bg.mp4 nu a fost găsit în folderul proiectului.")
        return

    st.markdown(
        f"""
        <video autoplay loop muted playsinline id="myVideo">
          <!-- Injectăm direct codul video-ului local în browser -->
          <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>

        <div id="video-overlay"></div>

        <style>
        #myVideo {{
          position: fixed;
          right: 0;
          bottom: 0;
          min-width: 100%; 
          min-height: 100%;
          z-index: -2;
          object-fit: cover;
        }}

        #video-overlay {{
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: -1;
          background: rgba(26, 0, 28, 0.65);
        }}

        .stApp, 
        [data-testid="stAppViewContainer"], 
        [data-testid="stMainBlockContainer"],
        .main {{
          background: transparent !important;
        }}
        
        [data-testid="stSidebar"] {{
            background-color: rgba(55, 0, 60, 0.95) !important;
        }}
        
        .stDataFrame {{
            opacity: 0.95;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apelăm funcția indicând numele fișierului tău local (trebuie să fie în același folder cu acest script)
add_local_video_bg("bgg.mp4")

# De aici încolo codul tău rămâne la fel
st.logo('https://b.fssta.com/uploads/application/soccer/competition-logos/EnglishPremierLeague.png', size='large')
page_home = st.Page('_home.py', title='Home page', icon='🏡')
page_analysis = st.Page('_analysis.py', title='Top Picks', icon="🔥")
page_compare = st.Page('_radar.py', title='Radar Comparision', icon="🕸️")
page_builder = st.Page('_builder.py', title='Squad Builder', icon="⚽")
page_tips = st.Page('_tips.py', title='Tips and Tricks', icon="💡")
pg = st.navigation({  
    'Home': [page_home],
    'Analytics': [page_analysis, page_compare],
    'Tools': [page_builder, page_tips]
})
pg.run()
#endregion

#region 2.To do list:

#1.find a way of showing a brief for the selling points of each player✅
#2.add styles to the columns✅
#3.Do sum shit with matplotlib✅//made a chart
#4.make the app look more appropriate add themes on the background or sum❌//made sum complementary colours shit✅
#5.create select boxes for the latter build your team ideea❌ semi done
#6.search theming a little✅
#7.think about a way of comparing players form the table, with pros/cons❌
#8.Make a menu like//think about spotify menu✅
#9 we can make a way better design with the purple and maybe sum animations and shit❌
#endregion

#think about the theme a while
#I am considering to make the theme purple, with a little cyan, and the table to be wistia, but I am considering the black theme with the details beeing glowing purple with the table beeing the green gemini showed me





#✅
#❌

