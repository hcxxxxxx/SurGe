import os
import re
from datetime import datetime
from config import (
    LATEX_COMPILER, LATEX_TEMPLATE, LATEX_AUTHOR_NAME, 
    LATEX_AUTHOR_DEPT, LATEX_AUTHOR_INST, LATEX_AUTHOR_EMAIL, 
    LATEX_KEYWORDS
)

class LatexGenerator:
    def __init__(self, output_dir="output"):
        """
        初始化LaTeX生成器
        
        参数:
        - output_dir: 保存生成的LaTeX文件的目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def _fix_math_formulas(self, text):
        """
        修复文本中的数学公式，确保它们被正确包裹在美元符号中
        
        参数:
        - text: 需要修复的文本
        
        返回:
        - 修复后的文本
        """
        # 查找可能的数学公式模式
        # 1. 查找下划线(_)和上标(^)符号，它们通常表示数学公式
        # 2. 查找常见的数学符号和表达式
        
        # 修复下划线和上标
        text = re.sub(r'(?<!\$)(?<!\\)_([a-zA-Z0-9]+)(?!\$)', r'$_\1$', text)
        text = re.sub(r'(?<!\$)(?<!\\)\^([a-zA-Z0-9]+)(?!\$)', r'$^\1$', text)
        
        # 修复常见的数学表达式
        math_patterns = [
            r'min_([a-zA-Z0-9]+)\s+max_([a-zA-Z0-9]+)',  # min_G max_D
            r'min_([a-zA-Z0-9]+)',  # min_G
            r'max_([a-zA-Z0-9]+)',  # max_D
            r'E\[([^\]]+)\]',  # E[log(D(x))]
            r'log\(([^)]+)\)',  # log(D(x))
            r'\\frac\{([^}]+)\}\{([^}]+)\}',  # \frac{num}{den}
            r'\\sum_([a-zA-Z0-9]+)\^([a-zA-Z0-9]+)',  # \sum_i^N
            r'\\prod_([a-zA-Z0-9]+)\^([a-zA-Z0-9]+)',  # \prod_i^N
        ]
        
        for pattern in math_patterns:
            text = re.sub(pattern, r'$\0$', text)
        
        # 修复已经部分包裹的数学公式
        text = re.sub(r'(?<!\$)(?<!\\)\$(?!\$)', r'$', text)
        text = re.sub(r'(?<!\$)(?<!\\)\$(?!\$)', r'$', text)
        
        # 处理多行数学公式，使用$$而不是$
        # 查找可能的数学公式块（多行公式）
        math_block_patterns = [
            r'\$\$(.*?)\$\$',  # 已经使用$$的公式块
            r'\\begin\{equation\}(.*?)\\end\{equation\}',  # equation环境
            r'\\begin\{align\}(.*?)\\end\{align\}',  # align环境
            r'\\begin\{aligned\}(.*?)\\end\{aligned\}',  # aligned环境
            r'\\begin\{gather\}(.*?)\\end\{gather\}',  # gather环境
            r'\\begin\{multline\}(.*?)\\end\{multline\}',  # multline环境
        ]
        
        # 确保这些环境使用$$包裹
        for pattern in math_block_patterns:
            text = re.sub(pattern, r'$$\1$$', text, flags=re.DOTALL)
        
        return text
        
    def _fix_quotes(self, text):
        """
        修复文本中的引号，使用LaTeX特定的引号语法
        
        参数:
        - text: 需要修复的文本
        
        返回:
        - 修复后的文本
        """
        # 替换普通的双引号为LaTeX特定的引号格式
        # 先处理已经是LaTeX格式的引号，避免重复替换
        if "``" in text and "''" in text:
            return text
            
        # 处理引号对
        # 使用负向前视和负向后视确保不会影响已存在的LaTeX引号
        text = re.sub(r'(?<!`)(?<!\\)"(.*?)(?<!\\)"(?!\')', r"``\1''", text)
        
        # 处理剩余的未配对引号
        text = re.sub(r'(?<!`)(?<!\\)"', r"``", text)
        
        return text
        
    def _fix_ampersands(self, text):
        """
        修复文本中的&符号，确保它们被正确转义
        
        参数:
        - text: 需要修复的文本
        
        返回:
        - 修复后的文本
        """
        # 替换未转义的&符号为\&
        text = re.sub(r'(?<!\\)&', r'\\&', text)
        return text
        
    def _fix_greek_letters(self, text):
        """
        修复文本中的Unicode希腊字母，替换为LaTeX格式
        
        参数:
        - text: 需要修复的文本
        
        返回:
        - 修复后的文本
        """
        # 希腊字母映射表
        greek_map = {
            'α': '$\\alpha$', 'β': '$\\beta$', 'γ': '$\\gamma$', 'δ': '$\\delta$',
            'ε': '$\\epsilon$', 'ζ': '$\\zeta$', 'η': '$\\eta$', 'θ': '$\\theta$',
            'ι': '$\\iota$', 'κ': '$\\kappa$', 'λ': '$\\lambda$', 'μ': '$\\mu$',
            'ν': '$\\nu$', 'ξ': '$\\xi$', 'ο': '$\\omicron$', 'π': '$\\pi$',
            'ρ': '$\\rho$', 'σ': '$\\sigma$', 'τ': '$\\tau$', 'υ': '$\\upsilon$',
            'φ': '$\\phi$', 'χ': '$\\chi$', 'ψ': '$\\psi$', 'ω': '$\\omega$',
            'Γ': '$\\Gamma$', 'Δ': '$\\Delta$',
            'Θ': '$\\Theta$',
            'Λ': '$\\Lambda$',
            'Ξ': '$\\Xi$', 'Π': '$\\Pi$',
            'Σ': '$\\Sigma$', 
            'Φ': '$\\Phi$', 'Ψ': '$\\Psi$', 'Ω': '$\\Omega$'
        }
        
        # 替换所有希腊字母
        for greek, latex in greek_map.items():
            text = text.replace(greek, latex)
            
        return text
        
    def _remove_duplicate_section_titles(self, text, section_title):
        """
        移除文本中重复出现的章节标题
        
        参数:
        - text: 需要处理的文本
        - section_title: 章节标题
        
        返回:
        - 处理后的文本
        """
        # 移除文本开头重复的章节标题
        text = re.sub(f'^{section_title}\s*', '', text, flags=re.IGNORECASE)
        
        # 移除文本中其他可能重复的章节标题
        text = re.sub(f'\n{section_title}\s*\n', '\n', text, flags=re.IGNORECASE)
        
        return text
        
    def generate_survey(self, data, filename=None):
        """
        从综述数据生成LaTeX文件
        
        参数:
        - data: 包含综述所有部分的字典
        - filename: 输出文件的可选文件名，默认为经过清理的标题
        
        返回:
        - 生成的LaTeX文件路径
        """
        title = data.get("title", "Literature Survey")
        if not filename:
            # 清理标题以用作文件名
            filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
            filename = re.sub(r'[-\s]+', '-', filename)
            
        filepath = os.path.join(self.output_dir, f"{filename}.tex")
        
        # 检查分类是否有内容
        taxonomy_data = data.get("taxonomy", {})
        has_taxonomy = bool(taxonomy_data) and any(content.strip() for content in taxonomy_data.values())
        
        with open(filepath, "w", encoding="utf-8") as f:
            # LaTeX文档前导部分
            f.write("\\documentclass[conference]{IEEEtran}\n")
            f.write("\\usepackage{amsmath,amssymb,amsfonts}\n")
            f.write("\\usepackage{graphicx}\n")
            f.write("\\usepackage{textcomp}\n")
            f.write("\\usepackage{xcolor}\n")
            f.write("\\usepackage{hyperref}\n")
            f.write("\\usepackage{booktabs}\n")
            f.write("\\usepackage{multirow}\n")
            f.write("\\usepackage{listings}\n")
            f.write("\\usepackage{algorithm}\n")
            f.write("\\usepackage{algorithmic}\n")
            f.write("\\usepackage{cite}\n")
            f.write("\\usepackage{url}\n")
            f.write("\\usepackage{enumitem}\n\n")
            
            # 设置列表样式，符合IEEE标准
            f.write("\\setlist[itemize]{leftmargin=*,label=\\textbullet}\n")
            f.write("\\setlist[enumerate]{leftmargin=*,label=\\arabic*}\n\n")
            
            # 配置hyperref包
            f.write("\\hypersetup{\n")
            f.write("    colorlinks=false,\n")
            f.write("    linkcolor=blue,\n")
            f.write("    filecolor=magenta,\n")
            f.write("    urlcolor=cyan,\n")
            f.write("    pdftitle={" + title + "},\n")
            f.write("    pdfauthor={" + LATEX_AUTHOR_NAME + "},\n")
            f.write("    pdfsubject={Literature Survey},\n")
            f.write("    pdfkeywords={" + LATEX_KEYWORDS + "}\n")
            f.write("}\n\n")
            
            # 文档开始
            f.write("\\begin{document}\n\n")
            
            # 标题
            f.write("\\title{" + title + "}\n\n")
            
            # 作者信息（使用配置文件中的信息）
            f.write("\\author{\n")
            f.write(f"    \\IEEEauthorblockN{{{LATEX_AUTHOR_NAME}}}\n")
            f.write("    \\IEEEauthorblockA{\n")
            f.write(f"        \\textit{{{LATEX_AUTHOR_DEPT}}}\\\\\n")
            f.write(f"        \\textit{{{LATEX_AUTHOR_INST}}}\\\\\n")
            f.write(f"        Email: {LATEX_AUTHOR_EMAIL}\n")
            f.write("    }\n")
            f.write("}\n\n")
            
            # 生成标题页
            f.write("\\maketitle\n\n")
            
            # 添加目录（IEEE风格，带超链接）
            f.write("\\begin{center}\n")
            f.write("    \\textbf{\\large Contents}\n")
            f.write("\\end{center}\n\n")
            f.write("\\begin{itemize}[leftmargin=*]\n")
            f.write("    \\item \\hyperlink{sec:abstract}{Abstract}\n")
            f.write("    \\item \\hyperlink{sec:introduction}{Introduction}\n")
            f.write("    \\item \\hyperlink{sec:problem}{Problem Definition and Basic Concepts}\n")
            f.write("    \\item \\hyperlink{sec:challenges}{Challenges and Open Problems}\n")
            f.write("    \\item \\hyperlink{sec:future}{Future Research Directions}\n")
            f.write("    \\item \\hyperlink{sec:conclusion}{Conclusion}\n")
            f.write("    \\item \\hyperlink{sec:references}{References}\n")
            f.write("\\end{itemize}\n") 
            f.write("\\vspace{2em}\n")
            
            # 摘要
            f.write("\\begin{abstract}\n")
            f.write("\\hypertarget{sec:abstract}\n")
            # 移除可能存在的#符号
            abstract = data.get("abstract", "No abstract provided.")
            abstract = re.sub(r'#+', '', abstract)
            # 确保数学公式正确格式化
            abstract = self._fix_math_formulas(abstract)
            # 修复引号格式
            abstract = self._fix_quotes(abstract)
            # 修复&符号
            abstract = self._fix_ampersands(abstract)
            # 修复希腊字母
            abstract = self._fix_greek_letters(abstract)
            f.write(abstract + "\n")
            f.write("\\end{abstract}\n\n")
            
            # # 关键词（使用配置文件中的关键词）
            # f.write("\\begin{IEEEkeywords}\n")
            # f.write(LATEX_KEYWORDS + "\n")
            # f.write("\\end{IEEEkeywords}\n\n")
            
            # 引言
            f.write("\\section{Introduction}\n")
            f.write("\\hypertarget{sec:introduction}\n")
            # 移除可能存在的#符号
            introduction = data.get("introduction", "No introduction provided.")
            introduction = re.sub(r'#+', '', introduction)
            # 确保数学公式正确格式化
            introduction = self._fix_math_formulas(introduction)
            # 修复引号格式
            introduction = self._fix_quotes(introduction)
            # 修复&符号
            introduction = self._fix_ampersands(introduction)
            # 修复希腊字母
            introduction = self._fix_greek_letters(introduction)
            # 移除重复的章节标题
            introduction = self._remove_duplicate_section_titles(introduction, "Introduction")
            f.write(introduction + "\n\n")
            
            # 问题定义和基本概念
            f.write("\\section{Problem Definition and Basic Concepts}\n")
            f.write("\\hypertarget{sec:problem}\n")
            # 移除可能存在的#符号
            problem_definition = data.get("problem_definition", "No problem definition provided.")
            problem_definition = re.sub(r'#+', '', problem_definition)
            # 确保数学公式正确格式化
            problem_definition = self._fix_math_formulas(problem_definition)
            # 修复引号格式
            problem_definition = self._fix_quotes(problem_definition)
            # 修复&符号
            problem_definition = self._fix_ampersands(problem_definition)
            # 修复希腊字母
            problem_definition = self._fix_greek_letters(problem_definition)
            # 移除重复的章节标题
            problem_definition = self._remove_duplicate_section_titles(problem_definition, "Problem Definition and Basic Concepts")
            f.write(problem_definition + "\n\n")
            
            # 挑战和开放问题
            f.write("\\section{Challenges and Open Problems}\n")
            f.write("\\hypertarget{sec:challenges}\n")
            # 移除可能存在的#符号
            challenges = data.get("challenges", "No challenges provided.")
            challenges = re.sub(r'#+', '', challenges)
            # 确保数学公式正确格式化
            challenges = self._fix_math_formulas(challenges)
            # 修复引号格式
            challenges = self._fix_quotes(challenges)
            # 修复&符号
            challenges = self._fix_ampersands(challenges)
            # 修复希腊字母
            challenges = self._fix_greek_letters(challenges)
            # 移除重复的章节标题
            challenges = self._remove_duplicate_section_titles(challenges, "Challenges and Open Problems")
            f.write(challenges + "\n\n")
            
            # 未来研究方向
            f.write("\\section{Future Research Directions}\n")
            f.write("\\hypertarget{sec:future}\n")
            # 移除可能存在的#符号
            future_directions = data.get("future_directions", "No future directions provided.")
            future_directions = re.sub(r'#+', '', future_directions)
            # 确保数学公式正确格式化
            future_directions = self._fix_math_formulas(future_directions)
            # 修复引号格式
            future_directions = self._fix_quotes(future_directions)
            # 修复&符号
            future_directions = self._fix_ampersands(future_directions)
            # 修复希腊字母
            future_directions = self._fix_greek_letters(future_directions)
            # 移除重复的章节标题
            future_directions = self._remove_duplicate_section_titles(future_directions, "Future Research Directions")
            f.write(future_directions + "\n\n")
            
            # 结论
            f.write("\\section{Conclusion}\n")
            f.write("\\hypertarget{sec:conclusion}\n")
            # 移除可能存在的#符号
            conclusion = data.get("conclusion", "No conclusion provided.")
            conclusion = re.sub(r'#+', '', conclusion)
            # 确保数学公式正确格式化
            conclusion = self._fix_math_formulas(conclusion)
            # 修复引号格式
            conclusion = self._fix_quotes(conclusion)
            # 修复&符号
            conclusion = self._fix_ampersands(conclusion)
            # 修复希腊字母
            conclusion = self._fix_greek_letters(conclusion)
            # 移除重复的章节标题
            conclusion = self._remove_duplicate_section_titles(conclusion, "Conclusion")
            f.write(conclusion + "\n\n")
            
            # 参考文献
            f.write("\\section*{References}\n")
            f.write("\\hypertarget{sec:references}\n")
            references = data.get("references", [])
            papers = data.get("papers", [])
            
            # 判断是否有有效的参考文献
            if references and len(references) > 0:
                for reference in references:
                    # 修复&符号
                    reference = self._fix_ampersands(reference)
                    f.write(f"{reference}\n\n")
            else:
                f.write("No valid references found.\n\n")
            
            # 文档结束
            f.write("\\end{document}\n")
        
        return filepath 