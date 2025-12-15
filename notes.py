import streamlit as st
from datetime import datetime
import base64
import io

# 页面配置
st.set_page_config(
    page_title="个人简历生成器",
    page_icon="📄",
    layout="wide"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 整体样式 */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 标题样式 */
    .main-title {
        text-align: center;
        font-size: 3.2rem;  /* 放大字体 */
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3498db;
    }
    
    /* 副标题样式 */
    .section-title {
        font-size: 2.4rem;  /* 放大字体 */
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-left: 1rem;
        border-left: 6px solid #3498db;
    }
    
    /* 小标题样式 */
    .subsection-title {
        font-size: 2.0rem;  /* 放大字体 */
        font-weight: bold;
        color: #3498db;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* 卡片样式 */
    .resume-card {
        background-color: white;
        border-radius: 15px;
        padding: 3rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        height: 100%;
    }
    
    /* 表单样式 */
    .form-section {
        background-color: white;
        border-radius: 15px;
        padding: 2.2rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
        margin-bottom: 2rem;
    }
    
    /* 分隔线样式 */
    .divider {
        border-top: 3px solid #e0e0e0;
        margin: 2.5rem 0;
    }
    
    /* 个人信息项样式 */
    .info-item {
        margin-bottom: 1.8rem;
        padding-bottom: 1rem;
    }
    
    .info-label {
        font-weight: bold;
        color: #7f8c8d;
        font-size: 1.6rem;  /* 放大字体 */
        margin-bottom: 0.5rem;
    }
    
    .info-value {
        color: #2c3e50;
        font-size: 2.0rem;  /* 放大字体 */
        line-height: 1.8;
    }
    
    /* 列表项样式 */
    .list-item {
        margin-bottom: 1.5rem;
        padding-left: 2rem;
        position: relative;
        font-size: 1.8rem;  /* 放大字体 */
        line-height: 1.9;
    }
    
    .list-item:before {
        content: "•";
        color: #3498db;
        font-weight: bold;
        font-size: 2.2rem;
        position: absolute;
        left: 0.5rem;
        top: 0.2rem;
    }
    
    /* 按钮样式 */
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 1rem 2.5rem;
        font-weight: bold;
        font-size: 1.5rem;  /* 放大字体 */
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #2980b9;
        color: white;
    }
    
    /* 预览区域样式 */
    .preview-section {
        padding: 2rem;
    }
    
    /* 照片样式 - 更大尺寸 */
    .photo-container {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        margin-top: 20px;
    }
    
    .photo-frame {
        width: 180px;  /* 增大宽度 */
        height: 240px; /* 增大高度 */
        border: 3px solid #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f8f9fa;
    }
    
    .photo-placeholder {
        color: #7f8c8d;
        font-size: 1.3rem;  /* 放大字体 */
        text-align: center;
        padding: 20px;
    }
    
    /* 照片预览容器 */
    .photo-preview-container {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .photo-preview-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* 主标题样式 - 保持原大小 */
    .preview-name {
        font-size: 3.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.8rem;
    }
    
    .preview-job {
        font-size: 2.0rem;
        color: #3498db;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    /* 技能标签样式 */
    .skills-tag {
        display: inline-block;
        background-color: #e8f4fc;
        color: #3498db;
        padding: 0.5rem 1.2rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 1.6rem;  /* 放大字体 */
        font-weight: 500;
        border: 1px solid #3498db;
    }
    
    /* 语言标签样式 */
    .language-tag {
        display: inline-block;
        background-color: #f0f8ff;
        color: #2c3e50;
        padding: 0.5rem 1.2rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 1.6rem;  /* 放大字体 */
        font-weight: 500;
        border: 1px solid #bdc3c7;
    }
    
    /* 表格容器 */
    .table-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    /* 响应式调整 */
    @media (max-width: 1200px) {
        .section-title {
            font-size: 2.0rem;
        }
        .info-value {
            font-size: 1.8rem;
        }
        .list-item {
            font-size: 1.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 应用标题
st.markdown('<h1 class="main-title">个人简历生成器</h1>', unsafe_allow_html=True)

# 在session state中存储数据
if 'uploaded_photo' not in st.session_state:
    st.session_state.uploaded_photo = None
if 'photo_base64' not in st.session_state:
    st.session_state.photo_base64 = None

# 创建两列布局
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">📝 个人信息表单</div>', unsafe_allow_html=True)
    
    # 个人信息输入
    name = st.text_input("姓名", placeholder="请输入您的姓名", key="name_input")
    job_title = st.text_input("职位", placeholder="请输入期望职位", key="job_input")
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        phone = st.text_input("电话", placeholder="请输入联系电话", key="phone_input")
    with col1_2:
        email = st.text_input("邮箱", placeholder="请输入电子邮箱", key="email_input")
    
    birth_date = st.date_input("出生日期", value=datetime(1995, 1, 1), key="birth_input")
    
    # 性别选择
    gender = st.radio("性别", options=["男", "女", "其他"], horizontal=True, key="gender_input")
    
    # 个人简介
    bio = st.text_area(
        "个人简介", 
        placeholder="请简要介绍您的专业背景、职业目标和个人特点...",
        height=150,
        key="bio_input"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 教育背景与技能
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">🎓 教育背景与技能</div>', unsafe_allow_html=True)
    
    education = st.selectbox(
        "学历",
        options=["高中", "大专", "本科", "硕士", "博士", "其他"],
        key="edu_input"
    )
    
    # 语言能力
    languages = st.multiselect(
        "语言能力",
        options=["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语", "其他"],
        default=["中文"],
        key="lang_input"
    )
    
    # 技能选择
    skills = st.multiselect(
        "技能（可多选）",
        options=["Python编程", "数据分析", "项目管理", "UI/UX设计", "市场营销", "财务管理", 
                "团队领导", "沟通协调", "问题解决", "创意写作", "外语翻译", "其他"],
        placeholder="请选择相关技能",
        key="skills_input"
    )
    
    # 自定义技能输入
    custom_skill = st.text_input("其他技能（如上方选项未包含）", placeholder="请输入其他技能，用逗号分隔", key="custom_skill_input")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 工作经验与期望
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">💼 工作经验与期望</div>', unsafe_allow_html=True)
    
    experience_years = st.slider("工作经验（年）", min_value=0, max_value=40, value=3, key="exp_years_input")
    
    # 期望薪资范围
    salary_min, salary_max = st.slider(
        "期望薪资范围（元）",
        min_value=3000, max_value=50000, value=(10000, 20000), step=1000,
        key="salary_input"
    )
    
    # 最佳联系时间
    contact_time = st.select_slider(
        "最佳联系时间",
        options=["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
        value="09:00",
        key="contact_time_input"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 新增部分：详细信息
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">📋 详细信息</div>', unsafe_allow_html=True)
    
    # 工作经验（详细）
    st.markdown('<div style="font-size: 1.8rem; font-weight: bold; color: #2c3e50; margin: 1.5rem 0 1rem 0;">工作经验（详细描述）</div>', unsafe_allow_html=True)
    work_experience = st.text_area(
        " ",
        placeholder="例如：\n• 2020-2023: 在XX公司担任XX职位，负责...\n• 2018-2020: 在YY公司担任YY职位，负责...",
        height=180,
        key="work_exp_input",
        label_visibility="collapsed"
    )
    
    # 奖项荣誉
    st.markdown('<div style="font-size: 1.8rem; font-weight: bold; color: #2c3e50; margin: 1.5rem 0 1rem 0;">奖项荣誉</div>', unsafe_allow_html=True)
    awards = st.text_area(
        " ",
        placeholder="例如：\n• 2022年获得优秀员工奖\n• 2021年获得行业创新奖\n• 2020年获得优秀新人奖",
        height=150,
        key="awards_input",
        label_visibility="collapsed"
    )
    
    
    
    # 自我评价
    st.markdown('<div style="font-size: 1.8rem; font-weight: bold; color: #2c3e50; margin: 1.5rem 0 1rem 0;">自我评价</div>', unsafe_allow_html=True)
    self_evaluation = st.text_area(
        " ",
        placeholder="例如：\n• 工作认真负责，有强烈的责任心\n• 学习能力强，能快速适应新环境\n• 具备良好的沟通能力和团队协作精神",
        height=150,
        key="self_eval_input",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 照片上传
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="subsection-title">📸 上传个人照片</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "请上传个人照片（支持JPG, JPEG, PNG格式）",
        type=["jpg", "jpeg", "png"],
        help="建议尺寸：180x240像素",
        key="photo_uploader"
    )
    
    if uploaded_file is not None:
        # 保存到session state
        st.session_state.uploaded_photo = uploaded_file
        # 转换为base64
        file_bytes = uploaded_file.getvalue()
        st.session_state.photo_base64 = base64.b64encode(file_bytes).decode('utf-8')
        
        # 显示预览
        st.image(file_bytes, caption="已上传的个人照片", width=250)
    
    # 清空照片按钮
    if st.session_state.uploaded_photo is not None:
        if st.button("清除照片", key="clear_photo", use_container_width=True):
            st.session_state.uploaded_photo = None
            st.session_state.photo_base64 = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="resume-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👁️ 简历实时预览</div>', unsafe_allow_html=True)
    
    # 预览区域
    st.markdown('<div class="preview-section">', unsafe_allow_html=True)
    
    # 使用两列布局：左边是姓名职位，右边是照片
    header_col1, header_col2 = st.columns([3, 1])
    
    with header_col1:
        # 姓名和职位 - 使用自定义样式（保持原大小）
        if name:
            st.markdown(f'<div class="preview-name">{name}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="preview-name">[姓名]</div>', unsafe_allow_html=True)
        
        if job_title:
            st.markdown(f'<div class="preview-job">{job_title}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="preview-job">[职位]</div>', unsafe_allow_html=True)
    
    with header_col2:
        # 照片区域 - 使用HTML容器
        if st.session_state.photo_base64:
            # 有照片时显示照片
            photo_html = f"""
            <div class="photo-container">
                <div class="photo-frame">
                    <img src="data:image/jpeg;base64,{st.session_state.photo_base64}" 
                         style="width: 100%; height: 100%; object-fit: cover;">
                </div>
            </div>
            """
        else:
            # 没有照片时显示占位符
            photo_html = """
            <div class="photo-container">
                <div class="photo-frame">
                    <div class="photo-placeholder">
                        二寸证件照<br>（请上传照片）
                    </div>
                </div>
            </div>
            """
        
        st.markdown(photo_html, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 个人信息预览
    st.markdown('<p class="section-title">个人信息</p>', unsafe_allow_html=True)
    
    # 创建个人信息网格
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown(f'<div class="info-item"><div class="info-label">电话</div><div class="info-value">{phone if phone else "未填写"}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-item"><div class="info-label">邮箱</div><div class="info-value">{email if email else "未填写"}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-item"><div class="info-label">出生日期</div><div class="info-value">{birth_date.strftime("%Y/%m/%d")}</div></div>', unsafe_allow_html=True)
    
    with info_col2:
        st.markdown(f'<div class="info-item"><div class="info-label">性别</div><div class="info-value">{gender}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-item"><div class="info-label">学历</div><div class="info-value">{education}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-item"><div class="info-label">工作经验</div><div class="info-value">{experience_years}年</div></div>', unsafe_allow_html=True)
    
    # 个人简介预览
    st.markdown('<p class="section-title">个人简介</p>', unsafe_allow_html=True)
    if bio:
        st.markdown(f'<div class="info-value" style="line-height: 2.0;">{bio}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-value">这个人很神秘，没有留下任何介绍...</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 技能与语言预览
    st.markdown('<p class="section-title">技能与语言</p>', unsafe_allow_html=True)
    
    # 语言能力
    st.markdown('<div class="info-label">语言能力：</div>', unsafe_allow_html=True)
    if languages:
        lang_tags = "".join([f'<span class="language-tag">{lang}</span>' for lang in languages])
        st.markdown(f'<div style="margin-top: 0.5rem;">{lang_tags}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-value">未填写</div>', unsafe_allow_html=True)
    
    # 技能
    st.markdown('<div class="info-label" style="margin-top: 1.5rem;">技能：</div>', unsafe_allow_html=True)
    all_skills = skills.copy()
    if custom_skill:
        custom_skills = [s.strip() for s in custom_skill.split(",") if s.strip()]
        all_skills.extend(custom_skills)
    
    if all_skills:
        skill_tags = "".join([f'<span class="skills-tag">{skill}</span>' for skill in all_skills])
        st.markdown(f'<div style="margin-top: 0.5rem;">{skill_tags}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-value">未填写</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 期望薪资与联系时间
    st.markdown('<p class="section-title">期望与联系方式</p>', unsafe_allow_html=True)
    
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        st.markdown(f'<div class="info-item"><div class="info-label">期望薪资</div><div class="info-value">{salary_min:,} - {salary_max:,}元</div></div>', unsafe_allow_html=True)
    
    with exp_col2:
        st.markdown(f'<div class="info-item"><div class="info-label">最佳联系时间</div><div class="info-value">{contact_time}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 新增部分：工作经验（详细）
    st.markdown('<p class="section-title">工作经验</p>', unsafe_allow_html=True)
    if work_experience:
        # 将文本按行分割，每行前面添加圆点
        lines = work_experience.strip().split('\n')
        for line in lines:
            if line.strip():
                st.markdown(f'<div class="list-item">{line.strip()}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-value">暂无详细工作经验描述</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # 新增部分：奖项荣誉
    st.markdown('<p class="section-title">奖项荣誉</p>', unsafe_allow_html=True)
    if awards:
        # 将文本按行分割，每行前面添加圆点
        lines = awards.strip().split('\n')
        for line in lines:
            if line.strip():
                st.markdown(f'<div class="list-item">{line.strip()}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-value">暂无奖项荣誉记录</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    
    
    # 新增部分：自我评价
    st.markdown('<p class="section-title">自我评价</p>', unsafe_allow_html=True)
    if self_evaluation:
        # 将文本按行分割，每行前面添加圆点
        lines = self_evaluation.strip().split('\n')
        for line in lines:
            if line.strip():
                st.markdown(f'<div class="list-item">{line.strip()}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-value">暂无自我评价</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # 结束preview-section
    st.markdown('</div>', unsafe_allow_html=True)  # 结束resume-card

# 底部操作按钮
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    if st.button("💾 保存简历", use_container_width=True, key="save_btn"):
        st.success("简历已保存！（此处为演示功能）")

with col_btn2:
    if st.button("🖨️ 打印简历", use_container_width=True, key="print_btn"):
        st.info("打印功能已准备就绪！（此处为演示功能）")

with col_btn3:
    if st.button("📧 发送简历", use_container_width=True, key="send_btn"):
        st.success("简历发送功能已准备就绪！（此处为演示功能）")

# 底部说明
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #7f8c8d; font-size: 1.4rem; margin-top: 3rem; padding: 1.5rem; background-color: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <p style="font-size: 1.6rem; font-weight: 600; color: #2c3e50;">个人简历生成器 &copy; 2025</p>
        <p style="margin: 1rem 0; font-size: 1.5rem;">在左侧表单填写信息，右侧实时预览简历</p>
        <p style="color: #e74c3c; font-weight: 500; font-size: 1.4rem;">注意：本应用不会存储您的任何个人信息，所有数据仅在当前会话中有效</p>
    </div>
    """, 
    unsafe_allow_html=True
)
