import unittest
import sys
import os

# Подключаем папку src для импортов
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.triangle import calculate_triangle


class TestTriangle(unittest.TestCase):

    # --- 1. Позитивные тесты (Существующие треугольники) ---
    def test_equilateral_triangle_positive(self):
        t_type, coords = calculate_triangle("5", "5", "5")
        self.assertEqual(t_type, "равносторонний")
        self.assertNotEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_equilateral_triangle_float_inputs(self):
        t_type, _ = calculate_triangle("3.5", "3.5", "3.5")
        self.assertEqual(t_type, "равносторонний")

    def test_isosceles_triangle_sides_a_b_equal(self):
        t_type, _ = calculate_triangle("7", "7", "10")
        self.assertEqual(t_type, "равнобедренный")

    def test_isosceles_triangle_sides_b_c_equal(self):
        t_type, _ = calculate_triangle("10", "7", "7")
        self.assertEqual(t_type, "равнобедренный")

    def test_scalene_triangle_classic_3_4_5(self):
        t_type, _ = calculate_triangle("3", "4", "5")
        self.assertEqual(t_type, "разносторонний")

    def test_scalene_triangle_floats(self):
        t_type, _ = calculate_triangle("4.5", "6.2", "8.1")
        self.assertEqual(t_type, "разносторонний")

    # --- 2. Несуществующие треугольники ---
    def test_non_triangle_sum_equal_third_side(self):
        """Проверка 0.1 + 0.2 = 0.3"""
        t_type, coords = calculate_triangle("0.1", "0.2", "0.3")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_non_triangle_impossible_sides(self):
        t_type, coords = calculate_triangle("1", "2", "10")
        self.assertEqual(t_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_non_triangle_with_zero_side(self):
        t_type, _ = calculate_triangle("0", "5", "5")
        self.assertEqual(t_type, "не треугольник")

    def test_non_triangle_with_negative_side(self):
        t_type, _ = calculate_triangle("-3", "4", "5")
        self.assertEqual(t_type, "не треугольник")

    def test_non_triangle_all_zeros(self):
        t_type, _ = calculate_triangle("0", "0", "0")
        self.assertEqual(t_type, "не треугольник")

    # --- 3. Некорректный (нечисловой) ввод ---
    def test_invalid_input_letters(self):
        t_type, coords = calculate_triangle("abc", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_invalid_input_empty_string(self):
        t_type, coords = calculate_triangle("", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_invalid_input_none_value(self):
        t_type, coords = calculate_triangle(None, "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_invalid_input_special_symbols(self):
        t_type, coords = calculate_triangle("5@", "4", "5")
        self.assertEqual(t_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    # --- 4. Проверка координат и масштабирования ---
    def test_coordinates_within_100x100_grid(self):
        _, coords = calculate_triangle("10", "10", "10")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_coordinates_tuple_length(self):
        _, coords = calculate_triangle("3", "4", "5")
        self.assertEqual(len(coords), 3)

    def test_large_numbers_scaling(self):
        t_type, coords = calculate_triangle("1000", "1000", "1000")
        self.assertEqual(t_type, "равносторонний")
        for x, y in coords:
            self.assertTrue(0 <= x <= 100)

    def test_very_small_floats(self):
        t_type, _ = calculate_triangle("0.001", "0.001", "0.001")
        self.assertEqual(t_type, "равносторонний")

    def test_precision_floats_isosceles(self):
        t_type, _ = calculate_triangle("5.000001", "5.000001", "8.0")
        self.assertEqual(t_type, "равнобедренный")


if __name__ == "__main__":
    unittest.main()