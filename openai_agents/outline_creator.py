from .base import create_agent, call_openai_sync

class OutlineCreator:
    def __init__(self):
        """Initialize the OutlineCreator agent."""
        self.agent = create_agent(
            name="Blog Outline Creator",
            instructions="""You are an AI expert in generating SEO-optimized blog outlines for 2025.
            Your role is to create detailed, well-organized outlines for blog posts that incorporate research findings, 
            SEO keywords, trending angles, and product promotions in a natural way. You should generate structured 
            output that serves as an excellent blueprint for high-quality blog content with integrated FAQ sections 
            and product recommendations."""
        )
    
    def run(self, keywords: str, topic: str, research_summary: str, trend_summary: str, 
            audience: str = "", faq: str = "", product_name: str = "", product_url: str = "", 
            product_image_url: str = "", product_description_text: str = "", 
            product_price_min: str = "", product_price_max: str = "", 
            product_currency: str = "", language: str = "English") -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
You are an AI expert in generating SEO-optimized blog outlines for 2025.

Inputs:
- keywords: {keywords}
- topic: {topic}
- research_summary: {research_summary}
- trend_summary: {trend_summary}
- audience: {audience}
- faq: {faq}
- product_name: {product_name}
- product_url: {product_url}
- product_image_url: {product_image_url}
- product_description_text: {product_description_text}
- product_price_min: {product_price_min}
- product_price_max: {product_price_max}
- product_currency: {product_currency}

Your job:
1. Understand the main ideas from {trend_summary} and {research_summary}.
2. Create a compelling and SEO-optimized blog structure tailored to 2025 search trends.
3. Seamlessly incorporate the provided {keywords} into titles and subtopics to maximize organic visibility.

Task Instructions:
- Generate exactly 4 original, descriptive blog titles that directly reflect the ideas and structure of {trend_summary} and {research_summary} in {language} language.
- Ensure that all titles and subtopics are strictly unique and plagiarism-free.
- Under each title, provide exactly 3 relevant subtopics that clearly expand on the title, helping to structure the body of the blog.
- Each subtopic must be keyword-integrated and relevant to the target audience.
- All text must be plagiarism-free, human-like, and optimized for search engines in 2025.
- Include an FAQ section:
- Write exactly 3 to 5 clear and relevant FAQ questions and answers.
- Each FAQ question should be directly related to the blog's topic, aligned with the trend insights, and helpful to the {audience}.
- Each answer must provide concise, informative, and actionable information, designed for easy readability and SEO.
- Ensure a natural and engaging tone for the FAQs, matching the tone used in the rest of the outline.

product_title:
  - Promote {product_name} in context:
    - Write a dynamic, SEO-friendly paragraph that aligns with the blog topic and audience needs.
    - Blend the provided {product_description_text} naturally.
    - Emphasize value, relevance, and benefits.
    - MUST Include:
      - Price range: {product_price_min}–{product_price_max} {product_currency}
      - Product link: {product_url}
      - Image: ![Product Image]({product_image_url})

Return a Python list of dictionaries in the exact format:
[
  {{
    "title": "Blog Title",
    "subtopics": [
      "Subtopic 1 with keyword",
      "Subtopic 2 with keyword",
      "Subtopic 3 with keyword"
    ]
  }},
  ...
  {{
    "faq": [
      {{ "question": "Relevant question?", "answer": "Clear, actionable answer." }},
      ...
    ]
  }},
  {{
    "product_title": "{product_name}",
    "description": "Write a persuasive and SEO-optimized product blurb for {product_name}, based on the blog topic and target audience. Blend the provided product description ({product_description_text}) naturally into the paragraph. Highlight why {product_name} is a relevant and valuable recommendation. Include the price range ({product_price_min}–{product_price_max} {product_currency}), must include link to the product at {product_url}, and display the image: ![Product Image]({product_image_url})."
  }}
]

Output only the list. Do not include any extra text or formatting.
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in OutlineCreator agent: {str(e)}]"
