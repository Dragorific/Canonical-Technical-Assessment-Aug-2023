event_schema = {
    "type": "object",
    "properties": {
        "event_type": {"type": "string"},
        "user_id": {"type": "string"},
        "variant_data": {"type": "object"},
    },
    "required": ["event_type", "user_id", "variant_data"],
}
