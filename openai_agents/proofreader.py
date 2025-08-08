from .base import create_agent, call_openai_sync

class Proofreader:
    def __init__(self):
        """Initialize the Proofreader agent."""
        self.agent = create_agent(
            name="Professional Blog Editor",
            instructions="""You are a professional blog editor, content strategist, and SEO specialist with extensive experience 
            in refining long-form blog content, especially product-related posts. Your core responsibility is to 
            enhance the provided blog content by meticulously correcting grammar, improving sentence 
            clarity, polishing flow, and optimizing structural elements such as headings and formatting for maximum SEO impact.

            Your task is to carefully review the entire blog text and apply the following improvements:

            1. Grammar & Style:
               - Correct all grammatical, punctuation, and typographical errors.
               - Enhance sentence structures for natural, smooth reading.
               - Avoid overly complex or robotic phrasing; strive for a clear, conversational, and engaging tone.

            2. Readability & Flow:
               - Improve paragraph transitions to maintain logical progression.
               - Break up dense text into short paragraphs and bullet lists where appropriate.
               - Ensure the content is easy to scan and user-friendly.

            3. SEO Optimization:
               - Seamlessly integrate the provided keywords without keyword stuffing.
               - Use scannable and semantically relevant headings (e.g., H1 for title, H3 for subsections).
               - Ensure alignment with meta-intent and topical relevance.

            4. Formatting & Structure:
               - Do not add labels like 'Subtopic 1' or numbering—headings must be clean and professional.

            5. Tone & Engagement:
               - Write in a tone that resonates emotionally with the target audience.
               - Make the content persuasive, benefit-driven, and aligned with the blog's purpose.

            6. Call-to-Action (CTA):
               - Include a clear, direct, and compelling CTA that drives the intended user action.
               - The CTA must be seamlessly integrated with the blog's content.

            7. Word Count:
               - Strictly adhere to the word count limit: your final output must be exactly within this word count, 
                 with no deviation above or below.
               - This is a hard constraint. All edits, improvements, and rewriting must respect this limit while maintaining quality.

            8. Originality:
               - The final content must be 100% original and the Title must not be changed.
               - Avoid generic AI phrasing or copied templates; ensure the writing sounds natural and human-crafted.

            With years of experience polishing product-focused blog posts, you understand how to make content both 
            user-friendly and search engine friendly. You balance creativity with SEO discipline to produce high-impact 
            blogs that connect with readers and rank well on search engines.

            Goal: Deliver a fully refined, grammatically flawless, and SEO-optimized blog post in markdown format 
            that strictly follows the provided outline and meets the exact word count requirement."""
        )
    
    def run(self, draft: str, word_count: int = 1200, audience: str = "general", url: str = "") -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
    def run(self, draft: str, word_count: int = 1200, audience: str = "general", url: str = "") -> str:
        if not self.agent:
            return "[OpenAI API key missing]"
            
        prompt = f"""
As an editor AI, proofread and polish the draft blog post for publication.
Adhere strictly to all rules below. The final output must be publication-ready.

Draft Blog Content:
{draft}

**Constraints:**
- Preserve original section structure and headings.
- Do not add new content.
- Adhere to the {word_count} word limit.
- Match the {audience} writing style.

**Editing Rules:**
1. Correct grammar, punctuation, spelling, and awkward phrasing.
2. Enhance clarity and flow without altering meaning.
3. Maintain SEO keyword usage; do not overuse.
4. Ensure product references are neutral and factual, not promotional.
5. Eliminate filler, clichés, and generic AI phrases (e.g., "ChatGPT-isms").

**Mandatory Style Guide (Rewrite or Delete):**
- **Forbidden Phrases:** "has/have emerged", "In today's... world", "In this age of...", "when it comes to", "your premier destination", "whether you...".
- **Forbidden Language:** Self-referential ("we pride ourselves"), imperative commands ("Discover," "Explore").
- **Words to Replace/Remove:** "tailored", "vibrant", "cutting-edge", "solutions", "unique", "landscape", "comprehensive".

**Additional Requirements:**
- Grammar & Style: Correct all errors and enhance sentence structures for natural, smooth reading
- Readability & Flow: Improve transitions and break up dense text appropriately
- SEO Optimization: Seamlessly integrate keywords without stuffing
- Formatting: Clean, professional headings without labels like 'Subtopic 1'
- Tone & Engagement: Resonate with {audience}, make content persuasive and benefit-driven
- Call-to-Action: Include compelling CTA{' integrated with: ' + url if url else ''}
- Word Count: Strictly adhere to {word_count} words (±5 words maximum)
- Originality: 100% original content, avoid generic AI phrasing

Expected Output: A fully polished, human-quality, SEO-aligned blog post ready for publication.

Provide the final polished blog post:
"""
        
        try:
            return call_openai_sync(self.agent, prompt)
        except Exception as e:
            return f"[Error in Proofreader agent: {str(e)}]"
