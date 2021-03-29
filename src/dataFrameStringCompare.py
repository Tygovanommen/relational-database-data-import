from fuzzywuzzy import fuzz

class DataFrameStringCompare:

    # Constructor to setup shop importer
    def __init__(self, min_similarity, test_dataframe, test_column, control_dataframe, control_column):
        self.min_similarity = min_similarity
        self.test_dataframe = test_dataframe
        self.test_column = test_column
        self.control_dataframe = control_dataframe
        self.control_column = control_column

    def compare_replace_dataframe_string(self):
        for i in range(len(self.test_dataframe)):
            test_row = self.test_dataframe.loc[i, :]

            for j in range(len(self.control_dataframe)):
                control_row = self.control_dataframe.loc[j, :]
                # Compare test string row and column to control row and column. Replace test with control if > than min_similarity.
                if (fuzz.ratio(test_row[self.test_column], control_row[self.control_column]) >= self.min_similarity and fuzz.ratio(test_row[self.test_column], control_row[self.control_column]) < 100):
                    self.test_dataframe[self.test_column] = self.test_dataframe[self.test_column].str.replace(
                        test_row[self.test_column], control_row[self.control_column]
                    )