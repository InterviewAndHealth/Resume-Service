import os

from dotenv import load_dotenv

load_dotenv(override=True)

# Server
ENV = os.getenv("ENV", "development")

# Model
MODEL = os.getenv("MODEL") or os.getenv("RESUME_SERVICE_MODEL")

# Groq settings
USE_GROQ = (
    os.getenv("USE_GROQ") or os.getenv("RESUME_SERVICE_USE_GROQ") or "false"
).lower() == "true"
GROQ_MODEL = os.getenv("GROQ_MODEL") or os.getenv("RESUME_SERVICE_GROQ_MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("RESUME_SERVICE_GROQ_API_KEY")

# RabbitMQ URL
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}",
)
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")

# RabbitMQ Service settings
SERVICE_QUEUE = os.getenv("RESUME_QUEUE", "RESUME_QUEUE")
RPC_QUEUE = os.getenv("RESUME_RPC", "RESUME_RPC")

USER_QUEUE = os.getenv("USER_QUEUE")
USER_RPC = os.getenv("USER_RPC")
INTERVIEW_QUEUE = os.getenv("INTERVIEW_QUEUE")
INTERVIEW_RPC = os.getenv("INTERVIEW_RPC")
SCHEDULER_QUEUE = os.getenv("SCHEDULER_QUEUE")
JOB_QUEUE = os.getenv("JOB_QUEUE")
JOB_RPC = os.getenv("JOB_RPC")


_imported_variable = {
    "RABBITMQ_URL": RABBITMQ_URL,
    "EXCHANGE_NAME": EXCHANGE_NAME,
}

if USE_GROQ:
    _imported_variable.update({"GROQ_API_KEY": GROQ_API_KEY, "GROQ_MODEL": GROQ_MODEL})
else:
    _imported_variable.update({"MODEL": MODEL})


if not all(_imported_variable.values()):
    missing_variables = [key for key, value in _imported_variable.items() if not value]
    raise ValueError(f"Missing environment variables: {missing_variables}")
