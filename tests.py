'''
Things to test: is_valid_combo function, point counting, methods
'''
import unittest

from validator import is_valid_combo

class TestIsValidCombo(unittest.TestCase):
    
    
    def test_empty_table(self):
        self.assertFalse(is_valid_combo(6, []), 'Attempting to take from empty table should return False.')
    
    def test_pick_one_equal_card(self):
        self.assertTrue(is_valid_combo(11, [11]), 'Should be able to take one equal card.')
        
    def test_pick_multiple_equal_cards(self):
        self.assertTrue(is_valid_combo(9, [9,9,9]), 'Should be able to take multiple equal cards.')
    
    def test_pick_one_different_from_hand(self):
        self.assertFalse(is_valid_combo(7, [3]), 'Taking one card different from hand should return False.')
    
    def test_larger_than_hand_chosen(self):
        self.assertFalse(is_valid_combo(5, [1, 2, 3, 4, 6]), 'Attempting to take card larger than hand should return False.')
        
    def test_same_card_in_two_combos(self):
        self.assertFalse(is_valid_combo(7, [3,4,4]), 'One card can only contribute to one combination!')
        
    def test_valid_combo_with_multiple_values(self):
        self.assertTrue(is_valid_combo(8, [4, 6, 7, 1, 4, 2]), 'Attempting legal move should return True.')
        
    def test_valid_combo_with_subcombos_of_over_three_cards(self):
        self.assertTrue(is_valid_combo(10, [6, 3, 1, 1, 2, 4, 3, 2, 2, 2, 2, 2]), 'Should be possible to combine multiple cards.')
        
    def test_valid_combo_including_duplicate_values(self):
        self.assertTrue(is_valid_combo(13, [7,6,1,8,5,12,13,12,1]), 'Attempting legal move should return True.')
    
    def test_invalid_combo_with_large_amount_of_cards(self):
        self.assertFalse(is_valid_combo(16, [11, 7, 9, 3, 6, 4, 5, 6, 8, 2, 7, 14, 1, 1, 9, 15, 10, 1, 4, 7, 13, 2]), 'Invalid move should be detected before generating subcombos.')    


    
if __name__ == '__main__':
    unittest.main()