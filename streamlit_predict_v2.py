# streamlit_predict_v2.py (修复版)
import streamlit as st
import pickle
import pandas as pd

def introduce_page():
    """当选择简介页面时，将呈现该函数的内容"""
    st.write("# 欢迎使用！")
    st.sidebar.success("单击 🚀 预测医疗费用")
    st.markdown("""
    # 医疗费用预测应用
    这个应用利用机器学习模型来预测医疗费用，为保险公司的保险定价提供参考。
    
    ## 背景介绍
    - 开发目标：帮助保险公司合理定价保险产品，控制风险。
    - 模型算法：利用随机森林回归算法训练医疗费用预测模型。
    
    ## 使用指南
    - 输入准确完整的被保险人信息，可以得到更准确的费用预测。
    - 预测结果可以作为保险定价的重要参考，但需审慎决策。
    - 有任何问题欢迎联系我们的技术支持。
    
    技术支持:email: support@example.com
    """)

def predict_page():
    """当选择预测费用页面时，将呈现该函数的内容"""
    st.markdown("""
    ## 使用说明
    这个应用利用机器学习模型来预测医疗费用，为保险公司的保险定价提供参考。
    - **输入信息**：在下面输入被保险人的个人信息、疾病信息等。
    - **费用预测**：应用会预测被保险人的未来医疗费用支出。
    """)
    
    # 运用表单和表单提交按钮
    with st.form('user_inputs'):
        age = st.number_input('年龄', min_value=0, max_value=120, value=30)
        sex = st.radio('性别', options=['女性', '男性'], horizontal=True)
        bmi = st.number_input('BMI', min_value=10.0, max_value=60.0, value=25.0, format="%.1f")
        children = st.number_input('子女数量：', step=1, min_value=0, max_value=10, value=0)
        smoke = st.radio('是否吸烟', options=['否', '是'], horizontal=True)
        region = st.selectbox('区域', ('东南部', '西南部', '东北部', '西北部'))
        submitted = st.form_submit_button('预测费用')
    
    if submitted:
        try:
            # 加载模型
            with open('rfr_model.pkl', 'rb') as f:
                rfr_model = pickle.load(f)
            
            # 加载特征信息（如果存在）
            try:
                with open('model_features.pkl', 'rb') as f:
                    feature_info = pickle.load(f)
                feature_names = feature_info['feature_names']
            except FileNotFoundError:
                # 如果特征文件不存在，使用默认特征顺序
                feature_names = [
                    '年龄', 'BMI', '子女数量', 
                    '性别_女性', '性别_男性',
                    '是否吸烟_否', '是否吸烟_是',
                    '区域_东南部', '区域_西南部', '区域_东北部', '区域_西北部'
                ]
            
            # 准备特征数据
            features = {}
            
            # 数值特征
            features['年龄'] = age
            features['BMI'] = bmi
            features['子女数量'] = children
            
            # 性别独热编码
            features['性别_女性'] = 1 if sex == '女性' else 0
            features['性别_男性'] = 1 if sex == '男性' else 0
            
            # 吸烟状态独热编码
            features['是否吸烟_否'] = 1 if smoke == '否' else 0
            features['是否吸烟_是'] = 1 if smoke == '是' else 0
            
            # 区域独热编码
            features['区域_东南部'] = 1 if region == '东南部' else 0
            features['区域_西南部'] = 1 if region == '西南部' else 0
            features['区域_东北部'] = 1 if region == '东北部' else 0
            features['区域_西北部'] = 1 if region == '西北部' else 0
            
            # 创建DataFrame，确保特征顺序与训练时一致
            format_data = []
            for feature in feature_names:
                if feature in features:
                    format_data.append(features[feature])
                else:
                    format_data.append(0)  # 如果特征不存在，填充0
            
            format_data_df = pd.DataFrame([format_data], columns=feature_names)
            
            # 使用模型预测
            predict_result = rfr_model.predict(format_data_df)[0]
            
            # 显示预测结果
            st.success("### 预测结果")
            st.info(f"根据您输入的数据，预测该客户的医疗费用是：**${predict_result:,.2f}**")
            
            # 显示输入数据摘要
            with st.expander("查看输入数据详情"):
                st.write(f"- **年龄**: {age}岁")
                st.write(f"- **性别**: {sex}")
                st.write(f"- **BMI**: {bmi}")
                st.write(f"- **子女数量**: {children}人")
                st.write(f"- **吸烟状态**: {smoke}")
                st.write(f"- **居住区域**: {region}")
            
            st.markdown("---")
            st.write('技术支持:email: support@example.com')
            
        except FileNotFoundError:
            st.error("❌ **错误：未找到模型文件 'rfr_model.pkl'**")
            st.info("请先运行 `save_model.py` 生成模型文件")
        except Exception as e:
            st.error(f"❌ **预测过程中出现错误：** {str(e)}")
            st.info("请检查模型文件和输入数据格式")

# 设置页面的标题、图标
st.set_page_config(
    page_title="医疗费用预测系统",
    page_icon="🏥",
    layout="wide"
)

# 添加自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
    }
    .stButton > button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
    }
    .prediction-result {
        font-size: 1.5rem;
        color: #059669;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background-color: #D1FAE5;
        border-radius: 10px;
        border: 2px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)

# 在左侧添加侧边栏并设置单选按钮
st.sidebar.title("导航菜单")
nav = st.sidebar.radio(
    "请选择功能",
    ["🏠 应用简介", "🚀 预测医疗费用"],
    index=0
)

# 添加页脚信息
st.sidebar.markdown("---")
st.sidebar.info("""
**版本信息**  
v2.0 - 医疗费用预测系统  
© 2023 保险科技公司
""")

# 根据选择的结果，展示不同的页面
if nav == "🏠 应用简介":
    introduce_page()
else:
    predict_page()
