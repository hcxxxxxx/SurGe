import time
import random
from utils.logger import Logger
import openai
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE_URL, OPENAI_MODEL
from utils.paper_store import store_paper_info, clear_paper_store

class PaperAnalyzer:
    def __init__(self):
        self.logger = Logger("PaperAnalyzer")
        self.chat_model = ChatOpenAI(
            model_name=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL
        )
        self.logger.info(f"初始化 ChatOpenAI 模型: {OPENAI_MODEL}")
        self.logger.info(f"使用API基础URL: {OPENAI_API_BASE_URL if OPENAI_API_BASE_URL else '默认'}")
        
    def analyze_papers(self, papers, research_topic):
        """
        分析一组论文，提取关键信息
        
        参数:
        - papers: 论文列表
        - research_topic: 研究主题
        
        返回:
        - 分析结果列表
        """
        self.logger.info(f"开始分析 {len(papers)} 篇论文")
        
        # 清空之前存储的论文信息
        clear_paper_store()
        
        analysis_results = []
        
        for i, paper in enumerate(papers):
            self.logger.progress(i+1, len(papers), "论文分析")
            
            try:
                # 分析单篇论文
                result = self._analyze_paper(paper, research_topic)
                analysis_results.append(result)
                
                # 随机延迟，避免API限制
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                self.logger.error(f"分析论文 '{paper.get('title')}' 时出错: {str(e)}")
        
        self.logger.info("论文分析完成")
        return analysis_results
    
    def _analyze_paper(self, paper, research_topic):
        """
        分析单篇论文
        
        参数:
        - paper: 论文信息字典
        - research_topic: 研究主题
        
        返回:
        - 分析结果字典
        """
        title = paper.get('title', 'Untitled')
        abstract = paper.get('abstract', '')
        authors = paper.get('authors', [])
        year = paper.get('year', 'Unknown')
        
        self.logger.info(f"正在分析: {title} ---------- by: {', '.join(authors if isinstance(authors, list) else [authors])}")
        
        # 存储论文标题和作者信息
        store_paper_info(title, authors)
        
        # 使用OpenAI API分析论文
        try:
            paper_content = f"Title: {title}\nAuthors: {', '.join(authors if isinstance(authors, list) else [authors])}\nYear: {year}\nAbstract: {abstract}"
            
            prompt = f"""
            你是一个专业的论文分析助手。请分析以下论文信息，提取与研究主题"{research_topic}"相关的关键信息:

            {paper_content}
            
            请提供以下格式的分析:
            1. 研究方向: [论文所属的具体研究方向]
            2. 主要贡献: [论文的主要贡献，新方法或新发现]
            3. 技术方法: [论文使用的关键技术、算法或方法]
            4. 实验结果: [论文的主要实验结果或结论]
            5. 与研究主题的相关性: [高/中/低，以及原因]
            6. 在研究领域中的地位: [开创性工作/改进工作/应用工作/综述性工作等]
            
            请基于文本内容进行客观分析，不要添加不存在的信息。如果某项信息无法从摘要中确定，请标注为"信息不足"。
            """
            
            messages = [
                {"role": "system", "content": "你是一个专业的学术论文分析助手。"},
                {"role": "user", "content": prompt}
            ]
            
            response = self.chat_model.invoke(messages)
            
            analysis_text = response.content
            
            # 提取分析结果
            result = {
                'paper': paper,
                'analysis': analysis_text,
                'research_direction': self._extract_field(analysis_text, "研究方向"),
                'contributions': self._extract_field(analysis_text, "主要贡献"),
                'methods': self._extract_field(analysis_text, "技术方法"),
                'results': self._extract_field(analysis_text, "实验结果"),
                'relevance': self._extract_field(analysis_text, "与研究主题的相关性"),
                'status': self._extract_field(analysis_text, "在研究领域中的地位")
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"调用OpenAI API分析论文时出错: {str(e)}")
            # 返回基本信息和错误标记
            return {
                'paper': paper,
                'analysis': f"分析失败: {str(e)}",
                'research_direction': "信息不足",
                'contributions': "信息不足",
                'methods': "信息不足",
                'results': "信息不足",
                'relevance': "信息不足",
                'status': "信息不足",
                'error': True
            }
    
    def _extract_field(self, text, field_name):
        """从分析文本中提取特定字段的内容"""
        lines = text.split('\n')
        for line in lines:
            if line.startswith(f"{field_name}:") or line.startswith(f"{field_name}：") or line.startswith(f"{len(field_name)}. {field_name}:"):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    return parts[1].strip()
                return ""
        return "信息不足"
    
    def categorize_papers(self, analysis_results):
        """
        根据论文分析结果对论文进行分类
        
        参数:
        - analysis_results: 论文分析结果列表
        
        返回:
        - 分类结果字典
        """
        self.logger.info("开始对论文进行分类")
        
        # 收集所有研究方向
        research_directions = {}
        for result in analysis_results:
            direction = result.get('research_direction', '其他')
            if direction == "信息不足":
                direction = "未分类"
            
            if direction not in research_directions:
                research_directions[direction] = []
            
            research_directions[direction].append(result)
        
        # 对每个方向内的论文进行相关性排序
        for direction, papers in research_directions.items():
            # 根据相关性高中低进行排序
            def relevance_score(result):
                relevance = result.get('relevance', '').lower()
                if '高' in relevance:
                    return 3
                elif '中' in relevance:
                    return 2
                elif '低' in relevance:
                    return 1
                return 0
            
            research_directions[direction] = sorted(papers, key=relevance_score, reverse=True)
        
        self.logger.info(f"论文分类完成，共分为 {len(research_directions)} 个类别")
        
        return research_directions