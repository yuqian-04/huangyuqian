# 导入必要的库
# streamlit 用于创建网页应用，pandas 用于数据处理
import streamlit as st
import pandas as pd

# 设置页面配置：标题、图标、布局居中显示
st.set_page_config(
    page_title="学生作业进度档案",  # 页面标题，显示在浏览器标签页上
    page_icon="📚",  # 页面图标，用书本emoji表示
    layout="centered"  # 页面布局设置为居中
)

# 主标题：使用emoji和文字展示应用名称
st.title("📚 学生作业进度档案")

# === 一、基础信息模块 ===
# 用header函数显示"基础信息"作为二级标题
st.header("👤 基础信息")

# 创建4个等宽的列来展示基本信息
# 每个列显示一个信息项
col1, col2, col3, col4 = st.columns(4)

# 在第一列显示学生ID
with col1:
    st.write("**学生ID**")  # 加粗显示标签
    st.write("S2025-78945")  # 显示具体的学生ID

# 在第二列显示姓名
with col2:
    st.write("**姓名**")
    st.write("陆星辰")  # 显示学生姓名

# 在第三列显示所在班级
with col3:
    st.write("**所在班级**")
    st.write("22高本信管1班")  # 显示班级信息

# 在第四列显示学期信息
with col4:
    st.write("**学期**")
    st.write("2025-2026学年上学期")  # 显示当前学期

# 显示档案更新时间，包含同步状态
st.write("**档案更新时间:** 2025-12-11 16:48:00 | ✅ 已同步至教务系统")

# === 二、作业统计 ===
# 显示"本学期作业统计"作为二级标题
st.header("📊 本学期作业统计")

# 创建3个等宽的列来展示作业统计数据
col_stat1, col_stat2, col_stat3 = st.columns(3)

# 第一列显示作业总数量
with col_stat1:
    # 使用metric组件显示作业总数，包含变化值
    st.metric("作业总数量", "42", "+3 本周新增")

# 第二列显示已完成作业数量
with col_stat2:
    # 显示已完成作业数和完成比例
    st.metric("已完成作业", "35", "83.3%")

# 第三列显示待完成作业数量
with col_stat3:
    # 显示待完成作业数和本周需要完成的数量
    st.metric("待完成作业", "7", "本周需完成:3")

# === 三、作业能力矩阵 ===
# 显示"作业能力矩阵"作为二级标题
st.header("🔧 作业能力矩阵")

# 显示编程类作业的标签
st.write("**💻 编程类作业**")

# 创建3个列来展示编程类作业的各项指标
col_prog1, col_prog2, col_prog3 = st.columns(3)

# 第一列显示编程类作业的完成度
with col_prog1:
    # metric显示完成百分比和变化趋势
    st.metric("完成度", "92%", "+3%")

# 第二列显示编程类作业的平均得分
with col_prog2:
    # 显示平均分和评价等级
    st.metric("平均得分", "88分", "良好")

# 第三列显示编程类作业的进度条
with col_prog3:
    # 用进度条直观展示完成进度
    st.progress(0.92)

# 显示理论类作业的标签
st.write("**📚 理论类作业**")

# 创建3个列来展示理论类作业的各项指标
col_theory1, col_theory2, col_theory3 = st.columns(3)

# 第一列显示理论类作业的完成度
with col_theory1:
    st.metric("完成度", "85%", "-2%")  # 显示完成度和下降趋势

# 第二列显示理论类作业的得分率
with col_theory2:
    st.metric("得分率", "82%", "中等")  # 显示得分率和评价

# 第三列显示理论类作业的进度条
with col_theory3:
    st.progress(0.85)  # 进度条显示85%完成度

# 显示实践类作业的标签
st.write("**🔬 实践类作业**")

# 创建3个列来展示实践类作业的各项指标
col_prac1, col_prac2, col_prac3 = st.columns(3)

# 第一列显示实践类作业的完成度
with col_prac1:
    st.metric("完成度", "78%", "+5%")  # 显示完成度和上升趋势

# 第二列显示实践类作业的好评率
with col_prac2:
    st.metric("好评率", "90%", "优秀")  # 显示好评率和评价

# 第三列显示实践类作业的进度条
with col_prac3:
    st.progress(0.78)  # 进度条显示78%完成度

# === 四、作业进度日志 ===
# 显示"作业进度日志"作为二级标题
st.header("📋 作业进度日志")

# 创建作业数据的字典，包含5个作业的信息
# 每列对应一个数据字段：日期、作业名称、状态、得分、截止日期
assignment_data = {
    "日期": ["2025-12-01", "2025-12-05", "2025-12-08", "2025-12-10", "2025-12-15"],
    "作业名称": ["Python数据可视化作业", "高数第五章习题", "数据库系统设计报告", "机器学习实验一", "Java课程设计"],
    "状态": ["✅ 已完成", "✅ 已完成", "🔄 进行中", "⏰ 未提交", "🔄 进行中"],
    "得分": ["92", "85", "待批改", "待提交", "待批改"],
    "截止日期": ["2025-12-10 (已提交)", "2025-12-08 (准时)", "2025-12-20 (剩余9天)", "2025-12-12 (剩余1天)", "2025-12-25 (剩余14天)"]
}

# 将字典数据转换为pandas的DataFrame格式，便于表格显示
assignment_df = pd.DataFrame(assignment_data)

# 使用dataframe组件显示表格，比table组件有更好的交互性
# 可以直接显示DataFrame，无需额外设置
st.dataframe(assignment_df)

# === 五、近期作业成果 ===
# 显示"近期作业成果展示"作为二级标题
st.header("💡 近期作业成果展示")

# 创建一个简单的Python代码示例，展示学生的作业代码
# 这是一个分析学生成绩的简单函数
python_code = '''# Python数据可视化作业
# 导入必要的库：pandas用于数据处理，matplotlib用于绘图
import pandas as pd
import matplotlib.pyplot as plt

# 定义分析成绩的函数
def analyze_scores(scores):
    # 计算平均分：总分除以人数
    avg = sum(scores) / len(scores)
    # 找出最高分
    max_score = max(scores)
    # 找出最低分
    min_score = min(scores)
    # 返回三个计算结果
    return avg, max_score, min_score

# 示例数据：5个学生的成绩
student_scores = [88, 92, 76, 95, 85]

# 调用函数分析成绩
avg_score, max_score, min_score = analyze_scores(student_scores)

# 打印分析结果，平均分保留1位小数
print(f"平均分: {avg_score:.1f}")
print(f"最高分: {max_score}")
print(f"最低分: {min_score}")'''

# 使用code组件显示代码，设置语言为python以便语法高亮
st.code(python_code, language='python')

# 显示作业点评部分
st.write("**📝 作业点评**")

# 显示作业评分和等级
st.write("**评分：92分（优秀）**")

# 显示作业的优点
st.write("**优点：** 代码结构清晰，逻辑完整")

# 显示改进建议
st.write("**改进建议：** 可增加更多分析维度")

# === 六、系统提示 ===
# 显示"系统提示"作为二级标题
st.header("🔔 系统提示")

# 使用info组件显示重要的作业提醒，会有蓝色背景
st.info("⚠️ **作业提交提醒** 下一份作业 '数据库实验报告' 将于 3 天后截止")

# 显示系统状态信息
st.write("**当前档案版本：** V1.0")  # 显示系统版本
st.write("**数据来源：** 个人作业记录")  # 显示数据来源
st.write("**最后更新：** 2025-12-11 17:30:00")  # 显示最后更新时间