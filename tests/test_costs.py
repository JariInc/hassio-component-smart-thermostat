"""Self-check for _get_pid_setpoint cost-offset behavior."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "custom_components", "smart_thermostat"))

import _ha_stubs  # noqa: F401  (registers homeassistant/simple_pid stubs)

from controllers import ClimatePidController


class Controller(ClimatePidController):
    def _is_on(self): return True


class FakeStates:
    def __init__(self, value): self._v = value
    def get(self, entity_id):
        return type("S", (), {"state": self._v})()


def make(cost_signal, scaling, cost_state):
    c = Controller("t", "heat", "climate.t", "1,0,0", None, False, None, None, None,
                   cost_signal=cost_signal, cost_scaling_factor=scaling)
    c._hass = type("H", (), {"states": FakeStates(cost_state)})()
    return c


# no cost config -> plain setpoint, offset None
c = make(None, 0.75, "0.5")
assert c._get_pid_setpoint(21.0) == 21.0 and c._cost_offset is None

# scaling None -> plain
c = make("sensor.cost", None, "0.5")
assert c._get_pid_setpoint(21.0) == 21.0 and c._cost_offset is None

# normal: 21 + 0.5*0.75
c = make("sensor.cost", 0.75, "0.5")
assert c._get_pid_setpoint(21.0) == 21.375
assert abs(c._cost_offset - 0.375) < 1e-9
assert abs(c._effective_setpoint - 21.375) < 1e-9

# non-numeric / unavailable state -> fallback
for bad in ["unavailable", "unknown", None]:
    c = make("sensor.cost", 0.75, bad)
    assert c._get_pid_setpoint(21.0) == 21.0 and c._cost_offset is None

# extra_state_attributes exposes cost_offset + effective_setpoint
c = make("sensor.cost", 0.75, "0.5")
c._current_pid_params = None
c._get_pid_setpoint(21.0)
attrs = c.extra_state_attributes
assert attrs["cost_offset"] == 0.375 and attrs["effective_setpoint"] == 21.375

# fallback omits cost_offset attr, effective_setpoint == climate target
c = make(None, 0.75, "0.5")
c._current_pid_params = None
c._get_pid_setpoint(21.0)
attrs = c.extra_state_attributes
assert "cost_offset" not in attrs and attrs["effective_setpoint"] == 21.0

print("cost offset tests OK")
