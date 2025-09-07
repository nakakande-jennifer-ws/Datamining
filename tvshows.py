import pandas as pd  # Import pandas library for data manipulation and analysis


# -----------------------------
# 1. Define a Show class
# -----------------------------
class Show:  # Define a class to represent Netflix shows
    def __init__(tv, show_id, title, show_type, rating, release_year, genre):  # Constructor to initialize show attributes
        tv.show_id = show_id  # Store show ID attribute
        tv.title = title  # Store show title attribute
        tv.show_type = show_type  # Store show type (movie or TV show)
        tv.rating = rating  # Store content rating (G, PG, etc.)
        tv.release_year = release_year  # Store year when show was released
        tv.genre = genre  # Store show genre(s)

    def is_family_friendly(tv):  # Method to check if show is suitable for families
        """Check if the show is suitable for family viewing"""
        family_ratings = ["G", "PG", "TV-G", "TV-PG", "TV-Y", "TV-Y7"]  # List of family-friendly ratings
        return tv.rating in family_ratings  # Returns True if show's rating is in the family-friendly list


# -----------------------------
# 2. Functions
# -----------------------------
def load_shows(df):  # Function to convert DataFrame rows to Show objects
    """
    Convert pandas DataFrame rows into a list of Show objects.
    """
    shows = []  # Initialize empty list to store Show objects
    for _, row in df.iterrows():  # Iterate through each row in the DataFrame
        # Use .get() with default values to avoid errors if data is missing
        show_id = row.get("show_id", "Unknown")  # Get show ID or use "Unknown" if missing
        title = row.get("title", "Unknown")  # Get show title or use "Unknown" if missing
        show_type = row.get("type", "Unknown")  # Get show type or use "Unknown" if missing
        rating = row.get("rating", "NR")  # Get rating or use "NR" (Not Rated) if missing
        release_year = row.get("release_year", 0)  # Get release year or use 0 if missing
        genre = row.get("listed_in", "Other")  # Get genre or use "Other" if missing

        shows.append(Show(show_id, title, show_type, rating, release_year, genre))  # Create and add Show object to list
    return shows  # Return the list of Show objects


def count_shows_by_genre(shows):  # Function to count shows in each genre
    """
    Count how many shows belong to each genre using a dictionary.
    """
    genre_count = {}  # Initialize empty dictionary to store genre counts
    for show in shows:  # Iterate through each show
        # Each show can belong to multiple genres (comma separated)
        genres = show.genre.split(", ")  # Split the genre string by comma and space
        for g in genres:  # Iterate through each individual genre
            if g not in genre_count:  # If genre not in dictionary yet
                genre_count[g] = 0  # Initialize count for that genre
            genre_count[g] += 1  # Increment count for that genre
    return genre_count  # Return dictionary of genre counts


def count_shows_by_type(shows):  # Function to count shows by type (Movie/TV Show)
    """
    Count how many shows belong to each type (Movie/TV Show)
    """
    type_count = {}  # Initialize empty dictionary to store type counts
    for show in shows:  # Iterate through each show
        if show.show_type not in type_count:  # If show type not in dictionary yet
            type_count[show.show_type] = 0  # Initialize count for that type
        type_count[show.show_type] += 1  # Increment count for that type
    return type_count  # Return dictionary of type counts


def get_shows_by_year(shows, year):  # Function to filter shows by release year
    """
    Filter shows by release year
    """
    return [show for show in shows if show.release_year == year]  # Return list of shows from specified year


def get_shows_by_rating(shows, rating):  # Function to filter shows by rating
    """
    Filter shows by rating
    """
    return [show for show in shows if show.rating == rating]  # Return list of shows with specified rating


# -----------------------------
# 3. Main Program
# -----------------------------
def main():  # Main function that runs when script is executed directly
    # Load the local CSV file directly with pandas
    df = pd.read_csv("netflix_titles.csv")  # Read the Netflix shows dataset from CSV file    
    # Quick preview of data
    print("Dataset loaded successfully! ")  # Print success message
    print("Preview of first 5 rows:")  # Print header for preview
    print(df.head())  # Display first 5 rows of the DataFrame
    
    shows = load_shows(df)  # Convert DataFrame to list of Show objects
    
    # Example: Count family-friendly shows
    family_friendly = sum(1 for show in shows if show.is_family_friendly())  # Count shows with family-friendly ratings
    print(f"Number of family-friendly shows: {family_friendly}")  # Print count of family-friendly shows
    
    # Example: Get genre distribution
    genre_counts = count_shows_by_genre(shows)  # Get dictionary of genre counts
    print("\nTop 9 genres:")  # Print header for top genres
    for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:9]:  # Sort genres by count and get top 9
        print(f"- {genre}: {count} shows")  # Print each genre and its count
    
    # Example: Count by show type
    type_counts = count_shows_by_type(shows)  # Get dictionary of type counts
    print("\nCount by show type:")  # Print header for type counts
    for show_type, count in type_counts.items():  # Iterate through each show type
        print(f"- {show_type}: {count}")  # Print each type and its count
    
    # Example: Recent shows (2021)
    recent_shows = get_shows_by_year(shows, 2021)  # Get list of shows released in 2021
    print(f"\nNumber of shows released in 2021: {len(recent_shows)}")  # Print count of 2021 shows
    print("Some examples:")  # Print header for examples
    for show in recent_shows[:40]:  # Show first 40 shows from 2021
        print(f"- {show.title} ({show.show_type})")  # Print each show's title and type
    
    # Example: TV-MA rated shows (mature audience)
    mature_shows = get_shows_by_rating(shows, "TV-MA")  # Get list of TV-MA rated shows
    print(f"\nNumber of TV-MA rated shows: {len(mature_shows)}")  # Print count of TV-MA shows

if __name__ == "__main__":  # Check if script is being run directly
    main()  # Call the main function