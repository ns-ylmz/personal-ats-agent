"""
Shared prompts and prompt builder functions for LLM providers.
"""

CLEAN_RAW_JOB_TEXT_TEMPLATE = """
You are an expert recruiter. The following text is scraped from a job board website.
It contains a lot of noise (footers, similar jobs, cookie policies, company boilerplate, etc.).

Your task is to extract ONLY the relevant information about the job itself:
- Job Title and Location
- Job Definition / Role Summary
- Key Responsibilities
- Requirements / Qualifications
- Cultural Fit / Perks (if highly relevant)

Do NOT include:
- "Similar Jobs" or "People also viewed"
- Website navigation menus, footers, or legal boilerplate
- Irrelevant company marketing fluff

Return the cleaned text formatted clearly. Do not use JSON, just return plain readable text.

Raw Text:
{raw_text}
""".strip()


def get_clean_raw_job_text_prompt(raw_text: str) -> str:
    """Returns the prompt to clean raw scraped job text."""
    return CLEAN_RAW_JOB_TEXT_TEMPLATE.format(raw_text=raw_text)


def get_analyze_job_prompt(
    cv_text: str,
    job_description: str,
    past_feedback: str = "",
    include_role_preamble: bool = False,
    include_suffix_instructions: bool = False,
) -> str:
    """Builds the prompt for analyzing a CV against a job description."""
    feedback_section = ""
    if past_feedback:
        feedback_section = f"""
Past Interview Feedback Context:
Focus on addressing these past interview weaknesses and areas of improvement when generating prep questions.
{past_feedback}
"""

    preamble = "You are an expert ATS (Applicant Tracking System) and career coach.\n" if include_role_preamble else ""
    suffix = "\nPlease provide the match score, a cover letter, and prep questions." if include_suffix_instructions else ""

    return f"""
{preamble}Analyze the following CV against the given job description.

{feedback_section}

CV:
{cv_text}

Job Description:
{job_description}{suffix}
""".strip()


def get_extract_master_profile_prompt(cv_text: str, include_suffix_instructions: bool = False) -> str:
    """Builds the prompt for extracting a master profile from CV text."""
    suffix = "\nPlease provide the skills and experience summary." if include_suffix_instructions else ""
    return f"""
Extract the core professional profile from the following CV.

CV:
{cv_text}{suffix}
""".strip()


# System prompts (used by OpenAI or chat-based LLM APIs)
OPENAI_ATS_SYSTEM_PROMPT = "You are an expert ATS and career coach. Please output JSON according to the schema."
OPENAI_PROFILE_SYSTEM_PROMPT = "You are an expert recruiter parsing a CV into a structured master profile."
OPENAI_CLEAN_TEXT_SYSTEM_PROMPT = "You are an expert recruiter cleaning up scraped HTML text."
