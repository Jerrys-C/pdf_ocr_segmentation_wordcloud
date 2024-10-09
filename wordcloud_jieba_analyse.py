import jieba.analyse
import os
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re


# 从文本文件中读取内容
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def load_stopwords_from_directory(directory_path):
    stopwords = set()  # 使用集合存储停用词，自动去重
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # 确保只读取 txt 文件
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    stopwords.add(line.strip())  # 去除每行的换行符和多余空格
    return stopwords


# 清理OCR输出的文本，移除多余的空格
def clean_text(text):
    cleaned_text = re.sub(r'\s+', '', text)  # 去掉所有空格，包括换行
    return cleaned_text


# 使用 jieba.analyse 提取关键词
def extract_keywords(text, top_k=200):
    # 使用 TF-IDF 提取关键词，默认提取前100个关键词
    keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=False)
    return " ".join(keywords)


def generate_wordcloud(text, output_image_path, font_path, stopwords=None):
    wordcloud = WordCloud(width=1600, height=800, background_color=None, mode='RGBA',
                          collocations=False, font_path=font_path, stopwords=stopwords).generate(text)

    # 显示词云图像
    plt.figure(figsize=(16, 8), dpi=300)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # 保存词云图像
    wordcloud.to_file(output_image_path)
    plt.savefig(output_image_path, format='png', dpi=300, transparent=True, bbox_inches='tight')
    plt.show()


# 主函数修改
def main():
    # 替换为你生成的 txt 文件路径
    txt_file_path = 'output_text.txt'
    # 替换为输出词云图像的路径
    wordcloud_image_path = 'wordcloud_output.png'
    # 替换为中文字体路径
    font_path = '/System/Library/Fonts/STHeiti Medium.ttc'

    # 读取文本文件中的内容
    text = read_text_from_file(txt_file_path)

    # 自定义停用词列表
    stopwords_directory = 'stopwords/'  # 假设你的停用词放在 "stopwords" 文件夹下
    stopwords = load_stopwords_from_directory(stopwords_directory)

    # 打印停用词的数量，确认加载成功
    print(f"总共加载了 {len(stopwords)} 个停用词")

    # 清理 OCR 输出的文本
    cleaned_text = clean_text(text)

    # 使用 jieba 提取关键词
    keywords = extract_keywords(cleaned_text)

    # 生成词云并保存
    generate_wordcloud(keywords, wordcloud_image_path, font_path, stopwords)


# 调用主函数
main()
