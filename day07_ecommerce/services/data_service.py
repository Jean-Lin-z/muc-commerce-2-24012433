from pathlib import Path
import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def load_dashboard_data(base_dir: Path, selected_category: str = "全部") -> dict:
    data_dir = base_dir / "data"
    metrics_df = _read_csv(data_dir / "overall_metrics.csv")
    category_df = _read_csv(data_dir / "category_analysis.csv")
    segment_df = _read_csv(data_dir / "segment_analysis.csv")

    metric_map = dict(zip(metrics_df["指标"], metrics_df["数值"]))

    # ===================== TODO 2-1 完成：4张指标卡 =====================
    total_user = int(metric_map["用户数"])
    churn_user = int(metric_map["流失人数"])
    total_churn_rate = churn_user / total_user
    avg_order_val = float(metric_map["平均订单数"])

    metrics = [
        {"label": "总用户数", "value": f"{int(metric_map['用户数']):,}", "note": "人"},
        {"label": "流失用户", "value": f"{int(metric_map['流失人数']):,}", "note": "人"},
        {"label": "总体流失率", "value": f"{total_churn_rate:.1%}", "note": ""},
        {"label": "平均订单数", "value": f"{avg_order_val:.2f}", "note": "单/人"},
    ]

    # 注意：CSV列名为 PreferedOrderCat（少一个r）
    categories = ["全部", *category_df["PreferedOrderCat"].tolist()]
    table_df = category_df.copy()

    # ===================== TODO 3-1 完成：按选中品类筛选 =====================
    if selected_category != "全部":
        table_df = table_df[table_df["PreferedOrderCat"] == selected_category]

    table_df = table_df.rename(
        columns={
            "PreferedOrderCat": "偏好品类",
            "用户数": "用户数",
            "流失率": "流失率",
            "平均订单数": "平均订单数",
        }
    )[["偏好品类", "用户数", "流失率", "平均订单数"]]

    table_df["流失率"] = table_df["流失率"].map(lambda value: f"{value:.1%}")
    table_df["平均订单数"] = table_df["平均订单数"].map(lambda value: f"{value:.2f}")

    # ===================== TODO 2-2 完成：流失最高生命周期观察 =====================
    max_churn_row = segment_df.loc[segment_df["流失率"].idxmax()]
    stage_name = max_churn_row["TenureGroup"]
    stage_churn_rate = max_churn_row["流失率"]
    insight = f"生命周期流失风险最高阶段为【{stage_name}】，流失率高达{stage_churn_rate:.1%}，需要针对新用户做留存运营。"

    return {
        "metrics": metrics,
        "categories": categories,
        "category_rows": table_df.to_dict("records"),
        "insight": insight,
    }
