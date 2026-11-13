# Example 5: Ghibli Movie
# Difficulty: Intermediate

count = 0
total_movies = int(input("How many Ghibli movies do you want to list? "))

while count < total_movies:
    movie = input("Enter a Ghibli movie title: ")
    print(movie, "has been added to your collection!")
    count += 1

print("Your Ghibli movie collection is complete!")
print("Total movies collected:", count)
