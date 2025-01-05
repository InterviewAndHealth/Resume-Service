from enum import StrEnum


class EventType(StrEnum):
    GENERATE_RESUME_SCORE = "GENERATE_RESUME_SCORE"
    RESUME_SCORED = "RESUME_SCORED"


class RPCPayloadType(StrEnum):
    GET_RESUME_SCORE = "GET_RESUME_SCORE"
