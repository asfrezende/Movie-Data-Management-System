**Data structures project: simple movie manegement and search system.**
**PS: in order to upload this project here on GitHub, I had to use a reduced version of the ratings.csv file. Feel free to reach me out and I can send you the original file.**
This project was developed as the final assignment for the class INF01124 (taken in 2025/01) and has been slightly modified for publication. The primary objective was to apply concepts of data structures and sorting algorithms to efficiently organize, search and retrieve data.

**The system I conceptualized processess two CSV files provided by the professor:**
- Movies file (movies.csv): contains movie data;
- Users file (ratings.csv): contains simulated user ratings.

**To optimize data organization and facilitate searching, the following data structures were implemented:**
- A Hash Table to store all movie information for an easy and fast look-up;
- A TRIE to search with string inputs;
- A matrix to manage cross-referencing through the other data structures used.

The workflow is at it follows: the movies file is loaded into a temporary matrix and the movies' titles are mapped into a TRIE, with their IDs as the key; while the ratings file is mapped into a matrix that links users to their rated movies. 

**The search functionality works by:**
- Movie title: the TRIE locates the movie ID, which is used to collect the details from the Hash Table;
- User ID: the user's ratings are used on the Hash Table to pull the movies' data;
- Genre: the Hash Table is traversed to collect all movies of the given genre.
With this project, I learned the practical application of data structures and could efficiently handle large data sets in search operation, as well as integrate different data structures to create a cohesive system. Feedback and suggestions for improvement are welcome!
  
