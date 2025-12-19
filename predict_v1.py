import streamlit as st
import pickle
import pandas as pd


# 设置页面的标题、图标和布局
st.set_page_config(
    page_title="企鹅分类器",  # 页面标题
    page_icon="🐧",  # 页面图标（也可以用本地图片路径）
    layout="wide",
)

# 使用侧边栏实现多页面显示效果
with st.sidebar:
    # 注意：请确保"images/rigth_logo.png"路径存在（或替换为你的图片路径）
    st.image('images/rigth_logo.png', width=100)
    st.title("请选择页面")
    page = st.selectbox(
        "请选择页面", 
        ["简介页面", "预测分类页面"], 
        label_visibility='collapsed'
    )


# 简介页面
if page == "简介页面":
    st.title("企鹅分类器: penguin")
    st.header("数据集介绍")
    st.markdown("""
        帕尔默群岛企鹅数据集是用于数据探索和数据可视化的一个出色的数据集，
        也可以作为机器学习入门练习。
        该数据集是由 Gorman 等收集，并发布在一个名为 palmerpenguins 的 R 语言包，
        以对南极企鹅种类进行分类和研究。
        该数据集记录了 344 行观测数据，包含 3 个不同物种的企鹅：阿德利企鹅、巴布亚企鹅和帽带企鹅的各种信息。
    """)
    st.header("三种企鹅的卡通图像")
    # 注意：请确保"images/penguins.png"路径存在
    st.image('images/penguins.png')


# 预测分类页面
elif page == "预测分类页面":
    st.header("预测企鹅分类")
    st.markdown("""
        这个 Web 应用是基于帕尔默群岛企鹅数据集构建的模型。只需输入 6 个信息，
        就可以预测企鹅的物种，使用下面的表单开始预测吧！
    """)

    # 页面布局：3:1:2（表单:空列:图片）
    col_form, col, col_logo = st.columns([3, 1, 2])

    with col_form:
        # 用户输入表单
        with st.form('user_inputs'):
            island = st.selectbox('企鹅栖息的岛屿', options=['托尔斯岛', '比斯科群岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雄性', '雌性'])
            bill_length = st.number_input('喙的长度（毫米）', min_value=0.0)
            bill_depth = st.number_input('喙的深度（毫米）', min_value=0.0)
            flipper_length = st.number_input('翅膀的长度（毫米）', min_value=0.0)
            body_mass = st.number_input('身体质量（克）', min_value=0.0)
            submitted = st.form_submit_button('预测分类')

        # 特征编码（与训练时的独热编码对应）
        # 初始化岛屿相关变量
        island_biscoe, island_dream, island_torgerson = 0, 0, 0
        if island == '比斯科群岛':
            island_biscoe = 1
        elif island == '德里姆岛':
            island_dream = 1
        elif island == '托尔斯岛':
            island_torgerson = 1

        # 初始化性别相关变量
        sex_female, sex_male = 0, 0
        if sex == '雌性':
            sex_female = 1
        elif sex == '雄性':
            sex_male = 1

        # 构造输入数据（注意：顺序必须与训练时的features列一致）
        format_data = [
            bill_length, bill_depth, flipper_length, body_mass,
            island_biscoe, island_dream, island_torgerson,
            sex_female, sex_male
        ]


    # 加载模型和物种映射
    with open('rfc_model1.pkl', 'rb') as f:
        rfc_model = pickle.load(f)
    with open('output_uniques1.pkl', 'rb') as f:
        output_uniques = pickle.load(f)


    # 预测逻辑
    if submitted:
        # 将输入数据转换为DataFrame（与模型输入格式匹配）
        format_data_df = pd.DataFrame(
            data=[format_data],
            columns=rfc_model.feature_names_in_  # 保证列名与训练时一致
        )
        # 预测
        predict_result_code = rfc_model.predict(format_data_df)
        predict_result_species = output_uniques[predict_result_code][0]
        # 显示结果
        st.write(f"根据您输入的数据，预测该企鹅的物种名称是：**{predict_result_species}**")


    # 右侧图片显示
    with col_logo:
        if not submitted:
            st.image('images/rigth_logo.png', width=300)
        else:
            # 显示对应物种的图片（注意：图片文件名需与预测结果一致）
            st.image(f'images/{predict_result_species}.png', width=300)
