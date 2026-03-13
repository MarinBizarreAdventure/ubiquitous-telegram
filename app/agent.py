import json
import logging

import anthropic

from app.scraper import fetch_image_url, search_places
from app.weather import get_tomorrow_weather

logger = logging.getLogger(__name__)

TOOLS = [
    {
        "name": "get_weather",
        "description": "Get tomorrow's weather forecast for the user's city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name to get forecast for"},
            },
            "required": ["city"],
        },
    },
    {
        "name": "search_places",
        "description": "Search the internet for places matching the user's request in their city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City to search in"},
                "query": {"type": "string", "description": "What to search for, e.g. 'pool halls' or 'pizza restaurants'"},
            },
            "required": ["city", "query"],
        },
    },
]

SYSTEM_PROMPT = """You are a city guide assistant.
When a user tells you what they want to do, you:
1. Use get_weather to check tomorrow's forecast for their city
2. Use search_places to find venues matching their request
3. Suggest specific places to go and what to wear based on the weather

Be specific and practical. Name real places. For outfit advice, give concrete items (e.g. "jeans + light jacket + sneakers"), not vague descriptions."""


def _blocks_to_dicts(blocks: list) -> list[dict]:
    result = []
    for block in blocks:
        if block.type == "text":
            result.append({"type": "text", "text": block.text})
        elif block.type == "tool_use":
            result.append({"type": "tool_use", "id": block.id, "name": block.name, "input": block.input})
    return result


def run_agent(
    user_name: str,
    user_city: str,
    message: str,
    api_key: str,
    open_meteo_base_url: str,
) -> tuple[str, list[dict]]:
    client = anthropic.Anthropic(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": f"My name is {user_name} and I live in {user_city}. {message}",
        }
    ]

    logger.info("Agent started for user=%s city=%s", user_name, user_city)

    all_places: list[dict] = []
    reply_text = ""
    iteration = 0

    while True:
        iteration += 1
        logger.info("[iter %d] Calling Claude...", iteration)

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        logger.info("[iter %d] stop_reason=%s blocks=%s", iteration, response.stop_reason, [b.type for b in response.content])

        messages.append({"role": "assistant", "content": _blocks_to_dicts(response.content)})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    reply_text = block.text
                    logger.info("Agent finished. Response length=%d chars", len(reply_text))
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                logger.info("[iter %d] Tool call: %s(%s)", iteration, block.name, block.input)

                if block.name == "get_weather":
                    try:
                        result = get_tomorrow_weather(block.input["city"], open_meteo_base_url)
                        logger.info("[iter %d] Weather result: %s", iteration, result)
                    except Exception as e:
                        logger.error("[iter %d] Weather error: %s", iteration, e)
                        result = {"error": str(e)}

                elif block.name == "search_places":
                    try:
                        result = search_places(block.input["city"], block.input["query"])
                        logger.info("[iter %d] Scraper returned %d results", iteration, len(result))
                        for place in result:
                            if not any(p["name"] == place["name"] for p in all_places):
                                all_places.append(place)
                    except Exception as e:
                        logger.error("[iter %d] Scraper error: %s", iteration, e)
                        result = {"error": str(e)}

                else:
                    result = {"error": f"Unknown tool: {block.name}"}

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "user", "content": tool_results})
        else:
            logger.warning("[iter %d] Unexpected stop_reason=%s, breaking", iteration, response.stop_reason)
            for block in response.content:
                if hasattr(block, "text"):
                    reply_text = block.text
            break

    logger.info("Fetching images for %d places", len(all_places))
    for place in all_places:
        place["image_url"] = fetch_image_url(place["url"])

    return reply_text, all_places
