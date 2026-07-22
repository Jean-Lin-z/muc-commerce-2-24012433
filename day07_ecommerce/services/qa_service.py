from pathlib import Path
import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    # 1. 总体用户规模
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有 {int(metric_map['用户数']):,} 名用户。"

    # ===================== TODO 4-1 完成：4类问答 =====================

    # 2. 流失情况
    if any(word in normalized for word in ["流失率", "流失人数", "流失多少"]):
        total = int(metric_map["用户数"])
        churn = int(metric_map["流失人数"])
        rate = churn / total
        return f"总流失人数为{churn:,}人，总体流失率{rate:.1%}。"

    # 3. 偏好品类
    if any(word in normalized for word in ["哪个品类用户最多", "偏好品类", "品类用户"]):
        top_cat = category_df.loc[category_df["用户数"].idxmax()]
        cat_name = top_cat["PreferedOrderCat"]
        cat_user = int(top_cat["用户数"])
        return f"用户最多的偏好品类是【{cat_name}】，拥有{cat_user:,}名用户。"

    # 4. 生命周期流失风险
    if any(word in normalized for word in ["风险最高", "生命周期", "哪个阶段流失"]):
        max_seg = segment_df.loc[segment_df["流失率"].idxmax()]
        seg_name = max_seg["TenureGroup"]
        seg_rate = max_seg["流失率"]
        return f"流失风险最高的生命周期阶段是【{seg_name}】，流失率{seg_rate:.1%}。"

    # 5. 订单情况
    if any(word in normalized for word in ["平均订单", "订单数", "人均订单"]):
        avg_val = float(metric_map["平均订单数"])
        return f"用户平均订单数均值为{avg_val:.2f}。"

    return (
        "当前仅支持以下5类数据问题：\n"
        "1. 总体用户规模（总共有多少用户）\n"
        "2. 用户流失情况（总体流失率、流失人数）\n"
        "3. 偏好品类分布（哪个品类用户最多）\n"
        "4. 生命周期流失风险（哪个阶段流失最高）\n"
        "5. 平均订单数量（人均订单数）\n"
        "请更换更贴合数据集的提问。"
    )
