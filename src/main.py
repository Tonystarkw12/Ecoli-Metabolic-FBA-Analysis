# -*- coding: utf-8 -*-
"""
大肠杆菌代谢网络FBA分析 - 主程序
一键运行，自动生成分析结果和可视化图表
"""

import os
import sys
from fba_analysis import load_metabolic_model, run_fba_analysis, export_results
from visualization import plot_flux_distribution, plot_top_reactions_bar, plot_core_metabolic_pathway


def check_environment():
    """检查环境和依赖"""
    print("="*60)
    print("环境检查")
    print("="*60)
    
    # 检查依赖库
    try:
        import cobra
        print("✓ cobrapy 库已安装")
    except ImportError:
        print("✗ 缺少 cobrapy 库")
        print("  请运行：pip install cobrapy")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib 库已安装")
    except ImportError:
        print("✗ 缺少 matplotlib 库")
        print("  请运行：pip install matplotlib")
        return False
    
    try:
        import networkx
        print("✓ networkx 库已安装")
    except ImportError:
        print("✗ 缺少 networkx 库")
        print("  请运行：pip install networkx")
        return False
    
    try:
        import pandas
        print("✓ pandas 库已安装")
    except ImportError:
        print("✗ 缺少 pandas 库")
        print("  请运行：pip install pandas")
        return False
    
    # 检查目录结构
    required_dirs = ["../data", "../results", "../src"]
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"✗ 缺少目录：{dir_path}")
            return False
    
    print("✓ 目录结构完整")
    return True


def check_data_file():
    """检查数据文件是否存在"""
    data_path = "../data/iJO1366.xml"
    
    if os.path.exists(data_path):
        print(f"✓ 数据文件已存在：{data_path}")
        return True
    else:
        print(f"✗ 数据文件不存在：{data_path}")
        print("\n" + "="*60)
        print("数据下载说明")
        print("="*60)
        print("请按以下步骤获取数据文件：")
        print("1. 访问 BiGG Models 数据库：https://bigg.ucsd.edu/models/iJO1366")
        print("2. 点击 'Download SBML' 下载 iJO1366.xml")
        print("3. 将下载的文件放入 data/ 文件夹中")
        print("4. 重新运行本程序")
        print("\n提示：文件约 5MB，下载时间约 1-2 分钟")
        return False


def run_complete_analysis():
    """运行完整的FBA分析流程"""
    print("\n" + "="*60)
    print("开始FBA分析流程")
    print("="*60)
    
    # 1. 加载模型
    print("\n[步骤 1/4] 加载代谢网络模型...")
    model = load_metabolic_model("../data/iJO1366.xml")
    if model is None:
        return False
    
    # 2. 运行FBA分析
    print("\n[步骤 2/4] 运行通量平衡分析...")
    solution, non_zero_flux = run_fba_analysis(model)
    if solution is None:
        return False
    
    # 3. 导出结果
    print("\n[步骤 3/4] 导出分析结果...")
    export_results(non_zero_flux, "../results/non_zero_flux_results.csv")
    
    # 4. 生成可视化图表
    print("\n[步骤 4/4] 生成可视化图表...")
    plot_flux_distribution("../results/non_zero_flux_results.csv")
    plot_top_reactions_bar("../results/non_zero_flux_results.csv", top_n=15)
    plot_core_metabolic_pathway()
    
    return True


def print_summary():
    """打印分析总结"""
    print("\n" + "="*60)
    print("分析完成！")
    print("="*60)
    print("\n📊 生成的文件：")
    print("  - results/non_zero_flux_results.csv (通量数据表)")
    print("  - results/flux_distribution.png (通量分布图)")
    print("  - results/top_reactions_bar.png (通量条形图)")
    print("  - results/glycolysis_network.png (代谢通路图)")
    
    print("\n🎯 下一步建议：")
    print("  1. 查看 results/ 目录下的图表")
    print("  2. 分析非零通量反应，识别关键代谢途径")
    print("  3. 可修改目标反应，研究不同代谢策略")
    print("  4. 可替换 data/ 中的SBML文件，分析其他微生物")
    
    print("\n📚 项目说明：")
    print("  - 本项目使用公开的E. coli iJO1366代谢模型")
    print("  - 适用于干实验代谢调控研究")
    print("  - 可扩展用于菌株优化、代谢工程等场景")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    print("\n" + "="*60)
    print("大肠杆菌代谢网络FBA分析工具")
    print("E. coli Metabolic Flux Balance Analysis")
    print("="*60)
    print("作者：周子航 - 清华大学CLS项目")
    print("邮箱：zhou-zh23@mails.tsinghua.edu.cn")
    print("="*60)
    
    # 1. 检查环境
    if not check_environment():
        print("\n✗ 环境检查失败，请修复问题后重试")
        return
    
    # 2. 检查数据文件
    if not check_data_file():
        print("\n✗ 数据文件检查失败，请按说明下载数据")
        return
    
    # 3. 运行分析
    success = run_complete_analysis()
    
    # 4. 打印总结
    if success:
        print_summary()
    else:
        print("\n✗ 分析过程中出现错误，请检查输出信息")


if __name__ == "__main__":
    main()