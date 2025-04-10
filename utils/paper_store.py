"""
全局存储论文信息的模块
"""

# 存储所有论文的标题和作者信息
paper_info_store = []

def store_paper_info(title, authors):
    """
    存储论文的标题和作者信息
    
    参数:
    - title: 论文标题
    - authors: 作者列表
    """
    paper_info_store.append({
        'title': title,
        'authors': authors
    })
    
def get_all_papers():
    """
    获取所有存储的论文信息
    
    返回:
    - 论文信息列表
    """
    return paper_info_store

def clear_paper_store():
    """
    清空论文信息存储
    """
    global paper_info_store
    paper_info_store = [] 