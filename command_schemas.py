from jsonschema import Draft7Validator

COMMAND_SCHEMAS = {
    "OBSERVE_motion_sensor_1": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["OBSERVE"]},
            "target": {"type": "string", "enum": ["motion_sensor_1"]},
            "property": {"type": "string", "enum": ["motion_detected"]}
        },
        "required": ["action", "target", "property"],
        "additionalProperties": False
    },
    "ACTUATE_living_room_light_ON": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["ACTUATE"]},
            "target": {"type": "string", "enum": ["living_room_light"]},
            "property": {"type": "string", "enum": ["state"]},
            "value": {"type": "string", "enum": ["ON"]}
        },
        "required": ["action", "target", "property", "value"],
        "additionalProperties": False
    },
    "ACTUATE_living_room_light_OFF": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["ACTUATE"]},
            "target": {"type": "string", "enum": ["living_room_light"]},
            "property": {"type": "string", "enum": ["state"]},
            "value": {"type": "string", "enum": ["OFF"]}
        },
        "required": ["action", "target", "property", "value"],
        "additionalProperties": False
    },
    "OBSERVE_temperature_sensor_1": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["OBSERVE"]},
            "target": {"type": "string", "enum": ["temperature_sensor_1"]},
            "property": {"type": "string", "enum": ["current_temperature"]}
        },
        "required": ["action", "target", "property"],
        "additionalProperties": False
    },
    "OBSERVE_humidity_sensor_1": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["OBSERVE"]},
            "target": {"type": "string", "enum": ["humidity_sensor_1"]},
            "property": {"type": "string", "enum": ["current_humidity"]}
        },
        "required": ["action", "target", "property"],
        "additionalProperties": False
    }
}

VALIDATORS = {key: Draft7Validator(schema) for key, schema in COMMAND_SCHEMAS.items()}

def get_validator(command):
    """
    Returns the appropriate validator based on the command's action and target.
    """
    action = command.get("action")
    target = command.get("target")
    key = f"{action}_{target}"
    return VALIDATORS.get(key)
