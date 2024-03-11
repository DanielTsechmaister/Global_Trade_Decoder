# Global Trade Decoder with Pandas library

## Introduction
Global Trade Decoder is a Python project for analyzing international agricultural trade data. It aims to uncover insights and patterns in global import and export flows.

## Class Initialization
The `Preprocess_Data` class is initialized with the database loaded into a table named `df`, which is a public instance DataFrame. You can create an instance of this class as follows:

```python
from Preprocess_Data import Preprocess_Data

# Initialize the Preprocess_Data object
data = Preprocess_Data()
```

# Functions

 1. intro():
- Description: This function provides an introductory overview of the dataset. It prints the column names of the `df' table, its dimensions, and basic information about the content of the table columns.
- Input: None (only the `self' object).
- Output: None.

 2. object_describe(colname):
- Description: This function is used to describe columns that are of type object (categories or strings). It prints the unique number of occurrences in the specified column and the number of repetitions for each unique instance in the column.
- Input:
   - `colname`: Name of the column to describe.
- Output: A pandas Series containing the number of repetitions for each unique instance in the specified column.

3. all_describe(num):
- Description: This recursive function goes through all the columns in the database and describes them according to their type. If a column is numeric, it prints its percentile distribution. Otherwise, it uses the `object_describe` function to describe the column content. It uses the `issubdtype` function from the numpy library to distinguish between numeric and non-numeric columns.
- Input:
   - `num`: The position of a column in the data table `df`.
- Output: None.

4. zeros_omit():
- Description: This function operates on the `df` database and deletes rows in which the "Value" column contains 0 or NaN (lack). After deleting the rows, it initializes the index of the table.
- Input: None (only the `self' object).
- Output: True when finished.

5. filt_top_areas_by_unit(u, n):
- Description: This function receives a category `u` from the "Unit" column and a number `n`. It reduces the `df` table by keeping only the rows where the units in the "Unit" column match `u`. After the initial filtering, it checks how many occurrences there are in the table for each country (under the 'Area' column) and further reduces `df' to contain only the top `n` states with the highest number of occurrences.
- Input:
   - `u`: Possible category from the "Unit" column, which can be '$US 1000' or 'tonnes'.
   - `n`: Number of top states to keep in the final table.
- Output: None.

6. cols_drop(columns_to_drop):
- Description: This function receives a list of column names and removes these columns from the `df' database.
- Input:
   - `columns_to_drop`: List of column names to be removed.
- Output: None.

7. calc_stats_by_factors(factors, vals, funcs):
- Description: This function receives a data table (DataFrame), a list of names of categorical columns (`factors`), a numeric column name (`vals`), and a list of statistical functions (`funcs`). It returns a statistical summary table (a collection of outputs of the functions in `funcs`) of the values in the numeric column (`vals`) divided by categories (`factors`).

8. factors_by_norm(cols):
- Description: This function accepts a list of category columns (`cols`). It normalizes the "Value" column per category from the categories that appear in the columns `cols`. It adds a column called "val_normed," which contains the normalized values, to the `df' table.
- Input:
   - `cols`: List of category columns.
- Output: None.

9. factor_by_split(factor, val):
- Description: This function receives the name of a categorical column (`factor`) and a possible value (`val`) from this column. It extracts from the `df' table the rows in which the value `val' appears in the `factor' column. The function saves a local copy of this slice from the parent table and returns it as output. Before returning the output, the function initializes the number of rows (index) of the reduced table so that they will be running numbers without saving their original position.

10. dfs_merge(series1, series2, colnames):
- Description: This function receives two Series with common indexes (`series1` and `series2`) and a list of column names (`colnames`). It merges the two series to create a new DataFrame with two columns, containing all the common elements from both series (inner join). The function returns the consolidated DataFrame.

11. cols_diff_apply(d, col1, col2, newcol):
- Description: This function receives a data table `d`, the names of two numeric columns (`col1` and `co the name of another column (`newcol`). It invokes the helper function `cols_diff` using the `apply` method on the data table `d`, where the inputs to `cols_diff` are `col1` and `col2`, and the operation is applied along the column axis. The output of `apply` with `cols_diff` is placed in a new column called `newcol` in the table `d`. The function returns the modified table `d`.
- Input:
  - `d`: Data table.
  - `col1`: Name of the first numeric column.
  - `col2`: Name of the second numeric column.
  - `newcol`: Name of the new column to store the differences.
- Output: The modified table `d`.

12. cols_diff(dat, col1, col2):
- Description: This subfunction accepts a data table `dat` and two column names (`col1` and `col2`). It returns a Series of differences between the values in `col1` and `col2` columns from the `dat` table.

These functions together provide a comprehensive toolkit for preprocessing and analyzing the data stored in 'pickle.data'.
