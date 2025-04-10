import os
import sys
import argparse
import time
from tqdm import tqdm
from utils.logger import Logger
# from utils.markdown_generator import MarkdownGenerator
from utils.latex_generator import LatexGenerator
from modules.search_engine import SearchEngine
from modules.paper_analyzer import PaperAnalyzer
from modules.content_generator import ContentGenerator
from config import MAX_PAPERS, SEARCH_TIMEOUT, PAPER_SOURCES, OUTPUT_DIR

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='DeepResearch Agent - 自动生成文献综述')
    parser.add_argument('--topic', type=str, help='研究主题')
    parser.add_argument('--papers', type=int, default=MAX_PAPERS, help=f'最大论文数量 (默认: {MAX_PAPERS})')
    parser.add_argument('--timeout', type=int, default=SEARCH_TIMEOUT, help=f'搜索超时时间 (默认: {SEARCH_TIMEOUT}秒)')
    parser.add_argument('--output', type=str, default=OUTPUT_DIR, help=f'输出目录 (默认: {OUTPUT_DIR})')
    args = parser.parse_args()
    
    # 设置logger
    logger = Logger("DeepResearch")
    logger.info("DeepResearch Agent 启动")
    
    # 如果命令行没有指定主题，提示用户输入
    research_topic = args.topic
    if not research_topic:
        research_topic = input("请输入要研究的主题: ")
    
    if not research_topic:
        logger.error("未指定研究主题，程序退出")
        sys.exit(1)
    
    # 创建输出目录
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # 开始计时
    start_time = time.time()
    
    try:
        # 第一步：搜索论文
        logger.info(f"开始为主题 '{research_topic}' 搜索论文")
        search_engine = SearchEngine(max_papers=args.papers, timeout=args.timeout)
        papers = search_engine.search(research_topic, PAPER_SOURCES)
        
        if not papers:
            logger.error("未找到相关论文，程序退出")
            sys.exit(1)
        
        # 第二步：分析论文
        logger.info("开始分析论文内容")
        analyzer = PaperAnalyzer()
        analysis_results = analyzer.analyze_papers(papers, research_topic)
        
        # 第三步：对论文进行分类
        paper_categories = analyzer.categorize_papers(analysis_results)
        
        # 打印分类结果
        logger.info("论文分类结果:")
        for category, papers in paper_categories.items():
            logger.info(f"- {category}: {len(papers)}篇")
        
        # 第四步：生成综述内容
        logger.info("开始生成综述内容")
        content_generator = ContentGenerator()
        survey_data = content_generator.generate_survey(
            research_topic, 
            paper_categories, 
            papers, 
            analysis_results
        )
        
        # 第五步：生成LaTeX文档
        logger.info("生成最终LaTeX文档")
        latex_generator = LatexGenerator(output_dir=args.output)
        latex_file = latex_generator.generate_survey(survey_data)

        
        # 计算总耗时
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.info(f"综述生成完成! 总耗时: {total_time:.2f}秒")
        logger.info(f"LaTeX输出文件: {latex_file}")
        
    except KeyboardInterrupt:
        logger.info("用户中断操作，程序退出")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序执行过程中出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()