import logging
import time

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

from app import GROQ_API_KEY, GROQ_MODEL, MODEL, USE_GROQ
from app.services.system_messages import resume_evaluation, resume_template
from app.types.resume_score import ResumeScore
from app.utils.pdf_text import fetch_pdf_text

_resume_score_request_parser = JsonOutputParser(pydantic_object=ResumeScore)

_resume_prompt = PromptTemplate(
    template=resume_template,
    input_variables=["job_description", "resume"],
    partial_variables={
        "system_prompt": resume_evaluation,
        "format_instructions": _resume_score_request_parser.get_format_instructions(),
    },
)

_llm = (
    ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.1,
    )
    if USE_GROQ
    else ChatOllama(model=MODEL)
)


class ResumeScoreService:
    @staticmethod
    async def __get_resume(resume: str) -> str:
        # See if the resume is a URL
        if not resume.startswith("http"):
            return resume

        logging.info(f"Fetching resume from URL: {resume}")

        # Fetch the resume from the URL
        return await fetch_pdf_text(resume)

    @staticmethod
    async def get_score(job_description: str, resume: str) -> ResumeScore:
        chain = _resume_prompt | _llm | _resume_score_request_parser

        resume = await ResumeScoreService.__get_resume(resume)

        explanation = None
        score = None
        nth_try = 0

        while score is None and nth_try <= 10:
            if nth_try > 0:
                time.sleep(2 ** (nth_try - 1))

            response = chain.invoke(
                {
                    "job_description": job_description,
                    "resume": resume,
                }
            )

            try:
                score = response.get("score")
                explanation = response.get("explanation")
                if not isinstance(score, (int, float)):
                    raise ValueError("Invalid score format.")
            except Exception as e:
                logging.error(f"Error parsing response on attempt {nth_try}: {e}")
                score = None

            nth_try += 1

        if score is None:
            raise Exception("Failed to get a valid score after 10 attempts")

        return ResumeScore(score=score, explanation=explanation)
