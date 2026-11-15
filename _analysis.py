import streamlit as st
import pandas as pd
import numpy as np
from data import load_data
def safe_divided(n,d):
    return n/d if d>0 else 0
data=load_data()
if 'squad' not in st.session_state:
    st.session_state['squad']={
        'GK':'Empty',
        'DEF1':'Empty', 'DEF2':'Empty', 'DEF3':'Empty','DEF4':'Empty','DEF5':'Empty',
        'MID1':'Empty', 'MID2':'Empty','MID3':'Empty',"MID4":'Empty','MID5':'Empty',
        'FWD1':'Empty','FWD2':'Empty','FWD3':'Empty'
    }
def generate_scouting_report(player):
    tips=[]
    if float(player['form'])>=7.0:
        tips.append('🔥 Absolutely on fire right now')
    elif float(player['form'])>=5.0:
        tips.append('Consistent point provider recently')
    if float(player['selected_by_percent'])<=4.0 and float(player['form'])>=4.0:
        tips.append('💎Massive differential,under 5% selection')
    if float(player['now_cost'])/10<=4.0 and float(player['form'])>=4.0 and player['element_type']==1:
        tips.append('💰Good quality/price')
    if player['element_type']==1 and player['saves_per_90']>=2.0:
        tips.append('This goalkeeper has a high tendency to recieve saves bonus points')
    if float(player['now_cost'])/10<=4.5 and float(player['form'])>=4.0 and player['element_type']==2:
        tips.append('💰Good quality/price')
    if player['now_cost']/10<=6.0 and float(player['form'])>=4.0 and player['element_type']==3:
        tips.append('💰Good quality/price')
    if float(player['now_cost'])/10<=7.5 and float(player['form'])>=4.0 and player['element_type']==4:
        tips.append('💰Good quality/price')
    if float(player['goals_conceded_per_90'])<=1.0 and player['element_type']==1:
        tips.append('This has a very high expected clean sheet rate')
    if player['element_type']==2 and player['defensive_contribution_per_90']>=8.0:
        tips.append('This player has an amazing tendecy of getting defcon points')
    if player['yellow_cards']>=7:
        tips.append('This player is a bully(remember, any yellow card means -1 points)')
    if player['red_cards']>=3:
        tips.append('This player is the reincarnation of Andoni Goikoetxea(The Butcher of Bilbao)/whole lotta reds💀')
    if player['element_type']==2 and float(player['expected_assists'])>=2.5:
        tips.append('This defender has a crazy tendency of assisting in games')
    if player['element_type']==2 and float(player['expected_goals'])>=2.5:
        tips.append('This player has a crazy tendency of scoring in games')
    if player['element_type']==3 and player['defensive_contribution_per_90']>=8.0:
        tips.append('Wonderfull defensive midfielder that can make the diference')
    if player['element_type']==3 and float(player['expected_goals'])>=7.0:
        tips.append('This midfielder is expected to score a lot')
    if player['element_type']==3 and float(player['expected_assists'])>=7.0:
        tips.append('This midfielder is expected to assit a lot')
    if player['element_type']==3 and float(player['expected_assists'])>=10.0:
        tips.append('This player is expected to be a midfield maestro')
    if player['element_type']==4 and float(player['expected_goals'])>=9.0:
        tips.append('This player is expected to score a lot the next match')
    if not tips:
        return "Solid player, but he has no selling points"
    return "\n\n ".join(tips)
tab1,tab2,tab3,tab4=st.tabs(["Goalkeepers","Defenders","Midfielders","Forwards"], width="stretch")
with tab1:
    st.header('Top Gk picks for the week')
    keepers=[]
    for p in data['elements']:
        if p['element_type']==1 and p['total_points']!=0 and p['status']=='a':
            form=float(p['form'])
            total_pts = p['total_points']
            price=p['now_cost']/10
            saves_per_90=safe_divided(p['saves'],p['minutes'])*90
            conceded_per_90=safe_divided(p['goals_conceded'],p['minutes'])*90
            clean_sheets=p['clean_sheets']
            expected_points=float(p['ep_next'])
            expected_goals_conc=float(p['expected_goals_conceded_per_90'])
            score=(form*10)+(total_pts*0.5)+(saves_per_90*5)-(conceded_per_90*3)-(price*1.5)+(clean_sheets*3.5)+(expected_points*4)-(expected_goals_conc*4)
            player_dict_1={
                'name':p['web_name'],
                'score':round(score,2),
                'form':form,
                'saves_90':round(saves_per_90,2),
                'selection':p['selected_by_percent'],
                'total_points': p['total_points'],
                'expected_points':p['ep_next'],
                'expected_goals_conc':p['expected_goals_conceded_per_90'],
                'price':f"£{p['now_cost']/10}m"
            }
            player_dict_1['Scout_Verdict']=generate_scouting_report(p)
            keepers.append(player_dict_1)
    keepers.sort(key=lambda x:x['score'],reverse=True)
    df_keepers = pd.DataFrame(keepers[:5])
    df_keepers =df_keepers.drop(columns=['expected_goals_conc'])
    styled_df=df_keepers.style.format(precision=2).background_gradient(subset=df_keepers.columns,cmap="Wistia",gmap=df_keepers['score'])
    event=st.dataframe(styled_df,hide_index=True, use_container_width=True,on_select='rerun',selection_mode='single-row',column_config={'Scout_Verdict':st.column_config.TextColumn(width='medium',help='Hover over to see the full AI report.')})
    if len(event.selection.rows)>0:
        clicked_row_gk_index=event.selection.rows[0]
        selected_gk=df_keepers.iloc[clicked_row_gk_index]['name']
        st.session_state['squad']['GK']=selected_gk
        st.toast(f'Teleported {selected_gk} to your squad')
    st.write('Double click on the Scout_Verdict to see the full verdict')
#endregion
#region 4.Defenders
st.sidebar.write('Drag the slider so you can pick the best player for your budget:')
with tab2:
    st.header("Top Defenders picks for the week")
    level_defender=st.sidebar.slider("Choose a budget for your defenders", min_value=3.7,max_value=15.0,value=5.0,step=0.1,format="%.1f")
    st.write(f'Your budget:£{level_defender}m')
    defenders=[]
    for p in data['elements']:
        if p['element_type']==2 and p['total_points']!=0 and p['minutes']>=90 and p['status']=='a':
            form=float(p['form'])
            total_pts=p['total_points']
            price=p['now_cost']/10
            def_con_per_90=safe_divided(p['defensive_contribution'],p['minutes'])*90
            clean_sheets=p['clean_sheets']
            #goals_conceeded=p['goals_conceded']
            xg=float(p['expected_goals'])
            xa=float(p['expected_assists'])
            xgoalsconc=float(p['expected_goals_conceded'])
            score=(form*8)+(total_pts*1.5)-(price*2)+(def_con_per_90*3)+(clean_sheets*5)-(xgoalsconc*4)+(xg*2.5)+(xa*1.5)
            if p['now_cost']/10 <= level_defender:
                player_dict_2={
                    'name': p['web_name'],
                    'score':round(score,2),
                    'form': p['form'],
                    'defcon': p['defensive_contribution'],
                    'selection': p['selected_by_percent'],
                    'total_points': p['total_points'],
                    'xgoalsconced':p['expected_goals_conceded'],
                    'price':f"£{p['now_cost']/10}m"
                }
                player_dict_2['Scout_Verdict']=generate_scouting_report(p)
                defenders.append(player_dict_2)
    defenders.sort(key=lambda x:x['score'],reverse=True)
    if not defenders:
        st.warning('No defenders found for this budget. Try increasing the budget slider.')
    else:
        df_defenders= pd.DataFrame(defenders[:12])
        styled_df=df_defenders.style.format(precision=2).background_gradient(subset=df_defenders.columns,cmap="Wistia",gmap=df_defenders['score'])
        event1=st.dataframe(styled_df,hide_index=True, use_container_width=True,selection_mode='single-row',on_select='rerun',column_config={'Scout_Verdict':st.column_config.TextColumn(width='medium',help='Hover over to see the full AI report.')})
        if len(event1.selection.rows)>0:
            clicked_row_def_index=event1.selection.rows[0]
            selected_def=df_defenders.iloc[clicked_row_def_index]['name']
            placed=False
            for i in range(1,6):
                slotdf=f'DEF{i}'
                if st.session_state['squad'][slotdf]=='Empty':
                    st.session_state['squad'][slotdf]=selected_def  
                    st.toast(f'{selected_def} added to {slotdf}')
                    placed=True
                    break
            if not placed:
                st.error('Your defense if full!')
    st.write('Double click on the Scout_Verdict to see the full verdict')

#endregion
#region 5.Midfielders:
with tab3:
#midfielders
    st.header("Top Midfilder picks for the week")
    level_midfielders=st.sidebar.slider("Choose a budget for your midfielder",min_value=4.2,max_value=15.0,step =0.1,value = 6.0,format="%.1f")
    st.write(f"Your budget is:£{level_midfielders}m")
    midfielders=[]
    for p in data['elements']:
        if p['element_type']==3 and p['total_points']!=0 and p['minutes']>=100 and float(p['form'])>=1.0 and p['status']=='a':
            form=float(p['form'])
            total_pts=p['total_points']
            price=p['now_cost']/10
            def_con_per_90=safe_divided(p['defensive_contribution'],p['minutes'])*90
            assists=p['assists']
            goals=p['goals_scored']
            xg=float(p['expected_goals'])
            xa=float(p['expected_assists'])
            score=(form*11)-(price*2)+(total_pts*4)+(def_con_per_90*3.5)+(assists*2)+(goals*2.5)+(xg*5)+(xa*3)
            if p['now_cost']/10<=level_midfielders:
                player_dict_3={
                    'name': p['web_name'],
                    'score':round(score,2),
                    'form': p['form'],
                    'defcon': p['defensive_contribution'],
                    'selection': p['selected_by_percent'],
                    'total_points': p['total_points'],
                    'assists': p['assists'],
                    'goals':p['goals_scored'],
                    'price':f"£{p['now_cost']/10}m"
                }               
                player_dict_3['Scout_Verdict']=generate_scouting_report(p)
                midfielders.append(player_dict_3)
    midfielders.sort(key=lambda x:x['score'],reverse=True)
    df_midfielders= pd.DataFrame(midfielders[:12])
    styled_df=df_midfielders.style.format(precision=2).background_gradient(subset=df_midfielders.columns,cmap="Wistia",gmap=df_midfielders['score'])
    event2=st.dataframe(styled_df,hide_index=True, use_container_width=True,selection_mode='single-row',on_select='rerun',column_config={'Scout_Verdict':st.column_config.TextColumn(width='medium',help='Hover over to see the full AI report.')})
    if len(event2.selection.rows)>0:
        clicked_row_def_index=event2.selection.rows[0]
        selected_mid=df_midfielders.iloc[clicked_row_def_index]['name']
        placed=False
        for i in range(1,6):
            slot_mid=f'MID{i}'
            if st.session_state['squad'][slot_mid]=='Empty':
                st.session_state['squad'][slot_mid]=selected_mid  
                st.toast(f'{selected_mid} added to {slot_mid}')
                placed=True
                break
        if not placed:
            st.error('Your attack if full!')
    st.write('Double click on the Scout_Verdict to see the full verdict')
#endregion
#region 6.Forwards
with tab4:
    st.header("Top forwards picks for the week")
    level_forward=st.sidebar.slider("Choose a budget for your forward",min_value=4.1,max_value=16.0,step =0.1,value = 14.5,format="%.1f")
    st.write(f"Your budget is:£{level_forward}m")
    forwards=[]
    for p in data['elements']:
        if p['element_type']==4 and p['total_points']!=0 and p['minutes']>=100 and float(p['form'])>=1.0 and p['status']=='a':
            form=float(p['form'])
            total_pts=p['total_points']
            price=p['now_cost']/10
            assists=p['assists']
            goals=p['goals_scored']
            xg=float(p['expected_goals'])
            xa=float(p['expected_assists'])
            score=(form*11)-(price*3)+(total_pts*4)+(assists*2)+(goals*2.5)+(xg*5)+(xa*3)
            if p['now_cost']/10<=level_forward:
                player_dict_4={
                    'name': p['web_name'],
                    'score':round(score,2),
                    'form': p['form'],
                    'selection': p['selected_by_percent'],
                    'total_points': p['total_points'],
                    'assists': p['assists'],
                    'goals':p['goals_scored'],
                    'price':f"£{p['now_cost']/10}m"
            }
                player_dict_4['Scout_Verdict']=generate_scouting_report(p)
                forwards.append(player_dict_4)
    forwards.sort(key=lambda x:x['score'],reverse=True)
    df_forwards= pd.DataFrame(forwards[:12])
    styled_df=df_forwards.style.format(precision=2).background_gradient(subset=df_forwards.columns,cmap="Wistia",gmap=df_forwards['score'])
    event3=st.dataframe(styled_df,hide_index=True, use_container_width=True,selection_mode='single-row',on_select='rerun',column_config={'Scout_Verdict':st.column_config.TextColumn(width='medium',help='Hover over to see the full AI report.')})
    if len(event3.selection.rows)>0:
        clicked_row_def_index=event3.selection.rows[0]
        selected_fw=df_forwards.iloc[clicked_row_def_index]['name']
        placed=False
        for i in range(1,4):
            slotfw=f'FWD{i}'
            if st.session_state['squad'][slotfw]=='Empty':
                st.session_state['squad'][slotfw]=selected_fw  
                st.toast(f'{selected_fw} added to {slotfw}')
                placed=True
                break
        if not placed:
            st.error('Your attack if full!')
    st.write('Double click on the Scout_Verdict to see the full verdict')
#.Selling points:
#for goalies:
#easy fixtures, high tendency to keep a clean sheet,good form+good schedule
#for defenders:
#tendency to keep a clean sheet, defensive contribution,good form+good schedule
#for midfilders
#high probabilty to score/assist, def cons,good form+good schedule
#for strikers
#high probabilty to score/assist, def cons,good form+good schedule