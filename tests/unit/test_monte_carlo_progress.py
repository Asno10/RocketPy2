from unittest.mock import patch

from rocketpy.simulation import MonteCarlo


def test_simulate_prints_progress_when_verbose(
    stochastic_environment, stochastic_calisto, stochastic_flight, tmp_path
):
    """MonteCarlo.simulate should report iteration progress when verbose."""

    monte_carlo = MonteCarlo(
        filename=tmp_path / "progress_test",
        environment=stochastic_environment,
        rocket=stochastic_calisto,
        flight=stochastic_flight,
    )

    with patch("builtins.print") as mocked_print, patch.object(
        MonteCarlo, "_MonteCarlo__run_single_simulation", return_value=None
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_inputs", return_value="{}\n"
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_outputs", return_value="{}\n"
    ):
        monte_carlo.simulate(
            number_of_simulations=3, append=False, parallel=False, verbose=True
        )

    assert any(
        "Iteration 000003/000003" in call.args[0]
        for call in mocked_print.call_args_list
    )


def test_simulate_no_progress_when_not_verbose(
    stochastic_environment, stochastic_calisto, stochastic_flight, tmp_path
):
    """MonteCarlo.simulate should be silent when verbose is False."""

    monte_carlo = MonteCarlo(
        filename=tmp_path / "progress_silent",
        environment=stochastic_environment,
        rocket=stochastic_calisto,
        flight=stochastic_flight,
    )

    with patch("builtins.print") as mocked_print, patch.object(
        MonteCarlo, "_MonteCarlo__run_single_simulation", return_value=None
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_inputs", return_value="{}\n"
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_outputs", return_value="{}\n"
    ):
        monte_carlo.simulate(
            number_of_simulations=3, append=False, parallel=False, verbose=False
        )

    assert mocked_print.call_count == 0


def test_simulate_prints_progress_parallel(
    stochastic_environment, stochastic_calisto, stochastic_flight, tmp_path
):
    """MonteCarlo.simulate should report progress when running in parallel."""

    monte_carlo = MonteCarlo(
        filename=tmp_path / "progress_parallel",
        environment=stochastic_environment,
        rocket=stochastic_calisto,
        flight=stochastic_flight,
    )

    import multiprocessing
    import multiprocessing.managers as mp_managers

    with patch("builtins.print") as mocked_print, patch.object(
        MonteCarlo, "_MonteCarlo__run_single_simulation", return_value=None
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_inputs", return_value="{}\n"
    ), patch.object(
        MonteCarlo, "_MonteCarlo__evaluate_flight_outputs", return_value="{}\n"
    ), patch(
        "rocketpy.simulation.monte_carlo._import_multiprocess",
        return_value=(multiprocessing, mp_managers),
    ):
        monte_carlo.simulate(
            number_of_simulations=3,
            append=False,
            parallel=True,
            n_workers=2,
            verbose=True,
        )

    assert any(
        "Iteration 000003/000003" in call.args[0]
        for call in mocked_print.call_args_list
    )

