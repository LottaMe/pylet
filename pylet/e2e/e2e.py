import subprocess


def test_pylet():
    result = subprocess.run(['python', 'pylet', ''], capture_output=True, text=True, timeout=3)
    assert result.stderr == ''