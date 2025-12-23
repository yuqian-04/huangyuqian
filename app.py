# app.py（修改：全满显示100分版本）
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib
import os
from matplotlib.colors import LinearSegmentedColormap

# -------------------------- 全局配置 --------------------------
st.set_page_config(
    page_title="学生成绩分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# 路径配置
PROCESSED_DATA_PATH = "https://github.com/yuqian-04/huangyuqian/processed_data.csv"
MODEL_PATH = "https://github.com/yuqian-04/huangyuqian/optimized_score_model.pkl"
IMAGE_FOLDER = "images"
ZONG_IMAGE_PATH = "images\zong.png"

# -------------------------- 数据加载 --------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH, encoding='utf-8')
        df.columns = df.columns.str.strip()
        model_package = joblib.load(MODEL_PATH)
        attendance_col = model_package['attendance_col']
        
        if attendance_col not in df.columns:
            st.error(f"数据缺少出勤率列：{attendance_col}，请重新运行model.py")
            st.stop()
        
        df[attendance_col] = pd.to_numeric(df[attendance_col], errors='coerce')
        df['期末成绩是否及格'] = df['期末考试分数'] >= 60
        df = df.dropna(subset=['专业', attendance_col, '期末考试分数'])
        
        return df, attendance_col
    except Exception as e:
        st.error(f"数据加载错误：{str(e)}")
        st.stop()

df, attendance_col = load_data()

# -------------------------- 模型加载 --------------------------
@st.cache_resource
def load_model():
    try:
        model_package = joblib.load(MODEL_PATH)
        return model_package
    except Exception as e:
        st.error(f"模型加载错误：{str(e)}")
        st.stop()

model_package = load_model()

# -------------------------- 导航菜单 --------------------------
st.sidebar.title("导航")
page = st.sidebar.radio(
    "选择界面",
    ["项目介绍", "专业数据分析", "成绩预测"]
)

# -------------------------- 界面1：项目介绍 --------------------------
if page == "项目介绍":
    st.title("学生成绩分析与预测系统")
    
    col_overview, col_image = st.columns([2, 1])
    with col_overview:
        st.subheader("📋 项目概述")
        st.info("本项目是一个基于Streamlit的学生成绩分析平台，通过数据可视化和机器学习技术，帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。")
        
        st.subheader("🌟 主要特点")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("- 专业数据分析")
            st.markdown("- 各专业男女性别比例")
            st.markdown("- 各专业学习指标对比")
            st.markdown("- 各专业出勤率分析")
        with col2:
            st.markdown("- 成绩预测功能")
            st.markdown("- 机器学习模型驱动")
            st.markdown("- 个性化成绩预测")
            st.markdown("- 学习建议智能反馈")
        
        st.subheader("🎯 项目目标")
        target_cols = st.columns(3)
        with target_cols[0]:
            st.markdown("**目标一：分析影响因素**")
            st.markdown("- 识别关键学习指标")
            st.markdown("- 探索成绩相关因素")
            st.markdown("- 提供数据支持决策")
        with target_cols[1]:
            st.markdown("**目标二：可视化展示**")
            st.markdown("- 专业对比分析")
            st.markdown("- 性别分布研究")
            st.markdown("- 数据直观呈现")
        with target_cols[2]:
            st.markdown("**目标三：成绩预测**")
            st.markdown("- 机器学习模型")
            st.markdown("- 个性化预测结果")
            st.markdown("- 及时干预预警")
    
    with col_image:
        st.subheader("📊 系统示意图")
        if os.path.exists(ZONG_IMAGE_PATH):
            st.image(ZONG_IMAGE_PATH, use_container_width=True)
        else:
            st.warning(f"图片文件未找到：{ZONG_IMAGE_PATH}")
    
    st.subheader("🏗️ 技术架构")
    tech_cols = st.columns(4)
    with tech_cols[0]:
        st.markdown("### 前端框架")
        st.markdown("Streamlit")
    with tech_cols[1]:
        st.markdown("### 数据处理")
        st.markdown("Pandas")
    with tech_cols[2]:
        st.markdown("### 可视化")
        st.markdown("Matplotlib")
    with tech_cols[3]:
        st.markdown("### 机器学习")
        st.markdown("Scikit-learn")

# -------------------------- 界面2：专业数据分析 --------------------------
elif page == "专业数据分析":
    st.title("专业数据分析")
    
    # 各专业男女性别比例
    st.subheader("1. 各专业男女性别比例")
    col_chart1, col_table1 = st.columns([2, 1])
    with col_chart1:
        gender_count = df.groupby(['专业', '性别']).size().unstack(fill_value=0)
        gender_ratio = (gender_count.div(gender_count.sum(axis=1), axis=0) * 100).round(1)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_ylim(0, 60)
        x = np.arange(len(gender_ratio.index))
        width = 0.35
        ax1.bar(x - width/2, gender_ratio['男'], width, label='男生', color='#1f77b4', alpha=0.8)
        ax1.bar(x + width/2, gender_ratio['女'], width, label='女生', color='#ffbbcc', alpha=0.8)
        ax1.set_xlabel('专业', fontsize=12)
        ax1.set_ylabel('比例（%）', fontsize=12)
        ax1.set_title('各专业男女性别比例', fontsize=14)
        ax1.set_xticks(x)
        ax1.set_xticklabels(gender_ratio.index, rotation=45, ha='right')
        ax1.legend()
        st.pyplot(fig1)
    with col_table1:
        st.markdown("**性别比例（%）**")
        gender_table = gender_ratio.reset_index()
        gender_table.columns = ['major', '女', '男']
        st.dataframe(gender_table, use_container_width=True)
    
    # 各专业学习指标对比
    st.subheader("2. 各专业学习指标对比")
    col_chart2, col_table2 = st.columns([2, 1])
    with col_chart2:
        study_metrics = df.groupby('专业').agg({
            '每周学习时长（小时）': 'mean',
            '期中考试分数': 'mean',
            '期末考试分数': 'mean'
        }).round(1)
        fig2, ax2_1 = plt.subplots(figsize=(10, 6))
        x = np.arange(len(study_metrics.index))
        bars = ax2_1.bar(x, study_metrics['每周学习时长（小时）'], color='#1f77b4', alpha=0.8)
        ax2_1.set_xlabel('专业', fontsize=12)
        ax2_1.set_ylabel('学习时间（小时）', fontsize=12, color='#1f77b4')
        ax2_1.tick_params(axis='y', labelcolor='#1f77b4')
        ax2_2 = ax2_1.twinx()
        line1, = ax2_2.plot(x, study_metrics['期中考试分数'], marker='o', color='#ffaa00', linewidth=2)
        line2, = ax2_2.plot(x, study_metrics['期末考试分数'], marker='s', color='#2ca02c', linewidth=2)
        ax2_2.set_ylabel('分数（分）', fontsize=12, color='#333')
        ax2_2.tick_params(axis='y', labelcolor='#333')
        ax2_1.legend([bars, line1, line2], 
                    ['平均学习时间', '期中成绩', '期末成绩'],
                    loc='upper center', 
                    bbox_to_anchor=(0.5, 1.15),
                    ncol=3, 
                    fontsize=11,
                    frameon=False)
        ax2_1.set_title('各专业学习时间与成绩对比', fontsize=14)
        ax2_1.set_xticks(x)
        ax2_1.set_xticklabels(study_metrics.index, rotation=45, ha='right')
        st.pyplot(fig2)
    with col_table2:
        st.markdown("**学习指标详情**")
        study_table = study_metrics.reset_index()
        study_table.columns = ['专业', '平均学习时间（小时）', '期中平均分（分）', '期末平均分（分）']
        st.dataframe(study_table, use_container_width=True)
    
    # 各专业出勤率分析
    st.subheader("3. 各专业出勤率分析")
    col_chart3, col_table3 = st.columns([2, 1])
    with col_chart3:
        attendance_by_major = df.groupby('专业')[attendance_col].mean()
        attendance_percent = attendance_by_major * 100
        majors = attendance_percent.index.tolist()
        attendance_values = [int(value * 100) / 100.0 for value in attendance_percent]
        
        fig3, (ax3_1, ax3_2) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [10, 1]})
        x_positions = range(len(majors))
        bars = ax3_1.bar(x_positions, attendance_values, color='#4CAF50', alpha=0.7, edgecolor='#2E7D32', width=0.6)
        ax3_1.set_ylim(0, 100)
        ax3_1.set_xlabel('专业', fontsize=12)
        ax3_1.set_ylabel('平均出勤率（%）', fontsize=12)
        ax3_1.set_title('各专业平均出勤率', fontsize=14)
        ax3_1.set_xticks(x_positions)
        ax3_1.set_xticklabels(majors, rotation=45, ha='right')
        ax3_1.grid(axis='y', alpha=0.3)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax3_1.text(bar.get_x() + bar.get_width()/2, height + 0.5, f"{attendance_values[i]:.2f}%",
                      ha='center', va='bottom', fontsize=9)
        
        colors = ['#9C27B0', '#2196F3', '#4CAF50', '#FFC107']
        cmap = LinearSegmentedColormap.from_list('attendance_cmap', colors, N=100)
        gradient_bar = np.linspace(0, 100, 100).reshape(1, 100)
        ax3_2.imshow(gradient_bar, aspect='auto', cmap=cmap, extent=[0, 100, 0, 1])
        ax3_2.set_xlim(0, 100)
        ax3_2.set_xticks([0, 20, 40, 60, 80, 100])
        ax3_2.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
        ax3_2.set_yticks([])
        ax3_2.set_xlabel('出勤率值', fontsize=9)
        ax3_2.set_title('出勤程度参考（紫=低，黄=高）', fontsize=10, pad=10)
        ax3_2.spines['top'].set_visible(False)
        ax3_2.spines['right'].set_visible(False)
        ax3_2.spines['bottom'].set_visible(True)
        ax3_2.spines['left'].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig3)
    
    with col_table3:
        st.markdown("**专业出勤率排名**")
        ranking_df = pd.DataFrame({'专业': majors, '平均出勤率': attendance_values})
        ranking_df = ranking_df.sort_values('平均出勤率', ascending=False)
        ranking_df['排名'] = range(1, len(ranking_df) + 1)
        ranking_df['平均出勤率'] = ranking_df['平均出勤率'].apply(lambda x: f"{x:.2f}%")
        ranking_df = ranking_df[['排名', '专业', '平均出勤率']]
        st.dataframe(ranking_df, use_container_width=True)
    
    # 大数据管理专业专项分析
    st.subheader("4. 大数据管理专业专项分析")
    bigdata_df = df[df['专业'] == '大数据管理'].dropna(subset=['期末考试分数'])
    if bigdata_df.empty:
        st.warning("未找到'大数据管理'专业数据")
    else:
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        avg_att = int(bigdata_df[attendance_col].mean() * 10000) / 100.0
        avg_final = bigdata_df['期末考试分数'].mean().round(1)
        pass_rate = (bigdata_df['期末成绩是否及格']).sum() / len(bigdata_df) * 100
        avg_study = bigdata_df['每周学习时长（小时）'].mean().round(1)
        
        col_metric1.metric("平均出勤率", f"{avg_att:.2f}%")
        col_metric2.metric("平均期末成绩", f"{avg_final}分")
        col_metric3.metric("及格率", f"{pass_rate:.1f}%")
        col_metric4.metric("平均学习时间", f"{avg_study}小时")
        
        col_chart4_1, col_chart4_2 = st.columns(2)
        with col_chart4_1:
            fig4_1, ax4_1 = plt.subplots(figsize=(8, 6))
            bins = np.arange(60, 105, 5)
            ax4_1.hist(bigdata_df['期末考试分数'], bins=bins, color='#98FB98', alpha=0.7, edgecolor='#32CD32')
            ax4_1.set_xlabel('期末成绩（分）', fontsize=12)
            ax4_1.set_ylabel('人数', fontsize=12)
            ax4_1.set_title('期末成绩分布图（60-100分）', fontsize=14)
            ax4_1.set_xticks(bins)
            ax4_1.grid(axis='y', alpha=0.3)
            st.pyplot(fig4_1)
        
        with col_chart4_2:
            fig4_2, ax4_2 = plt.subplots(figsize=(8, 6))
            box_data = bigdata_df['期末考试分数'].values
            boxplot = ax4_2.boxplot([box_data], labels=['大数据管理专业'], patch_artist=True,
                                   showmeans=True, meanline=True, showfliers=True, widths=0.6)
            
            for box in boxplot['boxes']:
                box.set(facecolor='#87CEEB', alpha=0.7, linewidth=2)
                box.set_edgecolor('#1E90FF')
            for median in boxplot['medians']:
                median.set(color='#FF4500', linewidth=3)
            for whisker in boxplot['whiskers']:
                whisker.set(color='#1E90FF', linewidth=2)
            for cap in boxplot['caps']:
                cap.set(color='#1E90FF', linewidth=2)
            for mean in boxplot['means']:
                mean.set(color='#32CD32', linewidth=2, linestyle='--')
            for flier in boxplot['fliers']:
                flier.set(marker='o', color='#FF6347', alpha=0.7, markersize=6)
            
            ax4_2.set_ylim(50, 100)
            ax4_2.set_ylabel('期末成绩（分）', fontsize=12)
            ax4_2.set_title('大数据管理专业期末成绩箱线图', fontsize=14)
            ax4_2.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig4_2)

# -------------------------- 界面3：成绩预测（修改：全满显示100分） --------------------------
elif page == "成绩预测":
    st.title("期末成绩预测")
    
    # 提取模型组件
    model = model_package['model']
    scaler = model_package['scaler']
    selected_features = model_package['selected_features']
    gender_map = model_package['gender_map']
    major_encoder = model_package['major_encoder']
    
    # 初始化session state
    if 'prediction_made' not in st.session_state:
        st.session_state.prediction_made = False
    
    # 用户输入表单
    with st.form("prediction_form"):
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📋 基础信息")
            student_id = st.text_input("学号 *", placeholder="请输入学号", help="请输入学生的唯一学号标识")
            gender = st.selectbox("性别 *", list(gender_map.keys()))
            major = st.selectbox("专业 *", list(major_encoder.keys()))
        
        with col_right:
            st.subheader("📊 学习数据")
            
            # 每周学习时长（小时）- 0.1小时步长
            study_hours = st.slider(
                "每周学习时长（小时）",
                min_value=0.0,
                max_value=80.0,
                value=25.0,
                step=0.1,
                format="%.1f"
            )
            
            # 期中考试分数（分）- 0.1分步长
            midterm_score = st.slider(
                "期中考试分数（分）",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.1,
                format="%.1f"
            )
            
            # 上课出勤率（%）- 0.001%步长
            attendance_rate = st.slider(
                "上课出勤率（%）",
                min_value=0.000,
                max_value=100.000,
                value=90.000,
                step=0.001,
                format="%.3f"
            )
            
            # 作业完成率（%）- 0.001%步长
            homework_rate = st.slider(
                "作业完成率（%）",
                min_value=0.000,
                max_value=100.000,
                value=85.000,
                step=0.001,
                format="%.3f"
            )
        
        # 预测按钮
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            submit_btn = st.form_submit_button("🚀 预测期末成绩", use_container_width=True)
    
    # 预测逻辑
    if submit_btn:
        try:
            if not student_id.strip():
                st.warning("⚠️ 请先填写学号！")
                st.stop()
            
            # 构建输入数据
            input_data = {
                '性别_编码': gender_map[gender],
                '专业_编码': major_encoder[major],
                '每周学习时长（小时）': study_hours,
                attendance_col: attendance_rate,
                '期中考试分数': midterm_score,
                '作业完成率': homework_rate
            }
            
            # 检查是否所有指标都达到最大值
            all_max = (
                study_hours == 80.0 and  # 学习时长最大值
                midterm_score == 100.0 and  # 期中分数最大值
                attendance_rate == 100.000 and  # 出勤率最大值
                homework_rate == 100.000  # 作业完成率最大值
            )
            
            if all_max:
                # 如果所有指标都拉满，直接显示100分
                pred_score = 100.00
            else:
                # 按特征顺序整理输入
                input_features = [input_data[feat] for feat in selected_features]
                input_scaled = scaler.transform([input_features])
                
                # 预测
                pred_score = model.predict(input_scaled)[0]
                
                # 增强出勤率和作业完成率的影响（提高灵敏度）
                # 出勤率每1%增加0.8分，作业完成率每1%增加0.6分
                if attendance_col in input_data:
                    attendance_effect = (input_data[attendance_col] - 70) * 0.008
                    pred_score += attendance_effect
                
                if '作业完成率' in input_data:
                    homework_effect = (input_data['作业完成率'] - 70) * 0.006
                    pred_score += homework_effect
                
                # 确保分数在合理范围内
                pred_score = max(0.0, min(pred_score, 100.0))
            
            # 截断到小数点后两位，不四舍五入
            pred_score = float(pred_score)
            pred_score = int(pred_score * 100) / 100.0
            
            # 保存到session state
            st.session_state.prediction_made = True
            st.session_state.pred_score = pred_score
            st.session_state.student_id = student_id
            st.session_state.study_hours = study_hours
            st.session_state.midterm_score = midterm_score
            st.session_state.attendance_rate = attendance_rate
            st.session_state.homework_rate = homework_rate
            st.session_state.all_max = all_max  # 保存是否全满的状态
            
        except Exception as e:
            st.error(f"❌ 预测错误：{str(e)}")
    
    # 显示预测结果
    if st.session_state.prediction_made:
        st.header("🎯 预测结果")
        
        pred_score = st.session_state.pred_score
        all_max = st.session_state.all_max
        
        # 显示预测成绩
        st.markdown("### 预测期末成绩")
        
        # 使用Streamlit原生组件显示成绩
        if pred_score == 100.00:
            if all_max:
                st.success(f"💯 满分：{pred_score:.2f} 分（所有指标达到最优）")
            else:
                st.success(f"💯 满分：{pred_score:.2f} 分")
        elif pred_score >= 95:
            st.success(f"🏆 卓越：{pred_score:.2f} 分")
        elif pred_score >= 85:
            st.success(f"⭐ 优秀：{pred_score:.2f} 分")
        elif pred_score >= 75:
            st.info(f"📈 良好：{pred_score:.2f} 分")
        elif pred_score >= 60:
            st.warning(f"✅ 及格：{pred_score:.2f} 分")
        else:
            st.error(f"⚠️ 不及格：{pred_score:.2f} 分")
        
        # 显示当前学习指标
        st.markdown("### 📊 当前学习指标")
        
        # 使用Streamlit原生列布局
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("学习时长", f"{st.session_state.study_hours:.1f}h")
        with metric_cols[1]:
            st.metric("期中分数", f"{st.session_state.midterm_score:.1f}分")
        with metric_cols[2]:
            st.metric("出勤率", f"{st.session_state.attendance_rate:.3f}%")
        with metric_cols[3]:
            st.metric("作业完成", f"{st.session_state.homework_rate:.3f}%")
        
        # 显示是否达到最优的提示
        if all_max:
            st.success("🎉 太优秀啦！")
        
       
        st.markdown("### 🎨 成绩评价")
        
        if pred_score == 100.00:  
            image_name = "manfen.png"
        elif pred_score >= 85:
            image_name = "youxiu.jpg"
        elif pred_score >= 60:
            image_name = "gangjige.jpg"
        else:
            image_name = "bujige.jpg"
        
        image_path = os.path.join(IMAGE_FOLDER, image_name)
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning(f"提示：图片文件 {image_name} 未找到")
    
    else:
        # 首次进入页面时的提示
        st.info("👆 请填写学生信息并点击【预测期末成绩】按钮开始预测")