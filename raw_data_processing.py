from data_config import *

def csv_to_dat(filename):
	ifile = open(filename + '.csv', 'r')
	ofile = open(filename + '.dat', 'w')
	ifile.readline()
	for line in ifile:
		lst = line.split(',')
		ofile.write(('::').join(lst))
	ifile.close()
	ofile.close()

def get_movieId_mapping(data):
	dict_rawId_newId = {}
	movie_file = open(data['movies'], 'r')
	count = 1
	for line in movie_file:
		lst = line.split('::')
		dict_rawId_newId[lst[0]] = str(count)
		count += 1
	movie_file.close()
	return dict_rawId_newId

def get_userId_mapping(data):
	dict_rawId_newId = {}
	ratings_file = open(data['ratings'], 'r')
	count = 0
	rawId = ''
	for line in ratings_file:
		lst = line.split('::')
		if lst[0] != rawId:
			count += 1
			rawId = lst[0]
			dict_rawId_newId[lst[0]] = str(count)
	ratings_file.close()
	return dict_rawId_newId

def modify_movie_id(data, dict_movie):
	movies_file = open(data['movies'], 'r')
	movies_new = open(data['movies_new'], 'w')
	for line in movies_file:
		lst = line.split('::')
		lst[0] = dict_movie[lst[0]]
		movies_new.write(('::').join(lst))
	movies_file.close()
	movies_new.close()

def modify_ratings_file(data, dict_movie, dict_user):
	ratings_file = open(data['ratings'], 'r')
	ratings_new = open(data['ratings_new'], 'w')
	for line in ratings_file:
		lst = line.split('::')
		lst[0] = dict_user[lst[0]]
		lst[1] = dict_movie[lst[1]]
		ratings_new.write(('::').join(lst))
	ratings_file.close()
	ratings_new.close()

"""
tags user set is different from ratings user set.
"""
def modify_tags_file(data, dict_movie, dict_user):
	tags_file = open(data['tags'], 'r')
	tags_new = open(data['tags_new'], 'w')
	for line in tags_file:
		lst = line.split('::')
		lst[0] = dict_user[lst[0]]
		lst[1] = dict_movie[lst[1]]
		tags_new.write(('::').join(lst))
	tags_file.close()
	tags_new.close()

def process_raw_data(data):
	dict_movie = get_movieId_mapping(data)
	dict_user = get_userId_mapping(data)
	modify_movie_id(data, dict_movie)
	modify_ratings_file(data, dict_movie, dict_user)

def prune_ratings_file(data):
	"""
	Only save the userId movieId ratings
	"""
	ratings_file = open(data['ratings_new'], 'r')
	ratings_prune = open(data['ratings_prune'], 'w')
	for line in ratings_file:
		lst = line.split('::')
		lst = [lst[0], lst[1], lst[2]]
		ratings_prune.write(('\t').join(lst) + '\n')
	ratings_file.close()
	ratings_prune.close()

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    print 1