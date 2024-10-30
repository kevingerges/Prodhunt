
def format_output_as_markdown(results):
    # Header for the business plan
    md_output = "# Comprehensive Business Plan\n\n"

    for section, content in results.items():
        # Convert each section to a Markdown header
        md_output += f"## {section.replace('_', ' ').title()}\n\n"

        if "Error" in content or content == "No response generated.":
            md_output += f"**{content}**\n\n"
        elif isinstance(content, dict):  # If the content is structured
            for key, value in content.items():
                md_output += f"- **{key}**: {value}\n"
        else:
            md_output += f"{content}\n\n"

    return md_output
