# -*- coding: utf-8 -*-
# COG complained about byte characters, which is solved by this^

#Travis Torline: CS1300 Fall 2017
# Recitation: 209 – TA Ganesh
#
#Assignment 10

import os #this is used for checking if the file is empty

#read_books take a file as a parameter. It checks to see if the file exists and
#if the file is empty or not. If the file exists and has data, it fills a list
#with other lists; these lists consist of the author's name and their book.
#the 'container' list gets retruned.
def read_books(filename):

    #use a try-except to see if the file exists. If it doesn't return None
    #if it does exist, then run the code to parse the file.
    try:
        book_input_file = open(filename , 'r')
    except:
        return None
    else:
        book_list = []

        #Found this code on Stack Overflow
        #this os function returns the amount of bytes in a file.
        #If there's 0 bytes, the file is empty!
        if os.stat(filename).st_size == 0:
            return book_list
        else:
            #go through every line and split on the comma
            #append the author and the book to a list, making sure to strip newline or spaces
            #append that list to book_list
            for line in book_input_file:
                current_list = []

                split_line = line.split(',')

                current_list.append(split_line[1].strip())
                current_list.append(split_line[0].strip())

                book_list.append(current_list)

    book_input_file.close()
    return book_list
################################################################################

#read_users takes a file as a parameter. It checks to see if the file exists and
#to see if the file is empty or not. If the file exists and is filled, it fills
#a dictionary with user names as keys and their ratings as values. It then returns
#that dictionary.
def read_users(user_file):
    #use a try-except to check whether or not the file exists
    try:
        users_input_file = open(user_file)
    except:
        return None
    else:

        user_dictionary = {}

        #if the file is empty, return an empty list
        if os.stat(user_file).st_size == 0:
            return user_dictionary

        #go through every line, strip the newline character, and store in a list
        #the first item is always the key, the rest can be converted to ints
        #and stored in the ratings list
        for line in users_input_file:
            user_ratings_list = line.strip().split(' ')

            #since .split returns a list, the first element is the name
            #then, using list comprehension, convert every other element to int
            user_dictionary[user_ratings_list[0]] = [int(x) for x in user_ratings_list[1:len(user_ratings_list)]]

    return user_dictionary
################################################################################

#calculate_average_rating takes a dictionary of keys = users, values = ratings
#as a parameter. For every index, it finds the average of the index. Note that
#if the rating is 0, then the user has NOT read the book and will not be counted
#towards the average rating of that index.
def calculate_average_rating(ratings_dict):

    list_of_averages = []

    #need to get the length of one value(they all have the same length)
    #this is why the for loop breaks immediately
    #this length will be used in future iteration.
    length_of_value = 0
    for key, value in ratings_dict.items():
        length_of_value = len(value)
        break

    #using that length, go through every book for every user
    for i in range(0 , length_of_value):
        sum_of_ratings = 0
        num_of_ratings = 0
        for key, value in ratings_dict.items():

            sum_of_ratings += value[i]

            #If the user has not read the book, the denominator should NOT increase
            if value[i] != 0:
                num_of_ratings += 1

        #append 0 if none have read, otheerwise append the average
        if num_of_ratings == 0:
            list_of_averages.append(0)
        else:
            list_of_averages.append(float(sum_of_ratings) / num_of_ratings)

    return list_of_averages
################################################################################

def lookup_average_rating(index, book_dict, average_ratings_list_dict):
    #Note that book_dict is a list of lists, so take the index list.
    #Inside that list, the author is index 1 and book is index 0
    return "(%.2f) %s by %s" % (average_ratings_list_dict[index] , book_dict[index][0] , book_dict[index][1])
################################################################################

#CREATING THE RECOMMENDER CLASS

#The recommender class is initialized with a file for the authors and books and
#a file for the readers and their ratings. It has empty member variables that
#are filled by calling methods to read files passed through. It can also
#calculate the average rating for a book, find a book and its rating, calculate
#the similairty bewtween users, and recommend books based on similarity scores.
class Recommender(object):

    #the Recommender class will be initialized with three lists
    #two of the lists will be immediately filled with the files passed through.
    def __init__(self, books_filename, ratings_filename):
        self.book_list = []
        self.user_dictionary = {}
        self.average_ratings_list = []
        self.read_books(books_filename)
        self.read_users(ratings_filename)

################################################################################

    #this function is the same as the read_books function as above,
    #just formatted to fit the class.
    def read_books(self, file_name):
        try:
            book_input_file = open(file_name , 'r')
        except:
            return
        else:
            #Found this code on Stack Overflow
            #this os function returns the amount of bytes in a file.
            #If there's 0 bytes, the file is empty!
            if os.stat(file_name).st_size == 0:
                return
            else:
                #go through every line and split on the comma
                #append the author and the book to a list, making sure to strip newline or spaces
                #append that list to book_list
                for line in book_input_file:
                    current_list = []

                    split_line = line.split(',')

                    current_list.append(split_line[1].strip())
                    current_list.append(split_line[0].strip())

                    self.book_list.append(current_list)

        book_input_file.close()
        return
################################################################################

    #this function is the same as the read_users function as above,
    #just formatted to fit the class.
    def read_users(self, file_name):
            #use a try-except to check whether or not the file exists
            try:
                users_input_file = open(file_name)
            except:
                return
            else:
                #if the file is empty, return None
                if os.stat(file_name).st_size == 0:
                    return

                #go through every line, strip the newline character, and store in a list
                #the first item is always the key, the rest can be converted to ints
                #and stored in the ratings list
                for line in users_input_file:
                    user_ratings_list = line.strip().split(' ')

                    #since .split returns a list, the first element is the name
                    #then, using list comprehension, convert every other element to int
                    self.user_dictionary[user_ratings_list[0]] = [int(x) for x in user_ratings_list[1:len(user_ratings_list)]]

            users_input_file.close()
            return
################################################################################

    #this function is the same as the calculate_average_rating function as above,
    #just formatted to fit the class.
    def calculate_average_rating(self):
        #need to get the length of one value(they all have the same length)
        #this is why the for loop breaks immediately
        #this length will be used in future iteration.
        length_of_value = 0
        for key, value in self.user_dictionary.items():
            length_of_value = len(value)
            break

        #using that length, go through every book for every user
        for i in range(0 , length_of_value):
            sum_of_ratings = 0
            num_of_ratings = 0
            for key, value in self.user_dictionary.items():

                sum_of_ratings += value[i]

                #If the user has not read the book, the denominator should NOT increase
                if value[i] != 0:
                    num_of_ratings += 1

            #append 0 if none have read, otherwise append the average
            if num_of_ratings == 0:
                self.average_ratings_list.append(0)
            else:
                self.average_ratings_list.append(float(sum_of_ratings) / num_of_ratings)

################################################################################

    #this function is the same as the lookup_average_rating function as above,
    #just formatted to fit the class.
    def lookup_average_rating(self, index):

        #Fill all member variables using file-reading methods.
        #read-users need not be called here, as it is called in
        #calculate_average_rating
        self.calculate_average_rating()

        #Note that book_dict is a list of lists, so take the index list.
        #Inside that list, the author is index 1 and book is index 0
        return "(%.2f) %s by %s" % (self.average_ratings_list[index] , self.book_list[index][0] , self.book_list[index][1])

################################################################################

    #the calc_similarity function takes in two users as parameters. For every
    #rating each user has, it finds the "similarity". similarity =
    #(element0 * element0) + (element1 * element1)...etc
    def calc_similarity(self, user1, user2):
        #read in the users and their ratings

        similarity = 0

        #get the ratings values from the dictionary
        ratings_user_one = self.user_dictionary[user1]
        ratings_user_two = self.user_dictionary[user2]

        #iterate through each element and calculate the similarity - one score
        #times the other score - and add it to total similarity
        for i in range(0, len(self.user_dictionary[user1])):

            similarity += ratings_user_one[i] * ratings_user_two[i]

        return int(similarity)

################################################################################

    #get_most_similar_user takes a user_id as a parameter. It goes through
    #the user_dictionary and calculates similarity for every user
    #in order to find the highest similairty. It returns the user with which
    #current_user_id had the best match.
    def get_most_similar_user(self, current_user_id):

        #go through and calculate similarity for current_user_id with every
        #other user. If the similarity score is the highest yet, set that
        #user as the best_match.
        best_match = ""
        best_score = 0
        for key in self.user_dictionary:

            #don't find the similarity if we're checking the user against themselves.
            if current_user_id == key:
                continue

            current_similarity = self.calc_similarity(current_user_id,key)

            if current_similarity > best_score:
                best_match = key
                best_score = current_similarity

        return best_match

################################################################################

    #recommend_books takes a current_user_id as a parameter. It finds the most similar
    #user, and then for every book that user has rated 3 or 5 that current_user_id
    #has rated 0, it appends that book and its rating to a list. Return that list.
    def recommend_books(self, current_user_id):

        recommendations_list = []

        best_match = self.get_most_similar_user(current_user_id)

        #store the ratings arrays for iteration
        current_user_id_ratings = self.user_dictionary[current_user_id]
        best_match_ratings = self.user_dictionary[best_match]

        #Recommender has a function lookup_average_rating that will return
        #a formatted string of the books we find as recommendations
        for i in range(0 , len(current_user_id_ratings)):
            if current_user_id_ratings[i] == 0 and best_match_ratings[i] == 3 or current_user_id_ratings[i] == 0 and best_match_ratings[i] == 5:
                recommendations_list.append(self.lookup_average_rating(i))

        return recommendations_list


#TESTING THE FUNCTIONS USING A MAIN() FUNCTION
def main():
    print("\nTesting the read_books function - line 1 should be None, line 2 an empty list, and then a filled list should be printed:")
    print(read_books("thisfileisn'treal"))#no file in directory
    print(read_books("emptyFileForTesting.txt"))#just an empty file
    print(read_books("books_test.txt"))#the actual file

    print("\nTesting the read_users function - line 1 should be None, line 2 is an empty dictionary, and then a filled dictionary.")
    print(read_users("thisfileisn'treal"))#no file in directory
    print(read_users("emptyFileForTesting.txt"))#just an empty file
    print(read_users("ratings_test.txt"))#the actual file

    print("\nTesting the calculate_average_rating function - should output a list of floating point values.")
    user_dictionary = read_users("ratings_test.txt")
    print(calculate_average_rating(user_dictionary))

    print("\nTesting the lookup_average_rating funtion - should output the avg rating, book, and then author.")
    book_dict = read_books("books_test.txt")
    average_ratings_list = calculate_average_rating(user_dictionary)
    print(lookup_average_rating(1 , book_dict, average_ratings_list))

    print("\nTESTING CLASS RECOMMENDER:")
    testRecommender = Recommender("books_test.txt" , "ratings_test.txt")

    print("\nTesting the book_list function:")
    testRecommender.read_books("books_test.txt")
    print(testRecommender.book_list)

    print("\nTesting the read_users function:")
    testRecommender.read_users("ratings_test.txt")
    print(testRecommender.user_dictionary)

    print("\nTesting the calculate_average_rating function:")
    testRecommender.calculate_average_rating()
    print(testRecommender.average_ratings_list)

    print("\nTesting the lookup_average_rating function:")
    print(testRecommender.lookup_average_rating(7))

    print("\nTesting the calc_similarity function:")
    print(testRecommender.calc_similarity("Apollo" , "James"))

    print("\nTesting the get_most_similar_user function:")
    print(testRecommender.get_most_similar_user("Rudy_Ann"))

    print("\nTesting the recommend_books function:")
    print(testRecommender.recommend_books("Ella"))

if __name__ == '__main__':
    main()
