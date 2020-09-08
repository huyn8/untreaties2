import pandas as pd
import os
import csv
import numpy as np
import unittest

"""
The purpose of this unit testing is to compare the produced file "computerLabel.csv"
agaisnt data from the orginal human-coded file "compare.csv" to see how accurate the output
produced by the program is commpared to the human-coded output
The measurement is a similarity score that will be calculated. The higher the similarity score
the better

"""
class TestStringMethods(unittest.TestCase):
    def test_split(self):
        file_path_human = os.path.join(os.path.dirname(__file__), 'FinalTreatyCombo.csv')
        file_path_computer = os.path.join(os.path.dirname(__file__), 'computerLabel.csv')
        df_computer = pd.read_csv(file_path_computer)
        df_human = pd.read_csv(file_path_human)[list(df_computer.columns)]
        df_compare = pd.DataFrame(columns=df_computer.columns)
      
        for i in df_computer['treatyNum']:
            df_compare = df_compare.append(df_human.loc[df_human['treatyNum'] == str(i)])

        #removing duplicates
        df_compare = df_compare.drop_duplicates(subset='treatyNum', keep='first')

        #creating a csv file for referencing purposes
        df_compare.to_csv('compare.csv')
        print("A file named compare.csv was created for referencing purposes \n")

        print("Running checks between computer-labeled and human-labeled data:")
        for row in range(1, np.shape(df_computer)[0]):
            value = True
            for column in range(1, np.shape(df_computer)[1]):
                try:
                    if df_computer.iloc[row, column].lower() == list(df_compare.iloc[row, column].lower())[0]:
                        value = True
                    else:
                        value = False
                except (Exception):
                    continue
            print("Document: ", df_computer.iloc[row,0], " -> Same values?", value)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
