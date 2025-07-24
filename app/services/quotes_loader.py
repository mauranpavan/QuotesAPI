import pandas as pd
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Ensure the file exists
csv_path = Path("app/data/quotes.csv")
if not csv_path.exists():
    raise FileNotFoundError(f"{csv_path} does not exist!")

try:
    # Load the CSV with semicolon separator
    quotes_df = pd.read_csv(csv_path, sep=";")
    logger.info(f"Loaded {len(quotes_df)} quotes from {csv_path}")
except pd.errors.EmptyDataError:
    raise ValueError(f"The CSV file {csv_path} is empty!")
except pd.errors.ParserError as e:
    raise ValueError(f"Error parsing CSV file {csv_path}: {e}")

# Validate expected columns. If not, returns an error with missing columns.
expected_cols = {"quote", "author", "category"}
if not expected_cols.issubset(quotes_df.columns):
    missing_cols = expected_cols - set(quotes_df.columns)
    raise ValueError(f"CSV is missing required columns: {missing_cols}")

# Remove any rows with missing essential data
quotes_df = quotes_df.dropna(subset=["quote", "author"])
logger.info(f"After cleaning: {len(quotes_df)} valid quotes available")

if len(quotes_df) == 0:
    raise ValueError("No valid quotes found after cleaning data!")

def get_all_quotes(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get a random sample of quotes.
    
    Args:
        limit: Maximum number of quotes to return (default: 10)
        
    Returns:
        List of quote dictionaries
    """
    if limit <= 0:
        return []
    
    actual_limit = min(limit, len(quotes_df))
    return quotes_df.sample(n=actual_limit).to_dict(orient="records")

def get_random_quote() -> Dict[str, Any]:
    """
    Get a single random quote.
    
    Returns:
        Dictionary containing quote, author, and category
    """
    return quotes_df.sample(n=1).to_dict(orient="records")[0]

def get_quotes_by_category(category: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get quotes filtered by category.
    
    Args:
        category: Category to filter by
        limit: Maximum number of quotes to return
        
    Returns:
        List of quote dictionaries from the specified category
    """
    if category.lower() == "all":
        return get_all_quotes(limit)
    
    filtered_df = quotes_df[quotes_df['category'].str.lower() == category.lower()]
    
    if len(filtered_df) == 0:
        return []
    
    actual_limit = min(limit, len(filtered_df))
    return filtered_df.sample(n=actual_limit).to_dict(orient="records")

def get_quotes_by_author(author: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get quotes filtered by author.
    
    Args:
        author: Author name to filter by
        limit: Maximum number of quotes to return
        
    Returns:
        List of quote dictionaries from the specified author
    """
    filtered_df = quotes_df[quotes_df['author'].str.lower().str.contains(author.lower(), na=False)]
    
    if len(filtered_df) == 0:
        return []
    
    actual_limit = min(limit, len(filtered_df))
    return filtered_df.sample(n=actual_limit).to_dict(orient="records")

def get_available_categories() -> List[str]:
    """
    Get all unique categories available in the dataset.
    
    Returns:
        List of unique category names
    """
    return sorted(quotes_df['category'].dropna().unique().tolist())

def get_available_authors() -> List[str]:
    """
    Get all unique authors available in the dataset.
    
    Returns:
        List of unique author names
    """
    return sorted(quotes_df['author'].dropna().unique().tolist())

def get_stats() -> Dict[str, Any]:
    """
    Get statistics about the quotes dataset.
    
    Returns:
        Dictionary with dataset statistics
    """
    return {
        "total_quotes": len(quotes_df),
        "unique_authors": quotes_df['author'].nunique(),
        "unique_categories": quotes_df['category'].nunique(),
        "categories": get_available_categories()
    }