from utils.logger import Logger
import openai
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE_URL, OPENAI_MODEL

class ContentGenerator:
    def __init__(self):
        self.logger = Logger("ContentGenerator")
        self.chat_model = ChatOpenAI(
            model_name=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL
        )
        self.logger.info(f"Initializing ChatOpenAI model: {OPENAI_MODEL}")
        self.logger.info(f"Using API base URL: {OPENAI_API_BASE_URL if OPENAI_API_BASE_URL else 'default'}")
    
    def generate_survey(self, research_topic, paper_categories, papers, analysis_results):
        """
        Generate a complete literature survey
        
        Parameters:
        - research_topic: Research topic
        - paper_categories: Paper classification results
        - papers: List of papers
        - analysis_results: Paper analysis results
        
        Returns:
        - survey_data: Dictionary containing each section of the survey
        """
        self.logger.info(f"Starting to generate literature survey for topic '{research_topic}'")
        
        # Build RAG system
        from modules.rag_system import RAGSystem
        rag = RAGSystem()
        rag.add_documents(papers, analysis_results)
        
        # Generate title
        title = f"Research Survey on {research_topic}"
        
        # Generate abstract
        abstract_prompt = """
        Based on the provided research papers, generate a comprehensive and concise abstract that summarizes the main content, research status, key challenges, and future directions in this research field.
        The abstract should be between 300-500 words, using professional and objective language.
        Format the abstract in a style suitable for IEEE conference papers.
        DO NOT use any markdown formatting like # or * in your response.
        """
        abstract = rag.generate_section("Abstract", abstract_prompt, paper_categories)
        
        # Generate introduction
        introduction_prompt = """
        Write an academic introduction for this research topic, including:
        1. Research background and significance
        2. Brief introduction to the current research status
        3. Organization structure of this survey
        4. Research scope and objectives of the survey
        
        The introduction should explain why this field is important, the general situation of existing research, and how this survey will organize the content. The language should be professional, objective, and fluent.
        Format the introduction in a style suitable for IEEE conference papers, with proper paragraph structure and academic tone.
        DO NOT use any markdown formatting like # or * in your response.
        DO NOT use numbered lists with dots (like "1.") for paragraph numbering. Use proper IEEE-style paragraph organization.
        """
        introduction = rag.generate_section("Introduction", introduction_prompt, paper_categories)
        
        # Generate problem definition and basic concepts
        definition_prompt = """
        Provide clear problem definitions and explanations of basic concepts for this research field, including:
        1. Precise definition of the research problem
        2. Explanation of key terms and concepts
        3. Related mathematical notations and models (if applicable)
        4. Evaluation metrics and research hypotheses
        
        This section should provide readers with the basic knowledge needed to understand the field and clearly define the scope of research.
        Format the content in a style suitable for IEEE conference papers, with proper mathematical notation where appropriate.
        DO NOT use any markdown formatting like # or * in your response.
        DO NOT use numbered lists with dots (like "1.") for paragraph numbering. Use proper IEEE-style paragraph organization.
        """
        problem_definition = rag.generate_section("Problem Definition and Basic Concepts", definition_prompt, paper_categories)

        
        # Generate challenges and open problems
        challenges_prompt = """
        Analyze the main challenges and open problems facing this research field, including:
        1. Technical bottlenecks and unresolved difficulties
        2. Limitations of existing methods
        3. Challenges in data, resources, or evaluation
        4. Difficulties in practical applications
        
        Please specifically point out the manifestations and impacts of these challenges, as well as their constraints on research progress.
        Format the content in a style suitable for IEEE conference papers, with clear section organization and academic tone.
        DO NOT use any markdown formatting like # or * in your response.
        DO NOT use numbered lists with dots (like "1.") for paragraph numbering. Use proper IEEE-style paragraph organization.
        """
        challenges = rag.generate_section("Challenges and Open Problems", challenges_prompt, paper_categories)
        
        # Generate future research directions
        future_prompt = """
        Based on the current research status and challenges, predict future research directions in this field, including:
        1. Promising new technical approaches
        2. Worthwhile cross-disciplinary research areas
        3. Potential breakthrough points and innovation opportunities
        4. Potential development trends in industrial applications
        
        Please propose reasonable future development predictions based on existing research.
        Format the content in a style suitable for IEEE conference papers, with clear section organization and academic tone.
        DO NOT use any markdown formatting like # or * in your response.
        DO NOT use numbered lists with dots (like "1.") for paragraph numbering. Use proper IEEE-style paragraph organization.
        """
        future_directions = rag.generate_section("Future Research Directions", future_prompt, paper_categories)
        
        # Generate conclusion
        conclusion_prompt = """
        Provide a comprehensive conclusion for the entire survey, including:
        1. A concise review of the research status
        2. Brief summary of main research directions and achievements
        3. Emphasis on research challenges and future directions
        4. Assessment and outlook on the overall development of this research field
        
        The conclusion should be concise and clear, highlighting the main points, and encouraging future research.
        Format the conclusion in a style suitable for IEEE conference papers, with proper academic tone.
        DO NOT use any markdown formatting like # or * in your response.
        DO NOT use numbered lists with dots (like "1.") for paragraph numbering. Use proper IEEE-style paragraph organization.
        """
        conclusion = rag.generate_section("Conclusion", conclusion_prompt, paper_categories)
        
        # Generate references
        references = rag.generate_references(papers)
        
        # Assemble final results
        survey_data = {
            'title': title,
            'abstract': abstract,
            'introduction': introduction,
            'problem_definition': problem_definition,
            'challenges': challenges,
            'future_directions': future_directions,
            'conclusion': conclusion,
            'references': references,
            'papers': papers  # Include papers for reference generation
        }
        
        self.logger.info("Literature survey generation completed")
        
        return survey_data