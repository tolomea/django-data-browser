import pytest

from data_browser.common import get_optimal_decimal_places


@pytest.mark.parametrize(
    "numbers,decimal_places",
    [
        ([], 0),
        ([1e100], 0),
        ([0.1], 1),
        ([1.37], 2),
        ([13.37], 2),
        ([0.12345], 3),
        ([0.00001], 6),
        ([1e100, 0.1], 1),
        ([1e100, 1.37], 2),
        ([1e100, 13.37], 2),
        ([1e100, 0.12345], 3),
        ([1e100, 0.00001], 6),
        ([0.1, 1.37], 2),
        ([0.1, 13.37], 2),
        ([0.1, 0.12345], 3),
        ([0.1, 0.00001], 6),
        ([1.37, 13.37], 2),
        ([1.37, 0.12345], 3),
        ([1.37, 0.00001], 6),
        ([13.37, 0.12345], 3),
        ([13.37, 0.00001], 6),
        ([0.12345, 0.00001], 6),
        ([1.0], 0),
        ([None], 0),
        ([0], 0),
    ],
)
def test_optimal_decimal_places(numbers, decimal_places):
    assert get_optimal_decimal_places(numbers) == decimal_places
