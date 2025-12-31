import streamlit as st
import pandas as pd
import plotly.express as px



st.set_page_config(page_title='US Oopulation',page_icon='🏂',layout='wide')


def num_format(num):
    if num>1000000:
        return f"{round(num/1000000)} M"
    return f"{round(num/1000)} K"



st.title('US Population',text_alignment='center')

df=pd.read_csv('../usa population_streamlit/us-population-2010-2019.csv',index_col=0)


col1,col2,col3=st.columns([0.25,0.5,0.25])


#=====================

with st.sidebar:
    st.title('🏂 US Population Dashboard')

    list_year=df['year'].unique()[::-1]
    year_selected=st.selectbox('select a year',options=list_year)

#===================

current_pop=df[df['year']==year_selected].reset_index()

previous_pop=df[df['year']==year_selected-1].reset_index()

current_pop['diff_pop']=current_pop['population'].sub(previous_pop['population'],fill_value=0)

current_pop.sort_values(by='diff_pop',axis=0,ascending=False,inplace=True)

#=============================

with col1:
    st.write('### Gains/Losses')


    if year_selected != 2010 :

        # first card/positive
        state_name=current_pop.states.iloc[0]

        population=num_format(current_pop['population'].iloc[0])

        diff=num_format(current_pop['diff_pop'].iloc[0])

        st.metric(label=state_name,value=population,delta=diff,border=True,width='content')

    else :

        st.metric(label='',value=None,delta=None,border=True,width='content')

    
    if year_selected != 2010 :

        # second card/negative
        state_name_=current_pop.states.iloc[-1]

        population_=num_format(current_pop['population'].iloc[-1])

        diff_=num_format(current_pop['diff_pop'].iloc[-1])

        st.metric(label=state_name_,value=population_,delta=diff_,border=True,width='content')
        
    else :

        st.metric(label='',value=None,delta=None,border=True,width='content')



with col2:
    st.write('### Total Population')

    # first graph
    fig=px.choropleth(current_pop,locations='states_code',color='population',locationmode='USA-states',scope='usa',color_continuous_scale='viridis',labels={"population":"population"})
    fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    # second graph
    pivot_tab=df.pivot(index='year',columns='states',values='population')
    heatmap=px.imshow(pivot_tab,labels=dict(x='states',y='year',color='Max of population'))
    st.plotly_chart(heatmap)



with col3:
    st.write('### Top States')

    st.dataframe(current_pop.iloc[:10,:].sort_values(by='population',ascending=False),column_order=['states','population'],hide_index=True)

