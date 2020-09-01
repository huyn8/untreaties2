import pandas as pd
import os
import csv
import numpy as np
import unittest

class TestStringMethods(unittest.TestCase):
    def test_split(self):
        file_path_human = os.path.join(os.path.dirname(__file__), 'FinalTreatyCombo.csv')
        file_path_computer = os.path.join(os.path.dirname(__file__), 'computerLabel.csv')
        df_computer = pd.read_csv(file_path_computer)
        df_human = pd.read_csv(file_path_human)[list(df_computer.columns)]
        df_compare = pd.DataFrame(columns=df_computer.columns)

        for i in df_computer['treatyNum']:
            df_compare = df_compare.append(df_human.loc[df_human['treatyNum'] == i])
        df_compare.to_csv('compare.csv')
        print("A file named compare.csv was created for referencing purposes \n")

        print("Running checks between computer-labeled and human-labeled data:")
        for row in range(1, np.shape(df_computer)[0]):
            value = True
            for column in range(1, np.shape(df_computer)[1]):
                if df_computer.iloc[row, column].lower() == df_compare.iloc[row, column].lower():
                    value = True
                else:
                    value = False
            print("Document: ", df_computer.iloc[row,0], " -> Same values?", value)

       

        SCORE = .98 # 1 being 100% which is just a place holder at this point
        TARGET = .99 # target score can be changed later
        print("\n", "Similarity score: ", SCORE)
        print(" Target similarity score: ", TARGET)

        if SCORE != TARGET:
            print("\n Similarity score is not reached \n", "Current score: ", SCORE, " Desired score: ", TARGET)

        self.assertEqual(SCORE, TARGET)


if __name__ == '__main__':
    unittest.main()
