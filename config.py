import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenAI API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_API_MODEL", "gpt-4o-mini")

# 学术API配置
IEEE_API_KEY = os.getenv("IEEE_API_KEY")
ACM_API_KEY = os.getenv("ACM_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # 用于备用搜索

# 代理配置
HTTP_PROXY = os.getenv("HTTP_PROXY")          # HTTP代理，例如: http://127.0.0.1:7890
HTTPS_PROXY = os.getenv("HTTPS_PROXY")        # HTTPS代理，例如: http://127.0.0.1:7890
SOCKS_PROXY = os.getenv("SOCKS_PROXY")        # SOCKS代理，例如: socks5://127.0.0.1:1080
SCHOLAR_PROXY = os.getenv("SCHOLAR_PROXY")    # 专用于Google Scholar的代理
ARXIV_PROXY = os.getenv("ARXIV_PROXY")        # 专用于ArXiv的代理
IEEE_PROXY = os.getenv("IEEE_PROXY")          # 专用于IEEE的代理
ACM_PROXY = os.getenv("ACM_PROXY")            # 专用于ACM的代理

# 备用代理配置
BACKUP_HTTP_PROXY = os.getenv("BACKUP_HTTP_PROXY")    # 备用HTTP代理
BACKUP_HTTPS_PROXY = os.getenv("BACKUP_HTTPS_PROXY")  # 备用HTTPS代理
BACKUP_SOCKS_PROXY = os.getenv("BACKUP_SOCKS_PROXY")  # 备用SOCKS代理

# 是否启用代理
USE_PROXY = os.getenv("USE_PROXY", "False").lower() in ["true", "1", "yes"]
# 在主代理失败时是否尝试备用代理
USE_BACKUP_PROXY = os.getenv("USE_BACKUP_PROXY", "True").lower() in ["true", "1", "yes"]

# 搜索配置
MAX_PAPERS = 100  # 最大检索论文数量
SEARCH_TIMEOUT = 600  # 检索超时时间(秒)
MAX_RETRIES = 3  # 请求失败时的最大重试次数

# 论文来源
PAPER_SOURCES = [
    "arxiv.org",           # arXiv预印本
    "scholar.google.com",  # 谷歌学术
    "ieee.org",            # IEEE
    "acm.org",             # ACM
    # "springer.com",        # Springer
    # "sciencedirect.com",   # Science Direct
    # "nature.com",          # Nature
    # "science.org",         # Science
    # "ncbi.nlm.nih.gov",    # PubMed
    # "researchgate.net",    # ResearchGate
    # "semanticscholar.org", # Semantic Scholar
    # "dl.acm.org",          # ACM数字图书馆
    # "ieeexplore.ieee.org", # IEEE Xplore
    # "jstor.org",           # JSTOR
    # "ssrn.com",            # SSRN
    # "pnas.org",            # PNAS
    # "aps.org",             # 美国物理学会
    # "wiley.com",           # Wiley
    # "tandfonline.com",     # Taylor & Francis
    # "oup.com",             # Oxford University Press
    # "cell.com",            # Cell
    # "cnki.net",            # 中国知网
    # "wanfangdata.com.cn",  # 万方数据
    # "aclweb.org",          # ACL
    # "neurips.cc",          # NeurIPS
    # "mlr.press",           # JMLR
    # "mdpi.com",            # MDPI
    # "frontiersin.org",     # Frontiers
    # "elsevier.com",        # Elsevier
    # "biorxiv.org",         # bioRxiv
]

# RAG配置
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5

# 输出配置
OUTPUT_DIR = "output"
LOG_LEVEL = "INFO"

# LaTeX配置
LATEX_COMPILER = "pdflatex"  # LaTeX编译器
LATEX_TEMPLATE = "ieee"      # LaTeX模板类型
LATEX_AUTHOR_NAME = "Chengxun Hong"  # 作者姓名
LATEX_AUTHOR_DEPT = "Comp. Sci."  # 作者部门
LATEX_AUTHOR_INST = "Fudan University"  # 作者机构
LATEX_AUTHOR_EMAIL = "22300240021@m.fudan.edu.cn"  # 作者邮箱
LATEX_KEYWORDS = "Literature Survey, Research Topic, Future Directions"  # 关键词

# 爬虫配置
CRAWLER_DELAY_MIN = 1  # 最小请求延迟（秒）
CRAWLER_DELAY_MAX = 3  # 最大请求延迟（秒）