import re


def test_monte_carlo_parallel_progress(monte_carlo_calisto, capsys):
    """Ensure progress messages are printed when running in parallel."""
    monte_carlo_calisto.simulate(2, parallel=True, n_workers=2)
    captured = capsys.readouterr()
    out = captured.out.replace('\r', '\n')
    # There should be progress lines and a final status line
    assert out.count("Current iteration") >= 1
    assert "Completed" in out
