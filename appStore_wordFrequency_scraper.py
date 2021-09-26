from app_store_scraper import AppStore
import nltk
from nltk.corpus import stopwords
from pprint import pprint
import re

'''
Setup
  - Install "pip", the package installer for python. (https://pip.pypa.io/en/stable/installation/)
  - Install "NLTK", a platform for working with human language data. (https://www.nltk.org/install.html). We use this to filter out common English words.
  - Install "app_store_scaper". Instructions here: (https://pypi.org/project/app-store-scraper/)

  - When calling the "generate_word_count_dict" function in the code below below: modify the app_name, country, and the number_of_reviews you want to analyze.

  - To run, in your terminal, navigate to the directory where this file lives and type: 

    python3 appStore_wordFrequency_scraper.py
 '''

class WordCount:
	def __init__(self, word, count):
		self.word = word
		self.count = count

	def __str__(self):
		return "%s: %d" % (self.word, self.count)

	def __repr__(self):
		return str(self)

# generic func to fetch app store reviews and generate word count.
# note: uses the NLTK data to filter out common "stopwords" (ie: "a", "the", etc.)
def generate_word_count_dict(app_name, country_code, number_of_reviews):
	# fetches app metadata
	app = AppStore(country=country_code, app_name=app_name)
	app.review(how_many=number_of_reviews) #

	# create an object to store and associate words with their respective frequency.
	word_count_dict = {}

	# Get list of English stop words to filter out (ie: "a", "the", etc.) and convert them all to lowercase
	take_out = stopwords.words('english')
	take_out = [word.lower() for word in take_out]

	# iterate through each review
	for review_metadata in app.reviews:
		raw_review = review_metadata["review"]

		# break a single review into individual words
		review_words = raw_review.split()

		for word in review_words:

			# remove non-alphanumeric characters from each word and lowercase everything
			word_filtered = re.sub(r'\W+', '', word).lower()

			# skip words that are common
			if word_filtered not in take_out:
				if word_filtered in word_count_dict:
					word_count_dict[word_filtered] += 1
				else:
					word_count_dict[word_filtered] = 1

	return word_count_dict

# --------PROGRAM EXECUTION BEGINS HERE------------
nltk.download('stopwords')
word_count_dict = generate_word_count_dict("myfitnesspal", "us", 100)

# Uncomment to visualize the generated word count dictionary
# pprint(word_count_dict)

word_count_list = []

# transform {word : count} pair into WordCount object and add to list for sorting.
for key in word_count_dict:
	wordObject = WordCount(key, word_count_dict[key])
	word_count_list.append(wordObject)

# sort our words by frequency they were used
word_count_list.sort(key=lambda x: x.count)

# output the results
print(*word_count_list,sep='\n')
