# final_app.py
"""
Streamlit销售数据分析仪表板应用
功能：读取Excel销售数据，提供交互式筛选，展示关键指标和可视化图表
"""

import pandas as pd
import streamlit as st
import plotly.express as px


def get_dataframe_from_excel():
    """
    从Excel文件读取销售数据并返回Pandas DataFrame
    
    步骤：
    1. 读取指定Excel文件的特定工作表
    2. 处理时间列提取小时信息
    3. 返回处理后的数据框
    
    返回：
        DataFrame: 包含销售数据的数据框
    """
    # pd.read_excel()函数用于读取Excel文件的数据
    # 'supermarket_sales.xlsx'表示Excel文件的路径及名称
    # sheet_name='销售数据'表示读取名为"销售数据"的工作表的数据
    # skiprows=1表示跳过Excel中的第1行（通常是标题行或说明行）
    # index_col='订单号'表示将"订单号"这一列设置为数据框的索引（行标签）
    df = pd.read_excel(
        'supermarket_sales.xlsx',
        sheet_name='销售数据',
        skiprows=1,
        index_col='订单号'
    )
    
    # 处理时间列：从完整时间字符串中提取小时数
    # df['时间']取出原有的'时间'列，包含完整时间字符串（如'10:25:30'）
    # pd.to_datetime()将'时间'列转换为datetime数据类型
    # format="%H:%M:%S"指定原始时间字符串的格式（小时:分钟:秒）
    # .dt.hour从转换后的datetime对象中提取小时部分
    # 将提取的小时数赋值给新列'小时数'
    df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
    
    return df  # 返回处理后的数据框


def add_sidebar_func(df):
    """
    创建侧边栏筛选器，允许用户交互式筛选数据
    
    参数：
        df: 从Excel读取的原始数据框
    
    返回：
        DataFrame: 根据用户筛选条件过滤后的数据框
    
    筛选逻辑：
        - 用户可以选择一个或多个城市、顾客类型、性别
        - 如果用户取消所有选择，系统会自动选择全部选项（展示所有数据）
        - 使用Streamlit的multiselect组件提供多选功能
    """
    with st.sidebar:  # 创建侧边栏容器
        st.header("请筛选数据：")  # 侧边栏标题
        
        # 城市筛选器
        # 获取数据框中所有不重复的城市列表
        city_options = df["城市"].unique().tolist()
        # 创建多选下拉框，允许用户选择多个城市
        # options: 下拉框中可选的选项列表
        # default: 默认选中的选项（初始状态选择所有城市）
        # key: 组件的唯一标识符，用于状态管理
        city = st.multiselect(
            "请选择城市：",
            options=city_options,
            default=city_options,  # 初始默认全选
            key="city_select"
        )
        
        # 顾客类型筛选器
        # 获取数据框中所有不重复的顾客类型列表
        customer_type_options = df["顾客类型"].unique().tolist()
        customer_type = st.multiselect(
            "请选择顾客类型：",
            options=customer_type_options,
            default=customer_type_options,  # 初始默认全选
            key="customer_type_select"
        )
        
        # 性别筛选器
        # 获取数据框中所有不重复的性别列表
        gender_options = df["性别"].unique().tolist()
        gender = st.multiselect(
            "请选择性别：",
            options=gender_options,
            default=gender_options,  # 初始默认全选
            key="gender_select"
        )
    
    # ========== 核心逻辑：全取消筛选时返回全部数据 ==========
    # 当用户取消某个筛选器的所有选择时，使用所有选项作为默认值
    # 这样确保即使全取消也不会显示空白数据，而是显示全部数据
    
    # 1. 检查城市筛选器：如果用户取消了所有选择，使用全部城市选项
    city_filter = city if city else city_options
    
    # 2. 检查顾客类型筛选器：如果用户取消了所有选择，使用全部顾客类型选项
    customer_type_filter = customer_type if customer_type else customer_type_options
    
    # 3. 检查性别筛选器：如果用户取消了所有选择，使用全部性别选项
    gender_filter = gender if gender else gender_options
    
    # 4. 应用筛选条件到数据框
    # query()方法使用类似SQL的条件表达式筛选数据
    # @符号用于引用Python变量（筛选器选择的值）
    # 条件：城市在筛选范围内 AND 顾客类型在筛选范围内 AND 性别在筛选范围内
    df_selection = df.query(
        "城市 == @city_filter & 顾客类型 == @customer_type_filter & 性别 == @gender_filter"
    )
    
    return df_selection  # 返回筛选后的数据框


def product_line_chart(df):
    """
    生成按产品类型划分的销售额横向条形图
    
    参数：
        df: 筛选后的数据框
    
    返回：
        Figure: Plotly图形对象
    
    图表说明：
        - X轴：销售额（总价）
        - Y轴：产品类型
        - 条形按销售额从低到高排序
        - 横向条形图便于比较不同产品类型的销售表现
    """
    # 按产品类型分组，计算每个产品类型的总销售额
    # groupby(by=["产品类型"]): 按产品类型分组
    # [["总价"]]: 选择要聚合的列（双括号返回DataFrame，单括号返回Series）
    # .sum(): 对每个分组的总价列求和
    # .sort_values(by="总价"): 按总价从小到大排序
    sales_by_product_line = df.groupby(by=["产品类型"])[["总价"]].sum().sort_values(by="总价")
    
    # 使用Plotly Express创建条形图
    # px.bar(): 创建条形图函数
    # sales_by_product_line: 数据源
    # x="总价": 条形长度代表销售额
    # y=sales_by_product_line.index: 条形标签为产品类型（分组索引）
    # orientation="h": 创建横向条形图
    # title: 图表标题（使用HTML标签加粗）
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>"
    )
    
    return fig_product_sales  # 返回图形对象


def hour_chart(df):
    """
    生成按小时数划分的销售额纵向条形图
    
    参数：
        df: 筛选后的数据框
    
    返回：
        Figure: Plotly图形对象
    
    图表说明：
        - X轴：小时数（0-23）
        - Y轴：销售额（总价）
        - 纵向条形图展示一天中各时段的销售情况
    """
    # 按小时数分组，计算每个小时的总销售额
    # groupby(by=["小时数"]): 按小时数分组
    # [["总价"]]: 选择总价列进行聚合
    # .sum(): 对每小时的总价求和
    sales_by_hour = df.groupby(by=["小时数"])[["总价"]].sum()
    
    # 使用Plotly Express创建条形图
    # px.bar(): 创建条形图函数
    # x=sales_by_hour.index: X轴为小时数（分组索引）
    # y="总价": Y轴为销售额
    # title: 图表标题（使用HTML标签加粗）
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>"
    )
    
    return fig_hour_sales  # 返回图形对象


def main_page_demo(df):
    """
    主界面展示函数，显示关键指标和可视化图表
    
    参数：
        df: 筛选后的数据框
    
    功能：
        1. 显示仪表板标题
        2. 展示三个关键指标（总销售额、平均评分、平均每单销售额）
        3. 显示两个可视化图表（小时销售图、产品类型销售图）
    """
    # 显示仪表板标题
    # :bar_chart: 是Streamlit的表情符号简码，显示条形图图标
    st.title(":bar_chart: 销售仪表板")
    
    # 创建关键指标展示区域，分为三列
    # st.columns(3): 创建三个等宽的列容器
    # 每个列容器用于展示一个关键指标
    left_key_col, middle_key_col, right_key_col = st.columns(3)
    
    # 左列：总销售额
    with left_key_col:
        # 计算总销售额，处理可能的NaN值
        # df["总价"].sum(): 计算总价列的总和
        # pd.isna(): 检查结果是否为NaN（当数据为空时可能发生）
        # 如果总和是NaN，则返回0；否则转换为整数
        total_sales = int(df["总价"].sum()) if not pd.isna(df["总价"].sum()) else 0
        
        # 显示指标标题
        st.subheader("总销售额：")
        # 显示指标值，使用千位分隔符格式化数字
        # :, 在f-string中表示添加千位分隔符
        st.subheader(f"RMB ¥ {total_sales:,}")
    
    # 中列：顾客评分平均值
    with middle_key_col:
        # 计算评分的平均值
        average_rating = df["评分"].mean()
        
        # 检查平均值是否为NaN（当没有评分数据时）
        if pd.isna(average_rating):
            # 如果没有评分数据，平均值设为0，不显示星星
            average_rating = 0.0
            star_rating_string = ""
        else:
            # 有评分数据：四舍五入到一位小数
            average_rating = round(average_rating, 1)
            # 创建星星字符串：四舍五入到整数，然后乘以星星符号
            # int(round(average_rating, 0)): 将平均值四舍五入到整数
            # ":star: " * n: 重复星星符号n次
            star_rating_string = ":star: " * int(round(average_rating, 0))
        
        # 显示指标标题
        st.subheader("顾客评分的平均值：")
        # 显示指标值：平均值 + 星星符号
        st.subheader(f"{average_rating} {star_rating_string}")
    
    # 右列：每单平均销售额
    with right_key_col:
        # 计算每单平均销售额，处理可能的NaN值
        # df["总价"].mean(): 计算总价列的平均值
        # round(..., 2): 四舍五入到两位小数
        # pd.isna(): 检查结果是否为NaN
        # 如果是NaN，则返回0.0
        average_sale_by_transaction = round(df["总价"].mean(), 2) if not pd.isna(df["总价"].mean()) else 0.0
        
        # 显示指标标题
        st.subheader("每单的平均销售额：")
        # 显示指标值
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")
    
    # 添加水平分割线，分隔关键指标区和图表区
    st.divider()
    
    # 创建图表展示区域，分为两列
    # st.columns(2): 创建两个等宽的列容器
    # 左列显示小时销售图，右列显示产品类型销售图
    left_chart_col, right_chart_col = st.columns(2)
    
    # 左列：小时销售图
    with left_chart_col:
        # hour_chart(df): 调用函数生成小时销售条形图
        # st.plotly_chart(): 在Streamlit中显示Plotly图表
        # use_container_width=True: 图表宽度适应容器宽度
        st.plotly_chart(hour_chart(df), use_container_width=True)
    
    # 右列：产品类型销售图
    with right_chart_col:
        # product_line_chart(df): 调用函数生成产品类型销售条形图
        st.plotly_chart(product_line_chart(df), use_container_width=True)


def run_app():
    """
    应用主函数，初始化并运行Streamlit应用
    
    步骤：
    1. 配置页面设置
    2. 读取Excel数据
    3. 添加侧边栏筛选器
    4. 显示主界面
    """
    # 配置Streamlit页面设置
    # st.set_page_config(): 设置页面全局配置
    # page_title: 浏览器标签页标题
    # page_icon: 浏览器标签页图标（:bar_chart: 显示条形图图标）
    # layout="wide": 使用宽屏布局，最大化利用水平空间
    st.set_page_config(
        page_title="销售仪表板",
        page_icon=":bar_chart:",
        layout="wide"
    )
    
    # 从Excel文件读取销售数据
    sale_df = get_dataframe_from_excel()
    
    # 添加侧边栏筛选器，获取用户筛选后的数据
    df_selection = add_sidebar_func(sale_df)
    
    # 显示主界面，展示关键指标和图表
    main_page_demo(df_selection)


# Python程序入口
# 当直接运行此脚本时，执行run_app()函数
if __name__ == "__main__":
    run_app()
