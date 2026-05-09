import json
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


STAT_KEYS = ("strength", "intelligence", "charisma")


def clamp(value, minimum=0.0, maximum=None):
    value = max(minimum, value)
    if maximum is not None:
        value = min(value, maximum)
    return value


def normalize_stats(stats, max_total):
    total = sum(stats.values())

    if total <= max_total or total == 0:
        return stats

    scale = max_total / total
    return {key: round(value * scale, 2) for key, value in stats.items()}


def parse_json_object(raw):
    if not raw:
        raise ValueError("AI returned an empty response")

    text = raw.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and start < end:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass

    raise ValueError(f"AI returned invalid JSON: {raw[:300]}")


def get_numeric_stat(data, key):
    try:
        return clamp(float(data.get(key, 0)))
    except (TypeError, ValueError):
        raise ValueError(f"AI returned an invalid value for {key}")


def get_boss_hp(value):
    try:
        return max(float(value), 1.0)
    except (TypeError, ValueError):
        return 100.0


def generate_task_rewards(task_title, boss_max_hp):
    """
    Generates balanced RPG stats for a task using OpenRouter AI.
    """
    task_title = task_title or "a normal productivity task"
    boss_hp = get_boss_hp(boss_max_hp)

    prompt = f"""
    You are balancing rewards for an RPG productivity app.

    Analyze this task:
    "{task_title}"

    Return ONLY valid JSON. Do not wrap it in markdown or add explanations.

    Format:
    {{
        "strength": number,
        "intelligence": number,
        "charisma": number
    }}

    Boss HP: {boss_hp}

    Rules:
    - Small daily tasks should have low rewards
    - Harder tasks should reward more
    - Strength = physical effort
    - Intelligence = mental effort
    - Charisma = social/confidence effort
    - Keep the boss hp in mind so that a typical user can kill a boss in ~5 days of consistent effort, but not in 1 day. Assume 1 point of stats = 1 damage to the boss.
    - Keep values realistic with each point representing a significant effort. You may give the values in floating points
    """

    completion = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON generator. Return one JSON object only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    raw = completion.choices[0].message.content
    data = parse_json_object(raw)

    if not isinstance(data, dict):
        raise ValueError("AI returned JSON, but it was not an object")

    stats = {key: get_numeric_stat(data, key) for key in STAT_KEYS}

    # Prevent a single task from deleting the boss. This still lets bigger
    # bosses receive bigger rewards without trusting the model blindly.
    stats = normalize_stats(stats, max_total=max(1.0, boss_hp * 0.2))

    total_stats = sum(stats.values())

    return {
        "stats": stats,
        "total_stats": round(total_stats, 2),
    }
