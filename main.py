import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


filepath = 'C:/Users/Rakesh Sharma/Downloads/California_Fire_Incidents.csv'
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def dataFormation(data_frame):
    data = data_frame
    a = data.dtypes
    boolian_column = [column for column in data if a[column] == bool]
    numberOfRows = len(data.index)
    for i in boolian_column:
        trueVale = len(data[data[i] == True])
        if trueVale / numberOfRows < 0.1:
            data.drop(i, axis='columns', inplace=True)
    column_to_drop = ["Status","StructuresEvacuated", "SearchKeywords"]
    data.drop(column_to_drop, axis='columns', inplace=True)
    data.fillna(0, inplace=True)
    data['AcresBurned'] = data['AcresBurned'].astype('int64')
    data['AirTankers'] = data['AirTankers'].astype('int64')
    data['CrewsInvolved'] = data['CrewsInvolved'].astype('int64')
    data['Dozers'] = data['Dozers'].astype('int64')
    data['Engines'] = data['Engines'].astype('int64')
    data['Fatalities'] = data['Fatalities'].astype('int64')
    data['Injuries'] = data['Injuries'].astype('int64')
    data['Helicopters'] = data['Helicopters'].astype('int64')
    data['PersonnelInvolved'] = data['PersonnelInvolved'].astype('int64')
    data['StructuresDamaged'] = data['StructuresDamaged'].astype('int64')
    data['StructuresDestroyed'] = data['StructuresDestroyed'].astype('int64')
    data['StructuresThreatened'] = data['StructuresThreatened'].astype('int64')
    return data

def dateTimeCorrection(data_frame):
    data_frame['Started'] = pd.to_datetime(data_frame['Started'])
    data_frame['Updated'] = pd.to_datetime(data_frame['Updated'])
    data_frame['Extinguished'] = pd.to_datetime(data_frame['Extinguished'])

    data_frame['YearStarted'] = data_frame['Started'].dt.year
    data_frame['MonthStarted'] = data_frame['Started'].dt.strftime('%B')
    data_frame = data_frame[data_frame.YearStarted != 1969]
    return data_frame

data = pd.read_csv(filepath)

newData = dataFormation(data)
newData = dateTimeCorrection(newData)

year = ("2013","2014","2015","2016","2017","2018","2019")
county = ('Tuolumne','Los Angeles','Riverside','Placer','Ventura','Fresno',
 'Siskiyou','Humboldt','Tehama','Shasta','San Diego','Kern','Sonoma',
 'Contra Costa','Butte','Tulare','Santa Barbara','Mariposa','Monterey',
 'El Dorado','San Bernardino','Plumas','Modoc','San Luis Obispo','Madera',
 'Inyo' 'Napa','San Benito', 'San Joaquin', 'Lake', 'Alameda', 'Glenn', 'Yolo' ,
 'Sacramento','Stanislaus' ,'Solano', 'Merced', 'Mendocino', 'Lassen', 'Amador',
 'Yuba','Nevada','Santa Clara','Calaveras','San Mateo','Orange','Colusa',
 'Trinity','Del Norte','Mono','Alpine','Sutter','Kings','Sierra',
 'Santa Cruz', 'Marin', 'Mexico', 'State of Oregon', 'State of Nevada')

def numberOfFirePerYear(st,  county1="Los", df=[]):
    col1, col2 = st.columns(2)
    # checkList = True
    with col1:
        countyList = st.selectbox("County", county1, key="1")
    with col2:
        checkList= st.radio("Select Graph Type", ['Bar', "Pie"], key="2")
    with col1:
        level = df['YearStarted'].unique()
        size = df[['YearStarted']].value_counts().sort_index()
        fig, ax = plt.subplots()
        bar_graph = ax.bar(level, size)
        ax.set(xlabel="Year", ylabel='Number of Fire Incidents',
               title='Frequency of Fire Incidents per Year Between 2013-2019', ylim=(0, max(size) + 5))
        ax.bar_label(bar_graph, fmt='{:,.0f}')
        st.pyplot(fig)

    if checkList == 'Bar':
        with col2:
            # fig, ax = newData[['YearStarted']][newData['Counties']==countyList].value_counts().sort_index().plot(kind='bar', figsize=(12,7))
            size = df[['YearStarted']][df['Counties']==countyList].value_counts().sort_index()
            a = df[['YearStarted']][df['Counties']==countyList]
            a.reset_index(inplace=True)
            level = a['YearStarted'].unique()
            fig, ax = plt.subplots()
            bar_graph = ax.bar(level, size)
            title = "Frequency of Fire Incidents per Year Between 2013-2019 "+countyList
            ax.set(xlabel="Year", ylabel='Number of Fire Incidents',
                   title=title, ylim=(0, max(size) + 5))
            ax.bar_label(bar_graph, fmt='{:,.0f}')
            st.pyplot(fig)
    elif checkList == 'Pie':
        with col2:
            a = df[['YearStarted']][df['Counties'] == countyList]
            a.reset_index(inplace=True)
            labels = a['YearStarted'].unique()

            size = df['YearStarted'][df['Counties']==countyList].value_counts()
            fig, ax = plt.subplots()
            ax.pie(size,  labels=labels, autopct='%1.1f%%')
            title = "Frequency of Fire Incidents per Year Between 2013-2019 " + countyList
            ax.set(title=title)
            st.pyplot(fig)
    st.write("As from year wise analysis we got that **_Year 2017_** is very violent year and the fire"
             " is increasing year by year")

def areaDamaged(st, df=[], county2=[]):
    col1, col2 = st.columns(2)
    # checkList = True
    with col1:
        countyList1 = st.selectbox("County", county2, key="3")
    with col2:
        yearArray1 = st.slider('Select a range of Years',2013, 2019, (2013, 2019),1, key="4")
    with col1:
        level = df['YearStarted'][(df['YearStarted']>=yearArray1[0]) & (df['YearStarted']<=yearArray1[1])]
        size = df[['AcresBurned']][(df['YearStarted']>=yearArray1[0]) & (df['YearStarted']<=yearArray1[1])]

        fig, ax = plt.subplots()
        scattered_graph = ax.scatter(size, level, alpha=1, s=5)
        ax.set(xlabel="Area Damaged in Acres", ylabel='Years',
               title='Forest Area damaged in 2013-2019')
        st.pyplot(fig)
    with col2:
        level = df['YearStarted'][df['Counties']==countyList1][
            (df['YearStarted'] >= yearArray1[0]) & (df['YearStarted'] <= yearArray1[1])]
        size = df['AcresBurned'][df['Counties']==countyList1][
            (df['YearStarted'] >= yearArray1[0]) & (df['YearStarted'] <= yearArray1[1])]
        title = "Forest Area damaged in "+str(yearArray1[0])+" - " + str(yearArray1[1])+ " of " + countyList1
        fig, ax = plt.subplots()
        scattered_graph = ax.scatter(size, level, alpha=1, s=5)
        ax.set(xlabel="Area Damaged in Acres", ylabel='Years',
               title=title)
        st.pyplot(fig)

def firePerCountyPerMonth(st, df=[], county=[], year = []):
    col1, col2 = st.columns(2)
    col21, col22 = col2.columns(2)
    # checkList = True
    with col1:
        countyList = st.selectbox("County", county, key="5")
    with col21:
        checkList = st.radio("Select Graph Type", ['Bar', "Pie"], key="6")
    with col22:
        yearList = st.selectbox("Year", year, key="7")
    with col1:
        print(yearList, "col1", type(yearList))
        size = data['MonthStarted'][data['YearStarted']==int(yearList)].value_counts()
        level = data['MonthStarted'][data['YearStarted']==int(yearList)].sort_index().unique()
        fig, ax = plt.subplots()
        bar_graph = ax.bar(level, size)
        title = "Frequency of Fire Incidents per Months for "+yearList
        ax.set(xlabel="Months", ylabel='Number of Fire Incidents',
               title=title)
        plt.xticks(rotation=90, fontsize=11)
        ax.bar_label(bar_graph, fmt='{:,.0f}')
        st.pyplot(fig)
    if checkList == 'Bar':
        with col2:
            size = data['MonthStarted'][data['YearStarted']==int(yearList)][data['Counties']==countyList].value_counts()
            level = data['MonthStarted'][data['YearStarted']==int(yearList)][data['Counties']==countyList].unique()
            fig, ax = plt.subplots()
            bar_graph = ax.bar(level, size)
            title = "Frequency of Fire Incidents per Months for " + str(yearList)+" of "+countyList
            ax.set(xlabel="Months", ylabel='Number of Fire Incidents',
                   title=title)
            plt.xticks(rotation=90, fontsize=11)
            ax.bar_label(bar_graph, fmt='{:,.0f}')
            st.pyplot(fig)
    elif checkList == 'Pie':
        with col2:
            labels = newData['MonthStarted'][newData['YearStarted'] == int(yearList)][newData['Counties'] == countyList].unique()

            size = newData[['MonthStarted']][newData['YearStarted'] == int(yearList)][
                newData['Counties'] == countyList].value_counts()
            fig, ax = plt.subplots()
            ax.pie(size, labels=labels, autopct='%1.1f%%')

            title = "Frequency of Fire Incidents per Year Between 2013-2019 " + countyList
            ax.set(title=title)
            st.pyplot(fig)

def topCounty(st, df, year=[]):
    col1, col2 = st.columns(2)
    with col1:
        yearList = st.selectbox("Year", year, key="8")

    a = newData[['YearStarted', "Counties", 'AcresBurned']][newData['YearStarted'] == int(yearList)].groupby(
        ['YearStarted', "Counties"]).sum().sort_values('AcresBurned', ascending=False).head(10)
    a.reset_index(inplace=True)
    level = a["Counties"]
    size = a['AcresBurned']
    with col1:
        fig, ax = plt.subplots()
        bar_graph = ax.bar(level, size)
        title = "Top 10 County where fire occurs in  " + yearList
        ax.set(xlabel="County Name", ylabel='Acres Burn',
               title=title)
        plt.xticks(rotation=90, fontsize=11)
        ax.bar_label(bar_graph, fmt='{:,.0f}')
        st.pyplot(fig)
    with col2:
        st.title("")
        st.title("")
        fig, ax = plt.subplots()
        ax.pie(size, labels=level, autopct='%1.1f%%')
        title = "Top 10 County where fire occurs in " + yearList
        ax.set(title=title)
        st.pyplot(fig)

def numberOfFatalities(st, df =[]):
    col1, col2 = st.columns(2)
    with col1:
        a = newData[['Fatalities', 'YearStarted']].groupby('YearStarted').sum().sort_values('Fatalities',                                                                                        ascending=False)
        a.reset_index(inplace=True)
        level = a['YearStarted']
        size = a['Fatalities']
        fig, ax = plt.subplots()
        ax.bar(level, size)
        plt.xlabel('Year of Fire Incident')
        plt.ylabel('Number of Fatalities')
        plt.title('Number of Fatalities Each Year Between 2013-2019')
        st.pyplot(fig)
    with col2:
        level = newData['Fatalities']
        size = newData['AcresBurned']

        fig, ax = plt.subplots()
        scattered_graph = ax.scatter(size, level, alpha=1, s=5)
        ax.set(xlabel="Area Damaged in Acres", ylabel='Number of Fatalities',
               title='Number of Fatalities by Acres burned')
        st.pyplot(fig)
st.title ("California Wildfires 2013 - 2019")
st.write("With climate change, California's fire season has become a hot topic. "
         "What does a changing climate with periods of drought look like concerning the size, frequency, and deadliness of fires throughout the state?")
st.write("")
st.write("I'm using a dataset with California wildfire incidents from 2013 through 2019, from data that was originally scraped from the CalFire website.")
st.write("First off, which particular years and months tend to have the most wildfires? Do they continuously increase over time through the year, or each succeeding year? which county have suffered every year? Do the wildfire continuosly increaded or decresed? Which month is more dangerous? ")
st.write("With adverse impact of Global warming and climate change I hypothesized that:")
st.markdown("    -    The number of fire per year would increased")
st.markdown("    -    The most fire happened in summers")
st.markdown("    -    The number of acres burned increases with each year")
st.subheader("Analysis of wildfire in every County Between 2013 - 2019")
numberOfFirePerYear(st, county1=county, df = newData)
st.subheader("Wildlife Area Damaged between 2013 - 2019")
areaDamaged(st, df=newData, county2=county)
st.subheader("Analysis of wildfire in every county and every month")
firePerCountyPerMonth(st, df=newData, county=county, year=year)
st.markdown("_What does this tell us?_")
st.write("As suspected, the amount of fires per year increased overall between 2014 and 2017. "
         "2018 and 2019 however, have a drop in the number of fires, though each year still has more incidents than years previous to 2017.")
st.write("As to my hypothesis, the most fires occur during the month of July, with the biggest jump between May and June with the ramp up in warmer temperatures")
st.write("Why is this? Due to ongoing drought, what were traditionally thought of as the biggest fire months "
         "(September, October), are now being pushed earlier in the calendar. "
         "Fire season appears to stretch over 7 months, where those months have around 50 or more fire incidents per month.")

st.write("While the occurrence of mega-fires remains low compared to the number of fires that occur each year, "
         "there is the sign of a trend where larger fires appear more frequently as time passes.")
st.write("Does it follow that the more frequent the fires in a year the higher the fatalities and damage?")
st.write("I suspect that the number of fatalities and amount of damage corresponds with the number of fires and the number of acres burned each year.")
st.markdown("    -    The number of fires and acres burned goes up, so do fatalities and damage.")
st.subheader("Top county of every year")
topCounty(st, df=newData, year=year)
st.subheader("Fatalities during 2013 - 2019 wildfire")
numberOfFatalities(st, df=newData)
st.write("While 2017 was the year with the most fires, it did not have the most fatalities - "
         "the highest number of deaths occured in 2018, which is due to the Camp Fire which destroyed the town of Paradise very quickly.")
st.write("Overall fatality numbers are low for most years thankfully, but the years with the highest incidence of fires (2017-2019) do have the largest number of deaths.")
st.write("There is a disconnect between number of fatalities and acres burned, "
         "which can be seen in the above graph. "
         "So the hypothesis that deaths correspond with larger fires is not necessarily true.")

st.write("The counties with the highest frequency of fires do not have the most acres burned!")
st.markdown("Colusa county has the most acres burned of all California counties. "
            "It is a mostly rural county with grasslands and wooded area on the western side.")
st.markdown("Alameda, which had a high frequency of fires, has a low number of acres burned, which most likely reflects its urban/suburban dominated environment.")
st.subheader("Conclusion")
st.write("While there are a couple of suprises with the data, overall the results support my hypothesis that fires are generally")
st.markdown("   -   Becoming more frequent")
st.markdown("   -   Burning more acreage")
st.markdown("   -   Causing more death and destruction with each passing year")
st.write("With the continued rise in average temperature, higher prevalence of drought, "
         "and the continued development of land for housing along previously wild areas, "
         "fires will most likely continue to get larger, more frequent, "
         "and continue to cause large amounts of property damage and loss of life within the state.")
st.subheader("What can we do about this?")
st.write("Our changing climate and drought conditions are issues on a scale that will take a large amount of cooperation, "
         "and to some extent there's no way to reverse some of those changes.What we can do is prepare on a local level, "
         "and think about planning for the future of the state.")
st.markdown("   -   Avoid building housing near wild, undeveloped areas which are at greater risk of fire. "
            "The solution may be more and denser housing near urban and suburban cores.")
st.markdown("   -   Putting in place early warning systems and ensuring each populated area has an "
            "evacuation plan to avoid loss of life.")
st.markdown("   -   Creating defensible space around buildings.")
st.markdown("   -   Improvements in forest management and use of controlled burns to remove highly "
            "flammable material to reduce intensity of wildfires.")
