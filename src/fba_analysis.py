# -*- coding: utf-8 -*-
"""
代谢网络通量平衡分析（FBA）核心模块
适用于干实验微生物代谢调控研究
"""

import cobra
import pandas as pd
import os


def load_metabolic_model(sbml_path):
    """
    加载代谢网络模型（SBML格式）
    
    参数:
        sbml_path: SBML文件路径
        
    返回:
        model: cobra.Model对象
    """
    try:
        model = cobra.io.read_sbml_model(sbml_path)
        print(f"✓ 成功加载模型：{model.id}")
        print(f"  - 反应数量：{len(model.reactions)}")
        print(f"  - 代谢物数量：{len(model.metabolites)}")
        print(f"  - 基因数量：{len(model.genes)}")
        return model
    except FileNotFoundError:
        print(f"✗ 错误：找不到文件 {sbml_path}")
        print("  请确保已从BiGG数据库下载iJO1366.xml并放入data/文件夹")
        return None
    except Exception as e:
        print(f"✗ 加载模型时出错：{e}")
        return None


def run_fba_analysis(model, target_reaction="BIOMASS_Ec_iJO1366_core_53p95M"):
    """
    运行通量平衡分析（FBA）
    
    参数:
        model: cobra.Model对象
        target_reaction: 目标反应ID（默认为大肠杆菌生物量合成）
        
    返回:
        solution: FBA求解结果对象
        non_zero_flux: 非零通量反应数据框
    """
    if model is None:
        print("✗ 模型为空，无法进行FBA分析")
        return None, None
    
    try:
        # 设置目标函数
        model.objective = target_reaction
        print(f"\n✓ 设置目标反应：{target_reaction}")
        
        # 运行FBA
        print("正在运行FBA分析...")
        solution = model.optimize()
        
        if solution.status != 'optimal':
            print(f"⚠ 警告：FBA求解状态为 {solution.status}，可能不是最优解")
        
        # 提取通量结果
        flux_data = pd.DataFrame({
            "reaction_id": [rxn.id for rxn in model.reactions],
            "flux_value": [solution.fluxes[rxn.id] for rxn in model.reactions],
            "reaction_name": [rxn.name for rxn in model.reactions]
        })
        
        # 筛选非零通量反应
        non_zero_flux = flux_data[flux_data["flux_value"].abs() > 1e-6].copy()
        non_zero_flux = non_zero_flux.sort_values("flux_value", key=abs, ascending=False)
        
        print(f"✓ FBA分析完成")
        print(f"  - 总反应数：{len(flux_data)}")
        print(f"  - 非零通量反应数：{len(non_zero_flux)}")
        print(f"  - 目标函数值：{solution.objective_value:.6f}")
        
        return solution, non_zero_flux
        
    except Exception as e:
        print(f"✗ FBA分析出错：{e}")
        return None, None


def get_top_reactions(non_zero_flux, top_n=20):
    """
    获取通量绝对值最大的前N个反应
    
    参数:
        non_zero_flux: 非零通量数据框
        top_n: 返回前N个反应
        
    返回:
        top_reactions: 前N个反应数据框
    """
    if non_zero_flux is None or len(non_zero_flux) == 0:
        return None
    
    top_reactions = non_zero_flux.head(top_n).copy()
    top_reactions["flux_abs"] = top_reactions["flux_value"].abs()
    return top_reactions


def export_results(non_zero_flux, output_path):
    """
    导出FBA分析结果到CSV文件
    
    参数:
        non_zero_flux: 非零通量数据框
        output_path: 输出文件路径
    """
    if non_zero_flux is not None:
        non_zero_flux.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✓ 结果已导出到：{output_path}")


if __name__ == "__main__":
    # 测试代码
    print("="*60)
    print("FBA分析模块测试")
    print("="*60)
    
    # 检查数据文件
    data_path = "../data/iJO1366.xml"
    if not os.path.exists(data_path):
        print(f"✗ 请先下载数据文件：{data_path}")
        print("  下载地址：https://bigg.ucsd.edu/models/iJO1366")
    else:
        # 加载模型
        model = load_metabolic_model(data_path)
        
        if model:
            # 运行FBA
            solution, non_zero_flux = run_fba_analysis(model)
            
            if solution is not None:
                # 导出结果
                export_results(non_zero_flux, "../results/non_zero_flux_results.csv")
                
                # 显示前10个反应
                top10 = get_top_reactions(non_zero_flux, 10)
                if top10 is not None:
                    print("\n" + "="*60)
                    print("通量绝对值前10的反应：")
                    print("="*60)
                    print(top10[["reaction_id", "flux_value", "reaction_name"]].to_string(index=False))