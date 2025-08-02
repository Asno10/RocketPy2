import numpy as np
import pytest

from rocketpy import Rocket, Flight


def test_drag_curve_with_altitude_array():
    data = np.array(
        [
            [0.0, 0.0, 0.3],
            [0.0, 1000.0, 0.2],
            [1.0, 0.0, 0.4],
            [1.0, 1000.0, 0.3],
        ]
    )
    rocket = Rocket(
        radius=0.05,
        mass=1.0,
        inertia=(1, 1, 1),
        power_off_drag=data,
        power_on_drag=data,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )
    assert rocket.power_off_drag.get_domain_dim() == 2
    assert rocket.power_off_drag.get_value_opt(1.0, 1000.0) == pytest.approx(0.3)


def test_u_dot_uses_altitude(example_plain_env):
    calls = {}

    def drag_func(mach, alt):
        calls["mach"] = mach
        calls["alt"] = alt
        return 0.5

    rocket = Rocket(
        radius=0.05,
        mass=1.0,
        inertia=(1, 1, 1),
        power_off_drag=drag_func,
        power_on_drag=drag_func,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )

    flight = Flight(
        rocket=rocket,
        environment=example_plain_env,
        rail_length=1,
        max_time=0.1,
        time_overshoot=False,
    )

    state = [0, 0, 1000.0, 100.0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    flight.u_dot(0, state)
    expected_mach = 100.0 / example_plain_env.speed_of_sound.get_value_opt(1000.0)
    assert calls["alt"] == 1000.0
    assert calls["mach"] == pytest.approx(expected_mach)

