import os

def load_file(filepath):
    """Utility to load content from a file."""

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()


def build_prompt(article_text, keywords, links, images, brand_rules):
    """
    Build a well-structured prompt for the LLM.

    Parameters:
    - article_text (str): Original article markdown
    - keywords (List[str]): Keywords from the txt file
    - links (List[Dict]): Matching links from DB
    - images (List[Dict]): Matching images from DB
    - brand_rules (str): Style/tone/branding instructions

    Returns:
    - str: The final prompt to send to OpenRouter
    """
 
    link_instructions = "\n".join([
    f"- Insert a Markdown link for the keyword: '{link['keyword']}', using this URL: {link['url']}"
    for link in links
    ]) if links else "No internal links to insert."

    image_instructions = "\n".join([
        f"- For keyword '{img['keyword']}', insert this image URL near relevant content: {img['url']} (add descriptive alt-text)"
        for img in images
    ]) if images else "No images to insert."

    prompt = f"""
You are a content editor AI.

Your job is to:
1. Embed exactly **two** relevant internal links using the URLs provided below.
    - Use the most relevant keywords as anchor text (or short variations).
    - Place links inline within the article text (do not put both at the end).
    - Use natural phrasing that fits context.
2. Insert two images from the list:
    - One near the top (hero)
    - One elsewhere in the body (in-context)
3. Follow brand guidelines strictly.

If you cannot insert exactly two links and two images, **do not proceed. Instead, return an error stating what’s missing.**
### EXAMPLE:
    Given keyword: "carbon capture technology"

    Insert like:  
    "According to the [IEA's carbon capture roadmap](https://example.com/ccs-roadmap)..."

## BRAND RULES:
{brand_rules}

## KEYWORDS TO CONSIDER:
{', '.join(keywords)}

## LINK INSTRUCTIONS:
{link_instructions}

## IMAGE INSTRUCTIONS:
{image_instructions}

---

Now, here's the markdown content you need to edit:

{article_text}

Return the updated markdown only — no explanations or extra text.
"""
    return prompt
