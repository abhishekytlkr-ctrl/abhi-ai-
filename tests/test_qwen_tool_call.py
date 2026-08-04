import src.agent_tools  # noqa: F401
from src.tool_parsing import parse_tool_blocks, strip_tool_blocks


def test_qwen_tool_call_parsing_and_stripping():
    raw = """Sure, let me check your accounts.

<|tool_call_start|>[list_email_accounts()]<|tool_call_end|>"""

    blocks = parse_tool_blocks(raw, skip_fenced=True)

    assert len(blocks) == 1
    assert blocks[0].tool_type == "mcp__email__list_email_accounts"
    assert blocks[0].content == "{}"
    assert strip_tool_blocks(raw, skip_fenced=True) == "Sure, let me check your accounts."


def test_qwen_tool_call_with_args():
    raw = """Okay, fetching recent messages.
<|tool_call_start|>[list_emails(account="Gmail", unread_only=True, max_results=5)]<|tool_call_end|>"""

    blocks = parse_tool_blocks(raw, skip_fenced=True)

    assert len(blocks) == 1
    assert blocks[0].tool_type == "mcp__email__list_emails"
    assert "Gmail" in blocks[0].content
    
    cleaned = strip_tool_blocks(raw, skip_fenced=True)
    assert cleaned == "Okay, fetching recent messages."


def test_qwen_tool_call_positional_args():
    # Single positional argument
    raw = '<|tool_call_start|>[web_search("Sweden news")]<|tool_call_end|>'
    blocks = parse_tool_blocks(raw, skip_fenced=True)
    assert len(blocks) == 1
    assert blocks[0].tool_type == "web_search"
    assert "Sweden news" in blocks[0].content

    # Multiple positional arguments
    raw = '<|tool_call_start|>[read_file("src/main.py", 10, 50)]<|tool_call_end|>'
    blocks = parse_tool_blocks(raw, skip_fenced=True)
    assert len(blocks) == 1
    assert blocks[0].tool_type == "read_file"
    assert "src/main.py" in blocks[0].content
    assert "10" in blocks[0].content
    assert "50" in blocks[0].content


def test_qwen_tool_call_whitespace_before_end_tag():
    raw = "Okay.\n<|tool_call_start|>[web_search(query=\"Sweden news\")]\n<|tool_call_end|>"
    blocks = parse_tool_blocks(raw, skip_fenced=True)
    assert len(blocks) == 1
    assert blocks[0].tool_type == "web_search"
    
    cleaned = strip_tool_blocks(raw, skip_fenced=True)
    assert cleaned == "Okay."


def test_qwen_tool_call_regex_fallback_and_single_arg():
    # Regex fallback with unquoted values containing spaces
    raw = '<|tool_call_start|>[web_search(query=Sweden news today, time_filter=day)]<|tool_call_end|>'
    blocks = parse_tool_blocks(raw, skip_fenced=True)
    assert len(blocks) == 1
    assert blocks[0].tool_type == "web_search"
    assert "Sweden news today" in blocks[0].content
    assert "day" in blocks[0].content

    # Single argument fallback (syntax error, no keyword)
    raw = '<|tool_call_start|>[web_search(Sweden news today)]<|tool_call_end|>'
    blocks = parse_tool_blocks(raw, skip_fenced=True)
    assert len(blocks) == 1
    assert blocks[0].tool_type == "web_search"
    assert "Sweden news today" in blocks[0].content

