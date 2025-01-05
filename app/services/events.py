import logging

from app import JOB_QUEUE
from app.services.broker import EventService
from app.services.resume_score import ResumeScoreService
from app.types.communications import EventType, RPCPayloadType


class EventsService:
    @staticmethod
    async def handle_event(event):
        if not event.get("type"):
            return

        logging.info(f"Received event: {event.get('type')}")

        if event["type"] == EventType.GENERATE_RESUME_SCORE:
            if (
                not event.get("data")
                # ID to be used for tracking the event
                or not event["data"].get("id")
                or not event["data"].get("job_description")
                or not event["data"].get("resume")
            ):
                return

            job_description = event["data"]["job_description"]
            resume = event["data"]["resume"]

            score = ResumeScoreService.get_score(job_description, resume)

            await EventService.publish(
                JOB_QUEUE,
                EventService.build_request_payload(
                    type=EventType.RESUME_SCORED,
                    data={
                        "id": event["data"]["id"],
                        "score": score.score,
                        "explanation": score.explanation or "",
                    },
                ),
            )

    @staticmethod
    async def respond_rpc(message):
        if not message.get("type"):
            return

        logging.info(f"Received RPC: {message.get('type')}")

        if message["type"] == RPCPayloadType.GET_RESUME_SCORE:
            if (
                not message.get("data")
                or not message["data"].get("job_description")
                or not message["data"].get("resume")
            ):
                return {"error": "job_description and resume are required"}

            job_description = message["data"]["job_description"]
            resume = message["data"]["resume"]

            score = ResumeScoreService.get_score(job_description, resume)
            return {
                "score": score.score,
                "explanation": score.explanation or "",
            }

        return {"data": "Responding to RPC"}
