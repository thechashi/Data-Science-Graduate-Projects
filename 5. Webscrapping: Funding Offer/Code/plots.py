import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('funding_info2.csv')
df = df[df['providing_assitantship']==1]
# =============================================================================
# df['faculty_areaname'].value_counts().plot(kind='bar')
# =============================================================================

ax = df['faculty_areaname'].value_counts().plot.bar()
ax.bar_label(ax.containers[0], label_type="edge")
plt.title('Funding offer count in differecnt areas of three Universities: CMU, UIUC and FSU')
plt.xlabel('Available Offers')
plt.ylabel('Area')
plt.legend(loc="upper right")
plt.show()

all_df = pd.read_csv('all_faculty_info.csv')
all_df = all_df.drop(all_df[all_df['faculty_areaname'] == 'unknown'].index)

top_areas = all_df['faculty_areaname'].value_counts().head(10)
ax = top_areas.plot(kind='pie', autopct='%1.1f%%')

# Remove the legend and label from the pie chart
ax.set_ylabel('')
ax.legend().remove()
plt.title('Top 10 Areas with the Highest Faculty Population')

# Show the plot
plt.show()

ml_faculties = all_df[all_df['faculty_areaname']=='ml']
ml_faculties = ml_faculties.sort_values('publications', ascending=False)
ml_faculties = ml_faculties.loc[:, ['faculty_name', 'publications', 'university_name']]
print(ml_faculties.head(7))

# Sort the dataframe by the 'publications' column in descending order
ml_faculties = ml_faculties.sort_values('publications', ascending=False)

# Get the top 5 rows of the sorted dataframe
top_faculties = ml_faculties.head(5)

# Plot a horizontal bar chart of the 'publications' column for the top 5 faculties
ax = top_faculties.plot(kind='barh', x='faculty_name', y='publications')

# Add the publication count and faculty count above each bar in the chart
for index, row in top_faculties.iterrows():
    ax.text(row['publications']+1, index, row['publications'], ha='left', va='center')
    ax.text(row['publications']+1, index-0.2, f"{row['publications']} ({index+1})", ha='left', va='center')

# Set the x-axis label
ax.set_xlabel('Number of Publications')

# Set the y-axis label with faculty names and university names
y_label = 'Faculty Name\nUniversity Name'
ax.set_ylabel(y_label)

# Add the university names to the y-axis label
for i, name in enumerate(top_faculties['university_name']):
    ax.text(0, i, name, ha='left', va='center')

# Reverse the order of the y-axis ticks to show the largest bar at the top
ax.invert_yaxis()
ax.bar_label(ax.containers[0], label_type="edge")
# Set the title of the plot
plt.title('Top 5 Faculties in ML by Number of Publications (2012-2022)')

# Show the plot
plt.show()
