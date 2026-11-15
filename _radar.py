import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data import load_data
data=load_data()
st.header("Player Comparasion")
st.write("Pick two player to compare their stats and see which one suits you the best")
st.write('You can pick any player from any position as it stands')
all_players_names=sorted([p['web_name'] for p in data['elements']])
#goalkeeper_player_names=sorted([if p['element_type']==1: p['web name'] for p in data['elements']])
col1,col2=st.columns(2)
with col1 :
    player1_name=st.selectbox("Select player 1:",all_players_names,index=all_players_names.index("Salah") if "Salah" in all_players_names else 0)
with col2:
    player2_name=st.selectbox("Select player 1:",all_players_names,index=all_players_names.index("Saka") if "Saka" in all_players_names else 1)
p1_data=next((p for p in data['elements'] if p['web_name']==player1_name),None)
p2_data=next((p for p in data['elements'] if p['web_name']==player2_name),None)
if p1_data and p2_data:
    categories=['Form','Points/Game','xG','xA','DefCons','Threat']
    N=len(categories)
    values_p1=[
        float(p1_data['form']),
        float(p1_data['points_per_game']),
        float(p1_data['expected_goals']),
        float(p1_data['expected_assists']),
        float(p1_data['defensive_contribution_per_90']),
        float(p1_data['threat'])/70
    ]
    values_p2=[
        float(p2_data['form']),
        float(p2_data['points_per_game']),
        float(p2_data['expected_goals']),
        float(p2_data['expected_assists']),
        float(p2_data['defensive_contribution_per_90']),
        float(p2_data['threat'])/70
        ]
    angles=[n/float(N)*2*np.pi for n in range(N)]
    values_p1+=values_p1[:1]
    values_p2+=values_p2[:1]
    angles+=angles[:1]
    fig,ax=plt.subplots(figsize=(6,6),subplot_kw=dict(polar=True),facecolor='#1a001c')
    ax.set_facecolor('#1a001c')
    plt.xticks(angles[:-1],categories,color='white',size=5)
    ax.tick_params(axis='y',colors='gray')
    ax.plot(angles,values_p1,linewidth=2,linestyle='solid',color='#04f5ff',label=player1_name)
    ax.fill(angles,values_p1,'#04f5ff',alpha=0.25)
    ax.plot(angles,values_p2,linewidth=2,linestyle='solid',color='#00ff85',label=player2_name)
    ax.fill(angles,values_p1,'#00ff85',alpha=0.25)    
    plt.legend(loc='upper right',bbox_to_anchor=(1.2,1.1),facecolor='#37003c',edgecolor='white',labelcolor='white',fontsize=8)
spacer1, chart_col, spacer2 = st.columns([1, 2, 1])
with chart_col:
    # Because the original image is 8x8 (High Res), Streamlit will shrink it smoothly!
    st.pyplot(fig, use_container_width=True)
#endregion

#region 1.TO DO LIST
#think about a way of translating the algorithm into a function so you can tell the user to choose between the field players and goalies to compare
#think about the stats so you can compare goalies
