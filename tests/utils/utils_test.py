#!/usr/bin/env python
# coding: utf-8

import unittest

import sys

sys.path.append(".")
from src.utils.utils import number_in_words_2_numeric
from src.constants.numeric import *


class MultiplyTestCase(unittest.TestCase):

    def test_number_unit_start(self):
        result = number_in_words_2_numeric(
            "Oito palavras? Fé, Amor, generosidade, perdão, família, gentileza, resiliência e chocolate."
        )
        self.assertEqual(result, 8)

    def test_number_unit_mid(self):
        result = number_in_words_2_numeric("Uma semana tem sete dias")
        self.assertEqual(result, 7)

    def test_number_unit_end(self):
        result = number_in_words_2_numeric("Eu sou jogador número cinco")
        self.assertEqual(result, 5)

    def test_number_tens_start(self):
        result = number_in_words_2_numeric("Vinte contar um segredo!")
        self.assertEqual(result, 20)

    def test_number_tens_mid(self):
        result = number_in_words_2_numeric("Um mês tem trinta dias")
        self.assertEqual(result, 30)

    def test_number_tens_end(self):
        result = number_in_words_2_numeric("Ontem assisti Super Onze")
        self.assertEqual(result, 11)

    def test_number_complete(self):
        result = number_in_words_2_numeric("Oitenta e um anos")
        self.assertEqual(result, 81)

    def test_number_first_check(self):
        result = number_in_words_2_numeric("Oitenta e muitos")
        self.assertEqual(result, 80)

    def test_number_many_numbers(self):
        result = number_in_words_2_numeric("Cinco, seis, sete, oito...")
        self.assertEqual(result, 5)

    def test_number_many_numbers_min_age(self):
        result = number_in_words_2_numeric("Um, dois, três, quatro...")
        self.assertEqual(result, 0)

    def test_no_numbers(self):
        result = number_in_words_2_numeric("Não existe nenhum número aqui")
        self.assertEqual(result, 0)

    def test_accented_word(self):
        result = number_in_words_2_numeric("Vinte e três")
        self.assertEqual(result, 23)

    def test_units(self):
        # verifica valores de 10 - 19
        for kt, vt in units.items():
            result = number_in_words_2_numeric(vt)

            if kt <= 4:
                self.assertEqual(result, 0)
            else:
                self.assertEqual(result, kt)

    def test_special_tens(self):
        for kt, vt in special_tens.items():
            result = number_in_words_2_numeric(vt)
            self.assertEqual(result, kt)

    def test_tens(self):
        for kt, vt in tens.items():
            result = number_in_words_2_numeric(vt)
            self.assertEqual(result, kt)

            for ku, vu in units.items():
                result = number_in_words_2_numeric(vt + " E " + vu)
                self.assertEqual(result, kt + ku)


if __name__ == "__main__":
    unittest.main()
