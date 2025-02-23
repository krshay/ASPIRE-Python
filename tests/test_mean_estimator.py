import os.path
from unittest import TestCase

import numpy as np
from pytest import raises

from aspire.basis import FBBasis3D
from aspire.operators import RadialCTFFilter
from aspire.reconstruction import MeanEstimator
from aspire.source.simulation import Simulation

DATA_DIR = os.path.join(os.path.dirname(__file__), "saved_test_data")


class MeanEstimatorTestCase(TestCase):
    def setUp(self):
        self.dtype = np.float32
        self.resolution = 8

        self.sim = sim = Simulation(
            n=1024,
            unique_filters=[
                RadialCTFFilter(defocus=d) for d in np.linspace(1.5e4, 2.5e4, 7)
            ],
            dtype=self.dtype,
        )
        basis = FBBasis3D((self.resolution,) * 3, dtype=self.dtype)

        self.estimator = MeanEstimator(sim, basis, preconditioner="none")

        self.estimator_with_preconditioner = MeanEstimator(
            sim, basis, preconditioner="circulant"
        )

    def tearDown(self):
        pass

    def testEstimateResolutionError(self):
        """
        Test mismatched resolutions yields a relevant error message.
        """

        with raises(ValueError, match=r".*resolution.*"):
            # This basis is intentionally the wrong resolution.
            incorrect_basis = FBBasis3D((2 * self.resolution,) * 3, dtype=self.dtype)

            _ = MeanEstimator(self.sim, incorrect_basis, preconditioner="none")

    def testEstimate(self):
        estimate = self.estimator.estimate()
        self.assertTrue(
            np.allclose(
                estimate[0][:, :, 4],
                [
                    [
                        +0.00000000,
                        +0.00000000,
                        +0.00000000,
                        +0.00000000,
                        -0.00000000,
                        +0.00000000,
                        +0.00000000,
                        +0.00000000,
                    ],
                    [
                        +0.00000000,
                        +0.00000000,
                        +0.02446793,
                        +0.05363505,
                        +0.21988572,
                        +0.19513786,
                        +0.01174418,
                        +0.00000000,
                    ],
                    [
                        +0.00000000,
                        -0.06168774,
                        +0.13178457,
                        +0.36011154,
                        +0.88632372,
                        +0.92307694,
                        +0.45524491,
                        +0.15142541,
                    ],
                    [
                        +0.00000000,
                        -0.09108749,
                        +0.19564009,
                        +0.78325885,
                        +2.34527692,
                        +2.44817345,
                        +1.41268619,
                        +0.53634876,
                    ],
                    [
                        +0.00000000,
                        +0.07150180,
                        +0.38347393,
                        +1.70868980,
                        +3.78134981,
                        +3.03582139,
                        +1.49942724,
                        +0.52104809,
                    ],
                    [
                        +0.00000000,
                        +0.00736866,
                        +0.19239950,
                        +1.71596036,
                        +3.59823119,
                        +2.64081679,
                        +1.08514933,
                        +0.24995637,
                    ],
                    [
                        +0.00000000,
                        +0.11075829,
                        +0.43197553,
                        +0.82667320,
                        +1.51163241,
                        +1.25342639,
                        +0.36478594,
                        -0.00464912,
                    ],
                    [
                        +0.00000000,
                        +0.00000000,
                        +0.43422818,
                        +0.64440739,
                        +0.44137408,
                        +0.25311494,
                        +0.00011242,
                        +0.00000000,
                    ],
                ],
                atol=1e-5,
            )
        )

    def testAdjoint(self):
        mean_b_coeff = self.estimator.src_backward().squeeze()
        self.assertTrue(
            np.allclose(
                mean_b_coeff,
                [
                    1.07338590e-01,
                    1.23690941e-01,
                    6.44482039e-03,
                    -5.40484306e-02,
                    -4.85304586e-02,
                    1.09852144e-02,
                    3.87838396e-02,
                    3.43796455e-02,
                    -6.43284705e-03,
                    -2.86677145e-02,
                    -1.42313328e-02,
                    -2.25684091e-03,
                    -3.31840727e-02,
                    -2.59706174e-03,
                    -5.91919887e-04,
                    -9.97433028e-03,
                    9.19123928e-04,
                    1.19891589e-03,
                    7.49154982e-03,
                    6.18865229e-03,
                    -8.13265715e-04,
                    -1.30715655e-02,
                    -1.44160603e-02,
                    2.90379956e-03,
                    2.37066082e-02,
                    4.88805735e-03,
                    1.47870707e-03,
                    7.63376018e-03,
                    -5.60619559e-03,
                    1.05165081e-02,
                    3.30510143e-03,
                    -3.48652120e-03,
                    -4.23228797e-04,
                    1.40484061e-02,
                    1.42914291e-03,
                    -1.28129504e-02,
                    2.19868825e-03,
                    -6.30835037e-03,
                    1.18524223e-03,
                    -2.97855052e-02,
                    1.15491057e-03,
                    -8.27947006e-03,
                    3.45442781e-03,
                    -4.72868856e-03,
                    2.66615329e-03,
                    -7.87929790e-03,
                    8.84126590e-04,
                    1.59402808e-03,
                    -9.06854048e-05,
                    -8.79119004e-03,
                    1.76449039e-03,
                    -1.36414673e-02,
                    1.56793855e-03,
                    1.44708445e-02,
                    -2.55974802e-03,
                    5.38506357e-03,
                    -3.24188673e-03,
                    4.81582945e-04,
                    7.74260101e-05,
                    5.48772082e-03,
                    1.92058500e-03,
                    -4.63538896e-03,
                    -2.02735133e-03,
                    3.67592386e-03,
                    7.23486969e-04,
                    1.81838422e-03,
                    1.78793284e-03,
                    -8.01474060e-03,
                    -8.54007528e-03,
                    1.96353845e-03,
                    -2.16254252e-03,
                    -3.64243996e-05,
                    -2.27329863e-03,
                    1.11424393e-03,
                    -1.39389189e-03,
                    2.57787159e-04,
                    3.66918811e-03,
                    1.31477774e-03,
                    6.82220128e-04,
                    1.41822851e-03,
                    -1.89476924e-03,
                    -6.43966255e-05,
                    -7.87888465e-04,
                    -6.99459279e-04,
                    1.08918981e-03,
                    2.25264584e-03,
                    -1.43651015e-04,
                    7.68377620e-04,
                    5.05955256e-04,
                    2.66936132e-06,
                    2.24934884e-03,
                    6.70529439e-04,
                    4.81121742e-04,
                    -6.40789745e-05,
                    -3.35915672e-04,
                    -7.98651783e-04,
                    -9.82705453e-04,
                    6.46337066e-05,
                ],
                atol=1e-6,
            )
        )

    def testOptimize1(self):
        mean_b_coeff = np.array(
            [
                1.07338590e-01,
                1.23690941e-01,
                6.44482039e-03,
                -5.40484306e-02,
                -4.85304586e-02,
                1.09852144e-02,
                3.87838396e-02,
                3.43796455e-02,
                -6.43284705e-03,
                -2.86677145e-02,
                -1.42313328e-02,
                -2.25684091e-03,
                -3.31840727e-02,
                -2.59706174e-03,
                -5.91919887e-04,
                -9.97433028e-03,
                9.19123928e-04,
                1.19891589e-03,
                7.49154982e-03,
                6.18865229e-03,
                -8.13265715e-04,
                -1.30715655e-02,
                -1.44160603e-02,
                2.90379956e-03,
                2.37066082e-02,
                4.88805735e-03,
                1.47870707e-03,
                7.63376018e-03,
                -5.60619559e-03,
                1.05165081e-02,
                3.30510143e-03,
                -3.48652120e-03,
                -4.23228797e-04,
                1.40484061e-02,
                1.42914291e-03,
                -1.28129504e-02,
                2.19868825e-03,
                -6.30835037e-03,
                1.18524223e-03,
                -2.97855052e-02,
                1.15491057e-03,
                -8.27947006e-03,
                3.45442781e-03,
                -4.72868856e-03,
                2.66615329e-03,
                -7.87929790e-03,
                8.84126590e-04,
                1.59402808e-03,
                -9.06854048e-05,
                -8.79119004e-03,
                1.76449039e-03,
                -1.36414673e-02,
                1.56793855e-03,
                1.44708445e-02,
                -2.55974802e-03,
                5.38506357e-03,
                -3.24188673e-03,
                4.81582945e-04,
                7.74260101e-05,
                5.48772082e-03,
                1.92058500e-03,
                -4.63538896e-03,
                -2.02735133e-03,
                3.67592386e-03,
                7.23486969e-04,
                1.81838422e-03,
                1.78793284e-03,
                -8.01474060e-03,
                -8.54007528e-03,
                1.96353845e-03,
                -2.16254252e-03,
                -3.64243996e-05,
                -2.27329863e-03,
                1.11424393e-03,
                -1.39389189e-03,
                2.57787159e-04,
                3.66918811e-03,
                1.31477774e-03,
                6.82220128e-04,
                1.41822851e-03,
                -1.89476924e-03,
                -6.43966255e-05,
                -7.87888465e-04,
                -6.99459279e-04,
                1.08918981e-03,
                2.25264584e-03,
                -1.43651015e-04,
                7.68377620e-04,
                5.05955256e-04,
                2.66936132e-06,
                2.24934884e-03,
                6.70529439e-04,
                4.81121742e-04,
                -6.40789745e-05,
                -3.35915672e-04,
                -7.98651783e-04,
                -9.82705453e-04,
                6.46337066e-05,
            ]
        )

        x = self.estimator.conj_grad(mean_b_coeff)
        self.assertTrue(
            np.allclose(
                x,
                [
                    1.24325149e01,
                    4.06481998e00,
                    1.19149607e00,
                    -3.31414200e00,
                    -1.23897783e00,
                    1.53987018e-01,
                    2.50221093e00,
                    9.18131863e-01,
                    4.09624945e-02,
                    -1.81129255e00,
                    -2.58832135e-01,
                    -7.21149988e-01,
                    -1.00909836e00,
                    5.72232366e-02,
                    -3.90701966e-01,
                    -3.65655187e-01,
                    2.33601017e-01,
                    1.75039197e-01,
                    2.52945224e-01,
                    3.29783105e-01,
                    7.85601834e-02,
                    -3.96439884e-01,
                    -8.56255814e-01,
                    7.35131473e-03,
                    1.10704423e00,
                    7.35615877e-02,
                    5.61772211e-01,
                    2.60428522e-01,
                    -5.41932165e-01,
                    4.29851425e-01,
                    3.86300956e-01,
                    -8.90168838e-02,
                    -1.02959264e-01,
                    6.03104058e-01,
                    1.85286462e-01,
                    -4.16434930e-01,
                    2.11092135e-01,
                    -1.85514653e-01,
                    9.80712710e-02,
                    -8.98429489e-01,
                    -9.54759574e-02,
                    -1.17952459e-01,
                    1.41721715e-01,
                    -1.36184702e-01,
                    3.23733962e-01,
                    -2.68721792e-01,
                    -1.42064052e-01,
                    1.41909797e-01,
                    -2.24251300e-03,
                    -4.27538724e-01,
                    1.28441757e-01,
                    -5.57623000e-01,
                    -1.54801935e-01,
                    6.51729903e-01,
                    -2.15567768e-01,
                    1.95041528e-01,
                    -4.18334680e-01,
                    3.26735913e-02,
                    6.35474331e-02,
                    3.06828631e-01,
                    1.43149180e-01,
                    -2.34377520e-01,
                    -1.54299735e-01,
                    2.82627560e-01,
                    9.60630473e-02,
                    1.47687304e-01,
                    1.38157247e-01,
                    -4.25581692e-01,
                    -5.62236939e-01,
                    2.09287213e-01,
                    -1.14280315e-01,
                    2.70617650e-02,
                    -1.19705716e-01,
                    1.68350236e-02,
                    -1.20459065e-01,
                    6.03971532e-02,
                    3.21465643e-01,
                    1.82032297e-01,
                    -2.95991444e-02,
                    1.53711400e-01,
                    -1.30594319e-01,
                    -4.71412485e-02,
                    -1.35301477e-01,
                    -2.36292616e-01,
                    1.95728111e-01,
                    2.54618329e-01,
                    -1.81663289e-03,
                    2.77960420e-02,
                    3.58816749e-02,
                    -2.50138365e-02,
                    2.54103161e-01,
                    9.82534014e-02,
                    9.00807559e-02,
                    3.71458771e-02,
                    -7.86838200e-02,
                    -1.03837231e-01,
                    -1.26116949e-01,
                    9.82006976e-02,
                ],
                atol=1e-4,
            )
        )

    def testOptimize2(self):
        mean_b_coeff = np.array(
            [
                1.07338590e-01,
                1.23690941e-01,
                6.44482039e-03,
                -5.40484306e-02,
                -4.85304586e-02,
                1.09852144e-02,
                3.87838396e-02,
                3.43796455e-02,
                -6.43284705e-03,
                -2.86677145e-02,
                -1.42313328e-02,
                -2.25684091e-03,
                -3.31840727e-02,
                -2.59706174e-03,
                -5.91919887e-04,
                -9.97433028e-03,
                9.19123928e-04,
                1.19891589e-03,
                7.49154982e-03,
                6.18865229e-03,
                -8.13265715e-04,
                -1.30715655e-02,
                -1.44160603e-02,
                2.90379956e-03,
                2.37066082e-02,
                4.88805735e-03,
                1.47870707e-03,
                7.63376018e-03,
                -5.60619559e-03,
                1.05165081e-02,
                3.30510143e-03,
                -3.48652120e-03,
                -4.23228797e-04,
                1.40484061e-02,
                1.42914291e-03,
                -1.28129504e-02,
                2.19868825e-03,
                -6.30835037e-03,
                1.18524223e-03,
                -2.97855052e-02,
                1.15491057e-03,
                -8.27947006e-03,
                3.45442781e-03,
                -4.72868856e-03,
                2.66615329e-03,
                -7.87929790e-03,
                8.84126590e-04,
                1.59402808e-03,
                -9.06854048e-05,
                -8.79119004e-03,
                1.76449039e-03,
                -1.36414673e-02,
                1.56793855e-03,
                1.44708445e-02,
                -2.55974802e-03,
                5.38506357e-03,
                -3.24188673e-03,
                4.81582945e-04,
                7.74260101e-05,
                5.48772082e-03,
                1.92058500e-03,
                -4.63538896e-03,
                -2.02735133e-03,
                3.67592386e-03,
                7.23486969e-04,
                1.81838422e-03,
                1.78793284e-03,
                -8.01474060e-03,
                -8.54007528e-03,
                1.96353845e-03,
                -2.16254252e-03,
                -3.64243996e-05,
                -2.27329863e-03,
                1.11424393e-03,
                -1.39389189e-03,
                2.57787159e-04,
                3.66918811e-03,
                1.31477774e-03,
                6.82220128e-04,
                1.41822851e-03,
                -1.89476924e-03,
                -6.43966255e-05,
                -7.87888465e-04,
                -6.99459279e-04,
                1.08918981e-03,
                2.25264584e-03,
                -1.43651015e-04,
                7.68377620e-04,
                5.05955256e-04,
                2.66936132e-06,
                2.24934884e-03,
                6.70529439e-04,
                4.81121742e-04,
                -6.40789745e-05,
                -3.35915672e-04,
                -7.98651783e-04,
                -9.82705453e-04,
                6.46337066e-05,
            ]
        )

        x = self.estimator_with_preconditioner.conj_grad(mean_b_coeff)
        self.assertTrue(
            np.allclose(
                x,
                [
                    1.24325149e01,
                    4.06481998e00,
                    1.19149607e00,
                    -3.31414200e00,
                    -1.23897783e00,
                    1.53987018e-01,
                    2.50221093e00,
                    9.18131863e-01,
                    4.09624945e-02,
                    -1.81129255e00,
                    -2.58832135e-01,
                    -7.21149988e-01,
                    -1.00909836e00,
                    5.72232366e-02,
                    -3.90701966e-01,
                    -3.65655187e-01,
                    2.33601017e-01,
                    1.75039197e-01,
                    2.52945224e-01,
                    3.29783105e-01,
                    7.85601834e-02,
                    -3.96439884e-01,
                    -8.56255814e-01,
                    7.35131473e-03,
                    1.10704423e00,
                    7.35615877e-02,
                    5.61772211e-01,
                    2.60428522e-01,
                    -5.41932165e-01,
                    4.29851425e-01,
                    3.86300956e-01,
                    -8.90168838e-02,
                    -1.02959264e-01,
                    6.03104058e-01,
                    1.85286462e-01,
                    -4.16434930e-01,
                    2.11092135e-01,
                    -1.85514653e-01,
                    9.80712710e-02,
                    -8.98429489e-01,
                    -9.54759574e-02,
                    -1.17952459e-01,
                    1.41721715e-01,
                    -1.36184702e-01,
                    3.23733962e-01,
                    -2.68721792e-01,
                    -1.42064052e-01,
                    1.41909797e-01,
                    -2.24251300e-03,
                    -4.27538724e-01,
                    1.28441757e-01,
                    -5.57623000e-01,
                    -1.54801935e-01,
                    6.51729903e-01,
                    -2.15567768e-01,
                    1.95041528e-01,
                    -4.18334680e-01,
                    3.26735913e-02,
                    6.35474331e-02,
                    3.06828631e-01,
                    1.43149180e-01,
                    -2.34377520e-01,
                    -1.54299735e-01,
                    2.82627560e-01,
                    9.60630473e-02,
                    1.47687304e-01,
                    1.38157247e-01,
                    -4.25581692e-01,
                    -5.62236939e-01,
                    2.09287213e-01,
                    -1.14280315e-01,
                    2.70617650e-02,
                    -1.19705716e-01,
                    1.68350236e-02,
                    -1.20459065e-01,
                    6.03971532e-02,
                    3.21465643e-01,
                    1.82032297e-01,
                    -2.95991444e-02,
                    1.53711400e-01,
                    -1.30594319e-01,
                    -4.71412485e-02,
                    -1.35301477e-01,
                    -2.36292616e-01,
                    1.95728111e-01,
                    2.54618329e-01,
                    -1.81663289e-03,
                    2.77960420e-02,
                    3.58816749e-02,
                    -2.50138365e-02,
                    2.54103161e-01,
                    9.82534014e-02,
                    9.00807559e-02,
                    3.71458771e-02,
                    -7.86838200e-02,
                    -1.03837231e-01,
                    -1.26116949e-01,
                    9.82006976e-02,
                ],
                atol=1e-4,
            )
        )
