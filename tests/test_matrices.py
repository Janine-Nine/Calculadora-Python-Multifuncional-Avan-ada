"""
Testes de matrizes e vetores: operações fundamentais e determinante.
"""

import unittest
from app.matrices import MatrixEngine
from app.validators import ValidationError


class TestMatrixEngine(unittest.TestCase):

    def setUp(self):
        self.a = [[1.0, 2.0], [3.0, 4.0]]
        self.b = [[2.0, 0.0], [1.0, 2.0]]

    def test_add(self):
        res = MatrixEngine.add(self.a, self.b)
        self.assertEqual(res, [[3.0, 2.0], [4.0, 6.0]])

    def test_subtract(self):
        res = MatrixEngine.subtract(self.a, self.b)
        self.assertEqual(res, [[-1.0, 2.0], [2.0, 2.0]])

    def test_multiply(self):
        # A(2x2) x B(2x2)
        # [1*2 + 2*1, 1*0 + 2*2] = [4, 4]
        # [3*2 + 4*1, 3*0 + 4*2] = [10, 8]
        res = MatrixEngine.multiply(self.a, self.b)
        self.assertEqual(res, [[4.0, 4.0], [10.0, 8.0]])

    def test_transpose(self):
        t = MatrixEngine.transpose(self.a)
        self.assertEqual(t, [[1.0, 3.0], [2.0, 4.0]])

    def test_determinant_2x2(self):
        # det([[1, 2], [3, 4]]) = 1*4 - 2*3 = 4 - 6 = -2
        det = MatrixEngine.determinant(self.a)
        self.assertAlmostEqual(det, -2.0)

    def test_determinant_3x3(self):
        m3 = [
            [2.0, 0.0, 1.0],
            [3.0, 0.0, 0.0],
            [5.0, 1.0, 1.0],
        ]
        # Laplace na coluna 2: det = 0 - 0 + 1 * (- (2*0 - 1*3)) = 3
        det = MatrixEngine.determinant(m3)
        self.assertAlmostEqual(det, 3.0)

    def test_vector_dot_product(self):
        u = [1.0, 2.0, 3.0]
        v = [4.0, -5.0, 6.0]
        # 1*4 + 2*(-5) + 3*6 = 4 - 10 + 18 = 12
        dot = MatrixEngine.vector_dot_product(u, v)
        self.assertEqual(dot, 12.0)

    def test_vector_norm(self):
        # ||(3, 4)|| = 5
        norm = MatrixEngine.vector_norm([3.0, 4.0])
        self.assertEqual(norm, 5.0)

    def test_incompatible_dimensions(self):
        with self.assertRaises(ValidationError):
            MatrixEngine.add([[1, 2]], [[1], [2]])


if __name__ == "__main__":
    unittest.main()
