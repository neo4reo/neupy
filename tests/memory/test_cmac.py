import numpy as np
import pandas as pd

from neupy import algorithms
from neupy.functions import errors
from base import BaseTestCase


class CMACTestCase(BaseTestCase):
    def test_cmac(self):
        input_train = np.reshape(np.linspace(0, 2 * np.pi, 100), (100, 1))
        input_train_before = input_train.copy()
        input_test = np.reshape(np.linspace(np.pi, 2 * np.pi, 50), (50, 1))
        input_test_before = input_test.copy()

        target_train = np.sin(input_train)
        target_train_before = target_train.copy()
        target_test = np.sin(input_test)

        cmac = algorithms.CMAC(
            quantization=100,
            associative_unit_size=32,
            step=0.2,
            verbose=False,
        )
        cmac.train(input_train, target_train, epochs=100)
        predicted_test = cmac.predict(input_test)
        error = errors.mae(target_test, predicted_test)

        self.assertEqual(round(error, 4), 0.0024)

        np.testing.assert_array_equal(input_train, input_train_before)
        np.testing.assert_array_equal(input_train, input_train_before)
        np.testing.assert_array_equal(target_train, target_train_before)

    def test_train_different_inputs(self):
        self.assertInvalidVectorTrain(
            algorithms.CMAC(),
            np.array([1, 2, 3]),
            np.array([1, 2, 3])
        )

    def test_predict_different_inputs(self):
        cmac = algorithms.CMAC()

        data = np.array([[1, 2, 3]]).T
        target = np.array([[1, 2, 3]]).T

        cmac.train(data, target, epochs=100)
        self.assertInvalidVectorPred(cmac, np.array([1, 2, 3]), target,
                                     decimal=2)

    def test_cmac_multi_output(self):
        input_train = np.linspace(0, 2 * np.pi, 100)
        input_train = np.vstack([input_train, input_train])

        input_test = np.linspace(0, 2 * np.pi, 100)
        input_test = np.vstack([input_test, input_test])

        target_train = np.sin(input_train)
        target_test = np.sin(input_test)

        cmac = algorithms.CMAC(
            quantization=100,
            associative_unit_size=32,
            step=0.2,
        )
        cmac.train(input_train, target_train, epochs=100)
        predicted_test = cmac.predict(input_test)
        error = errors.mae(target_test, predicted_test)

        self.assertEqual(round(error, 6), 0)
