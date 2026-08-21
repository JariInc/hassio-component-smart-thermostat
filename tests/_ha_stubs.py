"""Minimal homeassistant stubs to import controllers for a value test."""
import sys, types
import datetime

ha = types.ModuleType("homeassistant")
ha.__path__ = []  # treat as package
ha.dt = types.ModuleType("homeassistant.util.dt")
ha._util = types.ModuleType("homeassistant.util")
ha.dt.now = lambda: datetime.datetime.now()
ha.core = types.ModuleType("homeassistant.core")
ha.core.HomeAssistant = object
ha.core.Context = object
ha.core.CALLBACK_TYPE = object
ha.core.State = type("State", (), {})
ha.core.DOMAIN = "homeassistant"
ha.core.split_entity_id = lambda e: tuple(e.split(".", 1))

helpers = types.ModuleType("homeassistant.helpers")
helpers.event = types.ModuleType("homeassistant.helpers.event")

cc = types.ModuleType("homeassistant.components")
cc.climate = types.ModuleType("homeassistant.components.climate")
cc.climate.DOMAIN = "climate"
cc.climate.HVACMode = type("HVACMode", (), {"COOL":"cool","HEAT":"heat"})
cc.climate.HVACAction = type("HVACAction", (), {"IDLE":"idle","OFF":"off"})
cc.climate.ATTR_HVAC_ACTION = "hvac_action"
cc.climate.ATTR_HVAC_MODE = "hvac_mode"
cc.climate.ATTR_MIN_TEMP = "min_temp"
cc.climate.ATTR_MAX_TEMP = "max_temp"
cc.climate.ATTR_TARGET_TEMP_STEP = "target_temp_step"
cc.climate.SERVICE_SET_HVAC_MODE = "set_hvac_mode"
cc.climate.SERVICE_SET_TEMPERATURE = "set_temperature"
cc.climate.SERVICE_TURN_OFF = "turn_off"
cc.climate.const = cc.climate

cc.input_number = types.ModuleType("homeassistant.components.input_number")
for n in ["ATTR_MIN","ATTR_MAX","SERVICE_SET_VALUE","ATTR_VALUE","ATTR_STEP"]:
    setattr(cc.input_number, n, n)

ha.const = types.ModuleType("homeassistant.const")
for n in ["STATE_OFF","STATE_ON","ATTR_ENTITY_ID","SERVICE_TURN_ON","SERVICE_TURN_OFF","ATTR_TEMPERATURE"]:
    setattr(ha.const, n, n)

helpers.condition = types.ModuleType("homeassistant.helpers.condition")
helpers.event.async_track_time_interval = lambda *a, **k: (lambda x: None)

ha.helpers = helpers
ha.components = cc
ha.exceptions = types.ModuleType("homeassistant.exceptions")
ha.exceptions.ConditionError = Exception

sys.modules["homeassistant"] = ha
sys.modules["homeassistant.util"] = ha._util
sys.modules["homeassistant.util.dt"] = ha.dt
sys.modules["homeassistant.dt"] = ha.dt
sys.modules["homeassistant.core"] = ha.core
sys.modules["homeassistant.helpers"] = helpers
sys.modules["homeassistant.helpers.event"] = helpers.event
sys.modules["homeassistant.helpers.condition"] = helpers.condition
sys.modules["homeassistant.const"] = ha.const
sys.modules["homeassistant.components"] = cc
sys.modules["homeassistant.components.climate"] = cc.climate
sys.modules["homeassistant.components.climate.const"] = cc.climate
sys.modules["homeassistant.components.input_number"] = cc.input_number
sys.modules["homeassistant.exceptions"] = ha.exceptions
sys.modules["homeassistant.core"] = ha.core

# simple_pid
pidmod = types.ModuleType("simple_pid")
class PID:
    def __init__(self, *a, **k): 
        self.setpoint=k.get("setpoint"); self.output_limits=k.get("output_limits")
    def set_auto_mode(self, **k): pass
pidmod.PID = PID
sys.modules["simple_pid"] = pidmod

import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
