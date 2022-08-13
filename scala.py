# Scala
# With almost 30k commits and a history spanning over ten years, Scala is a mature programming language. 
# It is a general-purpose programming language that has recently become another prominent language for data scientists.

# Scala is also an open source project. Open source projects have the advantage that their entire development histories -- who made changes, what was changed, code reviews, etc. -- are publicly available.

# We're going to read in, clean up, and visualize the real world project repository of Scala that spans data from a version control system (Git) as well as a project hosting site (GitHub). We will find out who has had the most influence on its development and who are the experts.

# Importing pandas
import pandas as pd

# Importing matplotlib
import matplotlib.pyplot as plt

# Loading in the data
pulls_one = pd.read_csv('Datasets/pulls_2011-2013.csv')
pulls_two = pd.read_csv('Datasets/pulls_2014-2018.csv')
pull_files = pd.read_csv('Datasets/pull_files.csv')

#printing the DataFrames to get an idea about the data structures
print(pulls_one)
print(pulls_two)
print(pull_files)

# Append pulls_one to pulls_two
pulls = pulls_one.append(pulls_two)

# Convert the date for the pulls object
pulls['date'] = pd.to_datetime(pulls['date'], utc = True)

# understand the structure of the resulting pulls dataframe
print(pulls)

# Merge the two DataFrames
data = pulls.merge(pull_files, on = 'pid')

# unerstand the structure of the merged dataframe
print(data)

# Create a column that will store the month
data['month'] = data['date'].dt.month

# Create a column that will store the year
data['year'] = data['date'].dt.year

# Group by the month and year and count the pull requests
counts = data.groupby(['month', 'year'])['pid'].count()
print(counts)

# Plot the results
counts.plot(kind='bar', figsize = (12,4))
plt.show()

# Group by the submitter
by_user = data.groupby('user')['pid'].count()

# Plot the histogram
plt.hist(by_user)
plt.show()

# Identify the last 10 pull requests
last_10 = pulls.nlargest(10, 'date')
print(last_10)

# Join the two data sets
joined_pr = last_10.merge(pull_files, on = 'pid')
print(joined_pr)

# Identify the unique files
files = set(joined_pr['file'].unique())

# Print the results
print(files)

# This is the file we are interested in:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Identify the commits that changed the file
file_pr = pull_files[pull_files['file'] == file]
print(file_pr)

# Count the number of changes made by each developer
file_pr = file_pr.merge(pulls[['pid', 'user']], on = 'pid')

author_counts = file_pr.groupby('user').count()

# Print the top 3 developers
print(list(author_counts.nlargest(3, 'pid').index))

file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests that changed the target file
file_pr = file_pr = pull_files[pull_files['file'] == file]

# Merge the obtained results with the pulls DataFrame
joined_pr = file_pr.merge(pulls, on = 'pid')
print(joined_pr)

# Find the users of the last 10 most recent pull requests
users_last_10 = set(joined_pr.nlargest(10, 'date')['user'])

# Printing the results
print(users_last_10)

# The developers we are interested in
authors = ['xeno-by', 'soc']

# Get all the developers' pull requests
by_author = pulls[pulls['user'].isin(authors)]

# Count the number of pull requests submitted each year
counts = by_author.groupby([by_author['user'], by_author['date'].dt.year]).agg({'pid': 'count'}).reset_index()
print(counts)

# Convert the table to a wide format
counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)
print(counts_wide)

# Plot the results
counts_wide.plot(kind='bar')
plt.show()

authors = ['xeno-by', 'soc']
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests submitted by the authors, from the `data` DataFrame
by_author = data[data['user'].isin(authors)]
print(by_author)

# Select the pull requests that affect the file
by_file = by_author[by_author['file'] == file]

# Group and count the number of PRs done by each user each year
grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()
print(grouped)

# Transform the data into a wide format
by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)
print(by_file_wide)

# Plot the results
by_file_wide.plot(kind='bar')
plt.show()