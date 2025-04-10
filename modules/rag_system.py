import openai
from utils.logger import Logger
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_API_BASE_URL, OPENAI_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS
from utils.paper_store import get_all_papers

class RAGSystem:
    def __init__(self):
        self.logger = Logger("RAGSystem")
        self.chat_model = ChatOpenAI(
            model_name=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY,
            base_url=OPENAI_API_BASE_URL
        )
        self.logger.info(f"初始化 ChatOpenAI 模型: {OPENAI_MODEL}")
        self.logger.info(f"使用API基础URL: {OPENAI_API_BASE_URL if OPENAI_API_BASE_URL else '默认'}")
        self.documents = []
        
    def add_documents(self, papers, analysis_results):
        """
        添加文档到RAG系统
        
        参数:
        - papers: 论文列表
        - analysis_results: 分析结果列表
        """
        self.logger.info(f"为RAG系统添加 {len(papers)} 篇论文数据")
        
        # 清空已有文档
        self.documents = []
        
        # 为每篇论文创建文档
        for paper, analysis in zip(papers, analysis_results):
            title = paper.get('title', 'Untitled')
            abstract = paper.get('abstract', '')
            authors = paper.get('authors', [])
            if isinstance(authors, list):
                authors = ', '.join(authors)
            year = paper.get('year', 'Unknown')
            source = paper.get('source', 'Unknown')
            
            # 添加基本信息
            doc = {
                'title': title,
                'content': f"Title: {title}\nAuthors: {authors}\nYear: {year}\nSource: {source}\nAbstract: {abstract}",
                'metadata': {
                    'paper_id': paper.get('id', ''),
                    'source': source,
                    'year': year
                }
            }
            
            # 添加分析结果
            if analysis:
                doc['analysis'] = analysis.get('analysis', '')
                doc['research_direction'] = analysis.get('research_direction', '')
                doc['contributions'] = analysis.get('contributions', '')
                doc['methods'] = analysis.get('methods', '')
                doc['results'] = analysis.get('results', '')
                doc['relevance'] = analysis.get('relevance', '')
                doc['status'] = analysis.get('status', '')
                
                # 更新内容，加入分析结果
                doc['content'] += f"\n\nAnalysis:\n{analysis.get('analysis', '')}"
            
            self.documents.append(doc)
        
        self.logger.info("文档添加完成")
        
        # 创建文档块
        self._create_chunks()
    
    def _create_chunks(self):
        """创建文档块以便于检索"""
        self.logger.info("正在创建文档块...")
        
        self.chunks = []
        
        for doc in self.documents:
            content = doc['content']
            
            # 简单的分块策略 - 按段落分
            paragraphs = content.split('\n\n')
            
            for i, para in enumerate(paragraphs):
                if len(para.strip()) == 0:
                    continue
                    
                chunk = {
                    'title': doc['title'],
                    'content': para,
                    'doc_id': self.documents.index(doc),
                    'chunk_id': i,
                    'metadata': doc.get('metadata', {})
                }
                
                # 如果是分析部分，添加额外元数据
                if 'Analysis:' in para:
                    for key in ['research_direction', 'contributions', 'methods', 'results']:
                        if key in doc:
                            chunk['metadata'][key] = doc[key]
                
                self.chunks.append(chunk)
        
        self.logger.info(f"创建了 {len(self.chunks)} 个文档块")
    
    def generate_section(self, section_name, section_prompt, paper_categories=None):
        """
        生成综述的特定部分
        
        参数:
        - section_name: 部分名称
        - section_prompt: 生成提示
        - paper_categories: 论文分类结果
        
        返回:
        - 生成的内容
        """
        self.logger.info(f"开始生成 '{section_name}' 部分")
        
        try:
            # 准备背景资料
            context = ""
            
            # 如果提供了论文分类，将其作为上下文
            if paper_categories:
                context += "研究领域分类和论文摘要:\n\n"
                for category, papers in paper_categories.items():
                    context += f"## {category}\n"
                    for i, paper in enumerate(papers[:5]):  # 每个类别最多包括5篇
                        p = paper['paper']
                        context += f"{i+1}. {p.get('title')} ({p.get('year', 'Unknown')})\n"
                        context += f"   摘要: {p.get('abstract', '')[:200]}...\n"
                        context += f"   贡献: {paper.get('contributions', '')}\n\n"
            
            # 准备提示
            full_prompt = f"""
            你是一个专业的学术综述生成系统。请根据以下信息，生成综述的"{section_name}"部分：
            
            {context}
            
            请生成以下内容:
            {section_prompt}
            
            请确保内容学术性强，逻辑清晰，结构合理，并引用相关论文的观点。
            """
            
            # 调用OpenAI API
            messages = [
                {"role": "system", "content": "你是一个专业的学术综述生成助手。"},
                {"role": "user", "content": full_prompt}
            ]
            
            response = self.chat_model.invoke(
                messages,
                temperature=0.3,
                max_tokens=2500
            )
            
            content = response.content
            self.logger.info(f"'{section_name}' 部分生成完成")
            
            return content
            
        except Exception as e:
            self.logger.error(f"生成 '{section_name}' 部分时出错: {str(e)}")
            return f"生成 {section_name} 部分时出错: {str(e)}"
    
    def generate_references(self, papers):
        """
        生成参考文献列表
        
        参数:
        - papers: 论文列表（实际上不使用，使用全局存储的论文信息）
        
        返回:
        - references: 参考文献列表
        """
        references = []
        
        # 使用全局存储的论文信息
        stored_papers = get_all_papers()
        
        for i, paper_info in enumerate(stored_papers, 1):
            title = paper_info.get('title', '')
            authors = paper_info.get('authors', [])
            
            # 格式化作者：显示所有作者姓名，不使用et al.省略
            if isinstance(authors, list):
                if len(authors) >= 1:
                    formatted_authors = ", ".join(authors)
                else:
                    formatted_authors = "Unknown Author"
            else:
                formatted_authors = authors
                
            # 创建参考文献条目：[编号] 作者姓名, "论文标题"
            # 使用LaTeX特定的引号语法``和''代替普通双引号
            reference = f"[{i}] {formatted_authors}, ``{title}''"
            
            references.append(reference)
            self.logger.info(f"Added reference: {title}")
        
        self.logger.info(f"Generated {len(references)} references")
        return references