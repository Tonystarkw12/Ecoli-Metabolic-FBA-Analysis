# -*- coding: utf-8 -*-
"""
代谢网络FBA结果可视化模块
生成高质量图表，适合展示和论文使用
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import os


def plot_flux_distribution(flux_csv_path, output_path=None):
    """
    绘制非零通量分布直方图
    
    参数:
        flux_csv_path: FBA结果CSV文件路径
        output_path: 图片输出路径
    """
    if not os.path.exists(flux_csv_path):
        print(f"✗ 找不到结果文件：{flux_csv_path}")
        return
    
    try:
        flux_data = pd.read_csv(flux_csv_path)
        
        if len(flux_data) == 0:
            print("✗ 通量数据为空")
            return
        
        # 取通量绝对值
        flux_abs = flux_data["flux_value"].abs()
        
        # 设置中文字体（如果系统支持）
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 子图1：直方图
        ax1.hist(flux_abs, bins=50, color="#2E86AB", alpha=0.7, edgecolor="black")
        ax1.set_xlabel("通量绝对值", fontsize=12)
        ax1.set_ylabel("反应数量", fontsize=12)
        ax1.set_title("代谢通量分布直方图\n(E. coli iJO1366)", fontsize=14, fontweight="bold")
        ax1.grid(alpha=0.3, linestyle="--")
        
        # 子图2：对数尺度直方图（更好展示分布）
        ax2.hist(flux_abs, bins=50, color="#A23B72", alpha=0.7, edgecolor="black")
        ax2.set_xlabel("通量绝对值 (对数尺度)", fontsize=12)
        ax2.set_ylabel("反应数量", fontsize=12)
        ax2.set_title("代谢通量分布 (log scale)", fontsize=14, fontweight="bold")
        ax2.set_xscale('log')
        ax2.grid(alpha=0.3, linestyle="--")
        
        plt.tight_layout()
        
        if output_path is None:
            output_path = "../results/flux_distribution.png"
        
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        print(f"✓ 通量分布图已保存：{output_path}")
        
    except Exception as e:
        print(f"✗ 绘制通量分布图出错：{e}")


def plot_top_reactions_bar(flux_csv_path, top_n=15, output_path=None):
    """
    绘制通量绝对值最大的前N个反应的条形图
    
    参数:
        flux_csv_path: FBA结果CSV文件路径
        top_n: 显示前N个反应
        output_path: 图片输出路径
    """
    if not os.path.exists(flux_csv_path):
        print(f"✗ 找不到结果文件：{flux_csv_path}")
        return
    
    try:
        flux_data = pd.read_csv(flux_csv_path)
        
        # 按绝对值排序，取前N
        top_flux = flux_data.reindex(flux_data["flux_value"].abs().sort_values(ascending=False).index).head(top_n)
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 颜色映射：正值为蓝色，负值为红色
        colors = ["#2E86AB" if x >= 0 else "#A23B72" for x in top_flux["flux_value"]]
        
        # 绘制条形图
        bars = ax.barh(range(len(top_flux)), top_flux["flux_value"], color=colors, alpha=0.8)
        
        # 设置标签
        ax.set_yticks(range(len(top_flux)))
        ax.set_yticklabels(top_flux["reaction_id"], fontsize=9)
        ax.set_xlabel("通量值", fontsize=12)
        ax.set_title(f"通量绝对值前{top_n}的反应\n(蓝色：正值，红色：负值)", fontsize=14, fontweight="bold")
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars, top_flux["flux_value"])):
            ax.text(value + (0.01 if value >= 0 else -0.01), i, f"{value:.3f}", 
                   va='center', ha='left' if value >= 0 else 'right', fontsize=8)
        
        ax.grid(alpha=0.3, axis='x', linestyle="--")
        plt.tight_layout()
        
        if output_path is None:
            output_path = "../results/top_reactions_bar.png"
        
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        print(f"✓ 通量条形图已保存：{output_path}")
        
    except Exception as e:
        print(f"✗ 绘制条形图出错：{e}")


def plot_core_metabolic_pathway():
    """
    绘制核心代谢通路网络图（糖酵解示例）
    展示网络可视化能力，无需复杂数据
    """
    try:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建网络
        G = nx.DiGraph()
        
        # 添加代谢物节点
        metabolites = ["Glucose", "G6P", "F6P", "FBP", "G3P", "PEP", "Pyruvate", "ATP", "NADH"]
        G.add_nodes_from(metabolites)
        
        # 添加反应边（糖酵解途径）
        edges = [
            ("Glucose", "G6P"), ("G6P", "F6P"), ("F6P", "FBP"), 
            ("FBP", "G3P"), ("G3P", "PEP"), ("PEP", "Pyruvate"),
            ("ATP", "G6P"), ("ATP", "FBP"), ("NADH", "G3P")
        ]
        G.add_edges_from(edges)
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 布局
        pos = nx.spring_layout(G, seed=42, k=2)
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="#A23B72", 
                              alpha=0.8, ax=ax)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color="#2E86AB", width=2, 
                              arrowsize=20, arrowstyle='->', alpha=0.7, ax=ax)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', 
                               font_color='white', ax=ax)
        
        ax.set_title("核心代谢通路网络图\n(糖酵解途径示例)", fontsize=14, fontweight="bold")
        ax.axis('off')
        
        output_path = "../results/glycolysis_network.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        print(f"✓ 代谢通路网络图已保存：{output_path}")
        
    except Exception as e:
        print(f"✗ 绘制代谢通路图出错：{e}")


def plot_flux_comparison(flux_csv_path1, flux_csv_path2, label1="Condition 1", label2="Condition 2", output_path=None):
    """
    绘制两个条件下的通量比较图（高级功能）
    
    参数:
        flux_csv_path1: 第一个条件的通量结果
        flux_csv_path2: 第二个条件的通量结果
        label1, label2: 条件标签
        output_path: 输出路径
    """
    if not os.path.exists(flux_csv_path1) or not os.path.exists(flux_csv_path2):
        print("✗ 找不到比较数据文件")
        return
    
    try:
        df1 = pd.read_csv(flux_csv_path1)
        df2 = pd.read_csv(flux_csv_path2)
        
        # 合并数据
        merged = pd.merge(df1, df2, on="reaction_id", suffixes=("_1", "_2"), how="inner")
        
        if len(merged) == 0:
            print("✗ 两个条件没有共同的反应")
            return
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建散点图
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # 绘制散点
        ax.scatter(merged["flux_value_1"], merged["flux_value_2"], 
                  alpha=0.6, s=30, color="#2E86AB")
        
        # 添加对角线
        max_val = max(merged["flux_value_1"].abs().max(), merged["flux_value_2"].abs().max())
        ax.plot([-max_val, max_val], [-max_val, max_val], 'r--', alpha=0.5, label="y=x")
        
        ax.set_xlabel(f"{label1} 通量值", fontsize=12)
        ax.set_ylabel(f"{label2} 通量值", fontsize=12)
        ax.set_title(f"通量比较散点图\n{label1} vs {label2}", fontsize=14, fontweight="bold")
        ax.grid(alpha=0.3, linestyle="--")
        ax.legend()
        
        if output_path is None:
            output_path = "../results/flux_comparison.png"
        
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        
        print(f"✓ 通量比较图已保存：{output_path}")
        
    except Exception as e:
        print(f"✗ 绘制比较图出错：{e}")


if __name__ == "__main__":
    print("="*60)
    print("可视化模块测试")
    print("="*60)
    
    # 测试可视化功能
    test_csv = "../results/non_zero_flux_results.csv"
    
    if os.path.exists(test_csv):
        plot_flux_distribution(test_csv)
        plot_top_reactions_bar(test_csv, top_n=15)
        plot_core_metabolic_pathway()
        print("\n✓ 所有可视化测试完成！")
    else:
        print(f"✗ 请先运行FBA分析生成数据文件：{test_csv}")