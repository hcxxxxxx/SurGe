#!/bin/bash

# 检查是否提供了主题参数
if [ $# -eq 0 ]; then
    echo "请提供研究主题，例如: ./survey.sh \"Artificial Intelligence\""
    exit 1
fi

# 获取研究主题参数
TOPIC="$1"

# 将主题转换为小写并用连字符替换空格，用于文件名
FILENAME=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

echo "正在生成关于 '$TOPIC' 的研究综述..."

# 运行 Python 脚本生成综述
python3 main.py --topic "$TOPIC"

# 检查 Python 脚本是否成功执行
if [ $? -ne 0 ]; then
    echo "生成综述时出错，请检查错误信息"
    exit 1
fi

# 运行 pdflatex 生成 PDF
echo "正在编译 LaTeX 文档为 PDF..."
pdflatex "output/research-survey-on-$FILENAME.tex"

# 检查PDF是否成功生成
PDF_FILE="research-survey-on-$FILENAME.pdf"
if [ ! -f "$PDF_FILE" ]; then
    echo "PDF文件生成失败"
    exit 1
fi

# 移动PDF文件到output文件夹
echo "正在移动PDF文件到output文件夹..."
mv "$PDF_FILE" "output/"

# 删除临时文件
echo "正在清理临时文件..."
rm -f "research-survey-on-$FILENAME.log" "research-survey-on-$FILENAME.aux" "research-survey-on-$FILENAME.out"

echo "完成！您的研究综述已生成在 output/$PDF_FILE" 