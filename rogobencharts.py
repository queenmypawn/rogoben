# Data manipulation
import pandas as pd

# Graphs
import plotly.graph_objects as go

# Store the .csv file as a DataFrame for using data
df = pd.read_csv('.\\HHCAHPS.csv')

# Number of rows
numRows = len(df.index)

# Chart 1:

# Get the average star rating and store it in respective lists.

# Get the keys and store them in a list
ssr = 'HHCAHPS Survey Summary Star Rating'
prof = 'Star Rating for health team gave care in a professional way'
comm = 'Star Rating for health team communicated well with them'
disc = 'Star Rating team discussed medicines, pain, and home safety'
care = 'Star Rating for how patients rated overall care from agency'
c1_keys = [ssr, prof, comm, disc, care]

# Initialize the average values.
ssrAvg = 0
profAvg = 0
commAvg = 0
discAvg = 0
careAvg = 0

# We need to create a unique number of rows for each column
# because 'Not Available' entries will drag down the Star Rating.
ssrRowCount = 0
profRowCount = 0
commRowCount = 0
discRowCount = 0
careRowCount = 0

# Get the values, i.e. average star ratings, for each key.
for i in range(numRows):
	if df[ssr][i].isdigit():
		ssrAvg += int(df[ssr][i])
		ssrRowCount += 1

	if df[prof][i].isdigit():
		profAvg += int(df[prof][i])
		profRowCount += 1

	if df[comm][i].isdigit():
		commAvg += int(df[comm][i])
		commRowCount += 1

	if df[disc][i].isdigit():
		discAvg += int(df[disc][i])
		discRowCount += 1

	if df[care][i].isdigit():
		careAvg += int(df[care][i])
		careRowCount += 1

ssrAvg = ssrAvg/ssrRowCount
profAvg = profAvg/profRowCount
commAvg = commAvg/commRowCount
discAvg = discAvg/discRowCount
careAvg = careAvg/careRowCount

c1_values = [ssrAvg, profAvg, commAvg, discAvg, careAvg]

# Creation of the chart
c1 = go.Figure([go.Bar(
	x = c1_keys,
	y = c1_values,
	)
])

# Prettifying the bar chart
c1.update_layout(
	title = 'HHCAHPS Average Star Ratings',
	title_x = 0.5, # Centralizing the title
	yaxis = dict(
		range = [0, 5],
		dtick = 1,
		autorange = False
		),
	)

# Chart 2:

# Get the keys
nursing = 'Offers Nursing Care Services'
pTherapy = 'Offers Physical Therapy Services'
oTherapy = 'Offers Occupational Therapy Services'
speech = 'Offers Speech Pathology Services'
social = 'Offers Medical Social Services'
hAid = 'Offers Home Health Aide Services'
c2_keys = [nursing, pTherapy, oTherapy, speech, social, hAid]

# Get the number of Yes/No's for each key (category)
nursingYes = 0
nursingNo = 0
pTherapyYes = 0
pTherapyNo = 0
oTherapyYes = 0
oTherapyNo = 0
speechYes = 0
speechNo = 0
socialYes = 0
socialNo = 0
hAidYes = 0
hAidNo = 0

for i in range(numRows):
	if df[nursing][i] == 'Yes':
		nursingYes += 1
	if df[nursing][i] == 'No':
		nursingNo += 1

	if df[pTherapy][i] == 'Yes':
		pTherapyYes += 1
	if df[pTherapy][i] == 'No':
		pTherapyNo += 1

	if df[oTherapy][i] == 'Yes':
		oTherapyYes += 1
	if df[oTherapy][i] == 'No':
		oTherapyNo += 1

	if df[speech][i] == 'Yes':
		speechYes += 1
	if df[speech][i] == 'No':
		speechNo += 1

	if df[social][i] == 'Yes':
		socialYes += 1
	if df[social][i] == 'No':
		socialNo += 1

	if df[hAid][i] == 'Yes':
		hAidYes += 1
	if df[hAid][i] == 'No':
		hAidNo += 1

# Store and convert the values as percents
# It is easier to use a double y-axis displaying percents and numbers this way
c2_valuesYes = [nursingYes, pTherapyYes, oTherapyYes, speechYes, socialYes, hAidYes]
c2_valuesNo = [nursingNo, pTherapyNo, oTherapyNo, speechNo, socialNo, hAidNo]

c2_valuesYes = [category/numRows for category in c2_valuesYes]
c2_valuesNo = [category/numRows for category in c2_valuesNo]

# Creation of the chart
c2 = go.Figure([
	go.Bar(
		x = c2_keys,
		y = c2_valuesYes,
		name = 'Yes',
		yaxis = 'y1'
	),
	go.Bar(
		x = c2_keys,
		y = c2_valuesNo,
		name = 'No',
		yaxis = 'y1'
		),
	go.Bar(
		yaxis='y2' # Creates a 3rd bar graph with no data but allows the
				   # 2nd y-axis to appear without creating dependencies.
		)
])

# Prettifying the bar chart
c2.update_layout(
	title = 'HHCAHPS Medical Services Offered',
	title_x = 0.5, # Centralizing the title
	yaxis = dict(
		range = [0, 1],
		tickformat = '.0%',
		),
	yaxis2 = dict(
		range = [0, numRows],
		dtick = numRows/10,
		autorange = False,
		overlaying = 'y',
		side='right',
		),
	legend = dict(
		x = 1.1, # So the legend doesn't overlap the second y-axis
		)
	)

# Chart 3:

# Get the number of different types of ownerships
# All types of ownerships are guaranteed accounted for by calling the function
# df['Type of Ownership'].unique()

# Get the keys
tos = 'Type of Ownership'

oha = 'Official Health Agency'
local = 'Local'
vna = 'Visiting Nurse Association'
hbp = 'Hospital Based Program'
cgv = 'Combination Government Voluntary'
skfbp = 'Skilled Nursing Facility Based Program'
ohaCount = 0
localCount = 0
vnaCount = 0
hbpCount = 0
cgvCount = 0
skfbpCount = 0
c3_keys = [oha, local, vna, hbp, cgv, skfbp]

# Get the values for each key

for i in range(numRows):
	if df[tos][i] == oha:
		ohaCount += 1

	if df[tos][i] == local:
		localCount += 1

	if df[tos][i] == vna:
		vnaCount += 1

	if df[tos][i] == hbp:
		hbpCount += 1

	if df[tos][i] == cgv:
		cgvCount += 1

	if df[tos][i] == skfbp:
		skfbpCount += 1

# Store and convert the values as percents
# It is easier to use a double y-axis displaying percents and numbers this way
c3_values = [ohaCount, localCount, vnaCount, hbpCount, cgvCount, skfbpCount]
c3_values = [category/numRows for category in c3_values]

# Creation of the chart
c3 = go.Figure([
	go.Bar(
		x = c3_keys,
		y = c3_values,
		yaxis = 'y1'
	),
	go.Bar(
		yaxis='y2' # Creates a 3rd bar graph with no data but allows the
				   # 2nd y-axis to appear without creating dependencies.
		)
])

# Prettifying the bar chart
c3.update_layout(
	title = 'HHCAHPS Types of Ownerships',
	title_x = 0.5, # Centralizing the title
	yaxis = dict(
		range = [0, 1],
		tickformat = '.0%',
		),
	yaxis2 = dict(
		range = [0, numRows],
		dtick = numRows/10,
		autorange = False,
		overlaying = 'y',
		side='right',
		),
	)