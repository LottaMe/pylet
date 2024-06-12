from unittest import mock

import pytest

from components import timeout


@timeout(1)
def sample_function():
    return


@mock.patch("components.ThreadPool")
def test_timout_within_timeout(mock_threadpool):
    mock_pool = mock_threadpool.return_value
    mock_async_result = mock_pool.apply_async.return_value
    mock_async_result.get.return_value = 5

    decorated_function = timeout(1)(sample_function)

    result = decorated_function()

    assert result == 5

    mock_pool.apply_async.assert_called_once_with(sample_function, (), {})
    mock_async_result.get.assert_called_once_with(1)


@mock.patch("components.ThreadPool")
def test_timout_exceeds_timeout(mock_threadpool):
    mock_pool = mock_threadpool.return_value
    mock_async_result = mock_pool.apply_async.return_value
    mock_async_result.get.side_effect = TimeoutError("Function call timed out")

    decorated_function = timeout(1)(sample_function)

    with pytest.raises(TimeoutError, match="Function call timed out"):
        decorated_function()

    mock_pool.apply_async.assert_called_once_with(sample_function, (), {})
    mock_async_result.get.assert_called_once_with(1)
