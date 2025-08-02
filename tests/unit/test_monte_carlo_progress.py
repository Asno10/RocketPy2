from unittest.mock import patch

from rocketpy.simulation import MonteCarlo


def test_simulate_prints_progress(
    stochastic_environment, stochastic_calisto, stochastic_flight, tmp_path
):
    """MonteCarlo.simulate should report iteration progress."""

    monte_carlo = MonteCarlo(
        filename=tmp_path / "progress_test",
        environment=stochastic_environment,
        rocket=stochastic_calisto,
        flight=stochastic_flight,
    )

    messages = []

    def fake_reprint(msg, end="\n", flush=True):  # pylint: disable=unused-argument
        messages.append(msg)

    with patch(
        "rocketpy.simulation.monte_carlo._SimMonitor.reprint",
        side_effect=fake_reprint,
    ), patch.object(
        MonteCarlo, "_MonteCarlo__run_single_simulation", return_value=None
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_inputs", return_value="{}\n"
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_outputs", return_value="{}\n"
    ):
        monte_carlo.simulate(number_of_simulations=3, append=False, parallel=False)

    assert any("Iteration 000003/000003" in msg for msg in messages)

