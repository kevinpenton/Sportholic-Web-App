import numpy as np
import pandas as pd
import streamlit as st
import requests

# Remember to use "streamlit run main.py" (without the "") to start running streamlit

# getting url, accessing the data, and getting the specific list in the dictionary for performers
performers_url = "https://api.seatgeek.com/2/performers?client_id=MjYzMjg5MDB8MTY0ODU5MDg1My41NTk3NDM0"
performers_dict = requests.get(performers_url).json()
performers_list = performers_dict["performers"]

# assigning the indexes with the performer
eaglesBaseball = performers_list[0]
superBowl = performers_list[1]
wildcatsBaseball = performers_list[2]
playoffMLB = performers_list[3]
uniNotreDameFB = performers_list[4]
collegeFootballPlayoff = performers_list[5]
panthersBaseball = performers_list[6]
texasBowl = performers_list[8]
matteoTennis = performers_list[9]

baseball = [eaglesBaseball, wildcatsBaseball, playoffMLB, panthersBaseball]
football = [superBowl, uniNotreDameFB, collegeFootballPlayoff, texasBowl]
tennis = [matteoTennis]

sports_events = [baseball, football, tennis]

# title and subheader
st.title("*Sportholic*")
st.subheader("Your trusty search engine for the lovers of sports events")

name = st.text_input("What's your name?")
if name:
   st.write("Welcome, ", name)

   sports = ["Baseball", "Football", "Tennis"]

   # variables for event names
   baseball_events = [eaglesBaseball["name"], wildcatsBaseball["name"],
                      playoffMLB["name"], panthersBaseball["name"]]
   football_events = [superBowl["name"], uniNotreDameFB["name"],
                      collegeFootballPlayoff["name"], texasBowl["name"]]
   tennis_events = [matteoTennis["name"]]


   # method for map, takes in number to replace index and displays map
   def map(event):
       latitude = event["location"]["lat"]
       longitude = event["location"]["lon"]

       df = pd.DataFrame(
           np.random.randn(1, 1) / [50, 50] + [latitude, longitude], columns=['lat', 'lon']
       )
       st.map(df)


   # function to display info about each event
   def event_information(search):
       # interactive table to see all events
       all_available = st.checkbox('See all options available')
       if all_available:
           all_events = pd.DataFrame(
               {
                   "Baseball": [baseball_events[0], baseball_events[1], baseball_events[2], baseball_events[3]],
                   "Football": [football_events[0], football_events[1], football_events[2], football_events[3]],
                   "Tennis": [tennis_events[0], "", "", ""]
               }
           )
           st.dataframe(all_events)

       if search == "Baseball":
           st.info('Selected: Baseball')
           events = baseball_events
           info = baseball
       elif search == "Football":
           st.info('Selected: Football')
           events = football_events
           info = football
       elif search == "Tennis":
           st.info('Selected: Tennis')
           events = tennis_events
           info = tennis

       choices = st.multiselect('Choose performers you want to view', events)

       if choices:
           for i in choices:
               st.write(i, ":")

               for j in info:
                   if j["name"] == i and j["has_upcoming_events"]:
                       if j["location"]:
                           if st.button('View Location'):
                               location = map(j)
                       else:
                           st.error("Location unavailable.")

                       num_of_events = j["num_upcoming_events"]
                       st.success("This performer has upcoming events")

                       tickets = st.radio(
                           "Would you like to view tickets for upcoming events? ",
                           ('Yes', 'No'))

                       if tickets == 'Yes':
                           st.info('Click link to view tickets')
                           st.write(j["url"])

                   elif j["name"] == i and not j["has_upcoming_events"]:
                       st.error("Sorry, there are no upcoming events for this performer.")


   # selectbox with 3 choices of sports to filter by
   search_options = st.selectbox("Search by sport ", (sports))
   # calling to event info function
   event_information(search_options)

   see_popularity = st.checkbox('See what sports are popular right now')
   if see_popularity:

       baseball_count = 0
       football_count = 0
       tennis_count = 0

       for i in sports_events:
           for j in i:
               if j["type"] == "mlb" or "ncaa_baseball" or "baseball":
                   baseball_count += 1
                   continue
               if j["type"] == "football" or "ncaa_football":
                   football_count += 1
                   continue
               if j["type"] == "tennis":
                   tennis_count += 1
                   continue

       chartType = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart"])

       if (chartType == "Bar Chart"):
           popularity_chart = pd.DataFrame([baseball_count, football_count, tennis_count], sports, columns=[
               "Number of Events"])
           st.bar_chart(data=popularity_chart, width=350, height=0, use_container_width=False)

       if (chartType == "Line Chart"):
           popularity_chart = pd.DataFrame([baseball_count, football_count, tennis_count], sports,
                                           columns=["Number of Events"])
           st.line_chart(data=popularity_chart, width=350, height=0, use_container_width=False)

