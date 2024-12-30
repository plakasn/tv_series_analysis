# IMDb Movie Ratings Analysis

This project explores IMDb movie ratings data, combining information from multiple datasets to analyze patterns, trends, and insights related to average ratings, vote counts, genres, and more.

## Features

- **Data Cleaning and Integration**: Merged datasets (`title_basics_df` and others) into a unified DataFrame (`rating_df`) for comprehensive analysis.
- **Descriptive Statistics**: Summary statistics for `averageRating` and `numVotes`, providing insights into movie rating distributions.
- **Genre Analysis**: Exploration of how genres impact ratings and popularity.
- **Advanced Queries**: Filtering and sorting for targeted analysis of top-rated movies, most popular titles, and other key metrics.

## Prerequisites

To run this project, ensure you have the following installed:

- Python 3.7+
- Pandas
- NumPy
- Matplotlib 
## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/imdb-movie-ratings-analysis.git
   cd imdb-movie-ratings-analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place the IMDb datasets in the `data/` directory.

4. Run the analysis script:
   ```bash
   python analysis.py
   ```

## Usage

The script performs the following steps:
1. Loads IMDb datasets and merges them into a unified DataFrame.
2. Cleans and preprocesses data for analysis.
3. Computes key statistics and outputs insights to the console or a report.

Modify the script as needed to explore additional questions or generate visualizations.

## Contributions

Contributions are welcome! Feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
