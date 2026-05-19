#!/usr/bin/env python3
"""
决策树建模分析脚本
功能: 加载数据、网格搜索超参数优化、模型训练、评估和可视化
"""

import argparse
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def load_data(input_path, target_col):
    """加载并预处理数据"""
    print(f"[INFO] Loading data from: {input_path}")

    # 根据文件扩展名选择加载方式
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    elif input_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(input_path)
    else:
        raise ValueError("Unsupported file format. Please use CSV or Excel.")

    print(f"[INFO] Data shape: {df.shape}")

    # 检查目标列是否存在
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in data. Available columns: {list(df.columns)}")

    # 分离特征和目标
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 处理缺失值
    if X.isnull().sum().sum() > 0:
        print(f"[INFO] Found {X.isnull().sum().sum()} missing values, filling with column means")
        X = X.fillna(X.mean())

    # 对分类特征进行编码
    for col in X.select_dtypes(include=['object']).columns:
        print(f"[INFO] Encoding categorical column: {col}")
        X[col] = pd.factorize(X[col])[0]

    print(f"[INFO] Feature shape: {X.shape}, Target shape: {y.shape}")

    return X, y, df


def optimize_hyperparameters(X_train, y_train, cv_folds=5, random_state=42):
    """网格搜索超参数优化"""
    print(f"[INFO] Starting grid search with {cv_folds}-fold cross validation...")

    # 定义超参数搜索空间
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [3, 5, 7, 10, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None]
    }

    # 创建基础模型
    dt = DecisionTreeClassifier(random_state=random_state)

    # 网格搜索
    grid_search = GridSearchCV(
        dt,
        param_grid,
        cv=cv_folds,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(X_train, y_train)

    print(f"[INFO] Best parameters: {grid_search.best_params_}")
    print(f"[INFO] Best cross-validation score: {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_


def train_model(X_train, y_train, best_params, random_state=42):
    """使用最优参数训练模型"""
    print("[INFO] Training final model with best parameters...")

    model = DecisionTreeClassifier(**best_params, random_state=random_state)
    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):
    """评估模型性能"""
    print("[INFO] Evaluating model...")

    # 预测
    y_pred = model.predict(X_test)

    # 计算指标
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)

    print(f"[INFO] Test Accuracy: {accuracy:.4f}")

    # 构建评估报告
    evaluation_report = {
        'accuracy': float(accuracy),
        'classification_report': report,
        'confusion_matrix': cm.tolist()
    }

    return evaluation_report, y_pred


def visualize_decision_tree(model, feature_names, class_names, output_path):
    """可视化决策树"""
    print("[INFO] Generating decision tree visualization...")

    try:
        # 使用sklearn的plot_tree
        from sklearn.tree import plot_tree

        plt.figure(figsize=(20, 12))
        plot_tree(
            model,
            feature_names=feature_names,
            class_names=class_names,
            filled=True,
            rounded=True,
            fontsize=10
        )
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"[INFO] Decision tree saved to: {output_path}")

    except Exception as e:
        print(f"[WARNING] Failed to generate decision tree visualization: {e}")


def plot_feature_importance(model, feature_names, output_path):
    """绘制特征重要性"""
    print("[INFO] Plotting feature importance...")

    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1]

    plt.figure(figsize=(10, 6))
    plt.title('Feature Importance')
    plt.bar(range(len(feature_names)), importance[indices])
    plt.xticks(range(len(feature_names)), [feature_names[i] for i in indices], rotation=45)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"[INFO] Feature importance plot saved to: {output_path}")


def save_results(model, evaluation_report, best_params, cv_score, y_pred,
                 X_test, y_test, output_dir):
    """保存所有结果"""
    print("[INFO] Saving results...")

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 保存模型
    model_path = os.path.join(output_dir, 'decision_tree_model.pkl')
    joblib.dump(model, model_path)
    print(f"[INFO] Model saved to: {model_path}")

    # 保存评估报告
    full_report = {
        'best_params': best_params,
        'cv_score': float(cv_score),
        'evaluation': evaluation_report
    }

    report_path = os.path.join(output_dir, 'evaluation_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(full_report, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Evaluation report saved to: {report_path}")

    # 保存预测结果
    predictions_df = pd.DataFrame({
        'actual': y_test,
        'predicted': y_pred
    })
    pred_path = os.path.join(output_dir, 'predictions.csv')
    predictions_df.to_csv(pred_path, index=False)
    print(f"[INFO] Predictions saved to: {pred_path}")

    return output_dir


def main():
    parser = argparse.ArgumentParser(description='Decision Tree Modeling with Grid Search')
    parser.add_argument('--input', required=True, help='Input data file (CSV or Excel)')
    parser.add_argument('--target', required=True, help='Target column name')
    parser.add_argument('--output_dir', default='./output', help='Output directory')
    parser.add_argument('--test_size', type=float, default=0.2, help='Test set ratio (default: 0.2)')
    parser.add_argument('--cv_folds', type=int, default=5, help='Cross-validation folds (default: 5)')
    parser.add_argument('--random_state', type=int, default=42, help='Random seed (default: 42)')

    args = parser.parse_args()

    try:
        # 1. 加载数据
        X, y, df = load_data(args.input, args.target)

        # 2. 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_state, stratify=y
        )
        print(f"[INFO] Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

        # 3. 网格搜索优化超参数
        best_model, best_params, cv_score = optimize_hyperparameters(
            X_train, y_train, cv_folds=args.cv_folds, random_state=args.random_state
        )

        # 4. 评估模型
        evaluation_report, y_pred = evaluate_model(best_model, X_test, y_test)

        # 5. 创建输出目录
        os.makedirs(args.output_dir, exist_ok=True)

        # 6. 可视化
        feature_names = X.columns.tolist()
        class_names = [str(cls) for cls in best_model.classes_]

        tree_path = os.path.join(args.output_dir, 'decision_tree.png')
        visualize_decision_tree(best_model, feature_names, class_names, tree_path)

        importance_path = os.path.join(args.output_dir, 'feature_importance.png')
        plot_feature_importance(best_model, feature_names, importance_path)

        # 7. 保存结果
        save_results(
            best_model, evaluation_report, best_params, cv_score,
            y_pred, X_test, y_test, args.output_dir
        )

        print("\n" + "="*60)
        print("[SUCCESS] Decision tree modeling completed successfully!")
        print(f"[INFO] All results saved to: {args.output_dir}/")
        print("="*60)

    except Exception as e:
        print(f"\n[ERROR] Modeling failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    main()
