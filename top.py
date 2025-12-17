import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import base64

st.set_page_config(
    page_title="功能合集",
    page_icon="💠",
    layout="wide"
)

st.title("功能大合集")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["美食调查", "数字档案", "我的相册", "音乐播放", "视频网站", "个人简历生成器"])

with tab1:
    st.header("美食调查")
    st.markdown("#### 来查看各美食的热度")
    
    data = {
        "月份": ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        "餐厅": ["胖哥俩", "虾大叔", "茶炮火锅", "重庆小面", "罐老大", "胖哥俩", "虾大叔", "茶炮火锅", "重庆小面", "罐老大", "胖哥俩", "虾大叔"],
        "类型": ["中餐", "中餐", "火锅", "面食", "粉类", "中餐", "中餐", "火锅", "面食", "粉类", "中餐", "中餐"],
        "评分": [4.7, 4.6, 4.3, 4.5, 4.8, 4.7, 4.6, 4.3, 4.5, 4.8, 4.7, 4.6],
        "人均消费（元）": [32, 30, 42, 12, 20, 32, 30, 42, 12, 20, 32, 30],
    }

    df = pd.DataFrame(data)
    df.set_index('月份', inplace=True)

    st.markdown('## 📍南宁美食地图')
    map_data = {
        "latitude": [22.815767, 22.814051, 22.832171, 22.873231, 22.813471],
        "longitude": [108.321003, 108.321394, 108.292669, 108.266497, 108.318393]
    }
    mp_df = pd.DataFrame(map_data)
    st.map(mp_df)

    st.markdown('## 💯餐厅评分')
    df_reset = df.reset_index()
    rating_data = df_reset[['餐厅', '评分']]
    st.bar_chart(rating_data.set_index('餐厅'))

    st.markdown('## 💰不同类型餐厅价格')
    type_price_data = df_reset[['类型', '人均消费（元）']].groupby('类型').mean()
    st.line_chart(type_price_data)

    st.markdown('## ⏲︎用餐高峰时段')
    time_points = [f"{hour:02d}:00" for hour in range(8, 25)]
    peak_hours_data = {
        "时间": time_points,
        "胖哥俩": [40, 50, 60, 70, 80, 120, 180, 220, 180, 150, 130, 110, 90, 70, 50, 40, 30],
        "虾大叔": [30, 40, 50, 60, 70, 100, 160, 200, 160, 130, 110, 90, 70, 60, 40, 30, 20],
        "茶炮火锅": [20, 25, 30, 35, 40, 60, 100, 140, 120, 100, 80, 70, 60, 50, 40, 30, 20],
        "重庆小面": [50, 60, 70, 80, 90, 140, 200, 250, 200, 170, 150, 130, 110, 90, 70, 60, 50],
        "罐老大": [25, 30, 35, 40, 45, 70, 120, 160, 140, 120, 100, 80, 70, 60, 50, 40, 30]
    }
    peak_hours_df = pd.DataFrame(peak_hours_data)
    st.area_chart(peak_hours_df.set_index('时间'))

with tab2:
    st.header("数字档案")
    st.markdown("#### 我的数字档案")
    st.title("📚 学生作业进度档案")
    
    st.header("👤 基础信息")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("**学生ID**")
        st.write("S2025-78945")
    with col2:
        st.write("**姓名**")
        st.write("陆星辰")
    with col3:
        st.write("**所在班级**")
        st.write("22高本信管1班")
    with col4:
        st.write("**学期**")
        st.write("2025-2026学年上学期")
    
    st.write("**档案更新时间:** 2025-12-11 16:48:00 | ✅ 已同步至教务系统")
    
    st.header("📊 本学期作业统计")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("作业总数量", "42", "+3 本周新增")
    with col_stat2:
        st.metric("已完成作业", "35", "83.3%")
    with col_stat3:
        st.metric("待完成作业", "7", "本周需完成:3")

    st.header("🔧 作业能力矩阵")
    st.write("**💻 编程类作业**")
    col_prog1, col_prog2, col_prog3 = st.columns(3)
    with col_prog1:
        st.metric("完成度", "92%", "+3%")
    with col_prog2:
        st.metric("平均得分", "88分", "良好")
    with col_prog3:
        st.progress(0.92)

    st.write("**📚 理论类作业**")
    col_theory1, col_theory2, col_theory3 = st.columns(3)
    with col_theory1:
        st.metric("完成度", "85%", "-2%")
    with col_theory2:
        st.metric("得分率", "82%", "中等")
    with col_theory3:
        st.progress(0.85)

    st.write("**🔬 实践类作业**")
    col_prac1, col_prac2, col_prac3 = st.columns(3)
    with col_prac1:
        st.metric("完成度", "78%", "+5%")
    with col_prac2:
        st.metric("好评率", "90%", "优秀")
    with col_prac3:
        st.progress(0.78)

    st.header("📋 作业进度日志")
    assignment_data = {
        "日期": ["2025-12-01", "2025-12-05", "2025-12-08", "2025-12-10", "2025-12-15"],
        "作业名称": ["Python数据可视化作业", "高数第五章习题", "数据库系统设计报告", "机器学习实验一", "Java课程设计"],
        "状态": ["✅ 已完成", "✅ 已完成", "🔄 进行中", "⏰ 未提交", "🔄 进行中"],
        "得分": ["92", "85", "待批改", "待提交", "待批改"],
        "截止日期": ["2025-12-10 (已提交)", "2025-12-08 (准时)", "2025-12-20 (剩余9天)", "2025-12-12 (剩余1天)", "2025-12-25 (剩余14天)"]
    }
    assignment_df = pd.DataFrame(assignment_data)
    st.dataframe(assignment_df)

    st.header("💡 近期作业成果展示")
    python_code = '''# Python数据可视化作业
import pandas as pd
import matplotlib.pyplot as plt

def analyze_scores(scores):
    avg = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)
    return avg, max_score, min_score

student_scores = [88, 92, 76, 95, 85]
avg_score, max_score, min_score = analyze_scores(student_scores)

print(f"平均分: {avg_score:.1f}")
print(f"最高分: {max_score}")
print(f"最低分: {min_score}")'''
    st.code(python_code, language='python')
    st.write("**📝 作业点评**")
    st.write("**评分：92分（优秀）**")
    st.write("**优点：** 代码结构清晰，逻辑完整")
    st.write("**改进建议：** 可增加更多分析维度")

    st.header("🔔 系统提示")
    st.info("⚠️ **作业提交提醒** 下一份作业 '数据库实验报告' 将于 3 天后截止")
    st.write("**当前档案版本：** V1.0")
    st.write("**数据来源：** 个人作业记录")
    st.write("**最后更新：** 2025-12-11 17:30:00")

with tab3:
    st.header("相册")
    st.markdown("#### 动漫相册")
    
    if 'photo_index' not in st.session_state:
        st.session_state['photo_index'] = 0

    images = [
        {'url': "https://img-baofun.zhhainiao.com/fs/a4cdaadfb481ce7358b658f2f3de7f9c.jpg", 'text': '蜡笔小新'},
        {'url': "https://file.moyubuluo.com/d/file/2025-06-03/0176c88a7184c3a883e608a3f2e3b7a4.jpg", 'text': '疯狂动物城'},
        {'url': "http://vsd-picture.cdn.bcebos.com/5e516089e12c1fcd43d79dfaab8930a53c61766f.jpg", 'text': '风之谷'},
        {'url': "https://www.bizhigq.com/caiji-img/0495428d2e0d62f29753b9a101e11087.jpg", 'text': '千与千寻'}
    ]

    st.image(images[st.session_state['photo_index']]['url'], caption=images[st.session_state['photo_index']]['text'])

    def nextImg():
        st.session_state['photo_index'] = (st.session_state['photo_index'] + 1) % len(images)

    def prevImg():
        st.session_state['photo_index'] = (st.session_state['photo_index'] - 1) % len(images)

    c1, c2 = st.columns(2)
    with c1:
        st.button("上一张", on_click=prevImg, use_container_width=True)
    with c2:
        st.button("下一张", on_click=nextImg, use_container_width=True)

with tab4:
    st.header("音乐播放")
    st.markdown("#### 来这里放松，听听音乐")
    
    # 简化音乐播放器的CSS，避免冲突
    music_css = """
    <style>
    .music-section h3, .music-section p {
        color: white;
    }
    </style>
    """
    st.markdown(music_css, unsafe_allow_html=True)
    
    if 'music_index' not in st.session_state:
        st.session_state['music_index'] = 0

    songs = [
        {
            'url': "https://img95.699pic.com/photo/60062/6758.jpg_wh860.jpg",
            'text': "专辑封面",
            'name': "Cry For You",
            'author': 'Karry_b',
            'time': "时长：3:47",
            'audio': 'https://music.163.com/song/media/outer/url?id=3324819089.mp3'
        },
        {
            'url': "https://bpic.588ku.com/back_list_pic/22/03/17/648e220696a63adfe45c1efee071f142.jpg",
            'text': "专辑封面",
            'name': "春溯",
            'author': '二乘',
            'time': "时长:1:53",
            'audio': 'https://music.163.com/song/media/outer/url?id=3325298797.mp3'
        },
        {
            'url': "https://img95.699pic.com/photo/50003/7719.jpg_wh860.jpg",
            'text': "专辑封面",
            'name': "听海",
            'author': '张惠妹',
            'time': "时长:5:18",
            'audio': 'https://music.163.com/song/media/outer/url?id=3320620949.mp3'
        }
    ]

    current_index = st.session_state['music_index']
    current_song = songs[current_index]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(current_song['url'], caption=current_song['text'])
    with col2:
        st.markdown(f"### {current_song['name']}")
        st.markdown(f"**歌手：** {current_song['author']}")
        st.markdown(f"**{current_song['time']}**")
        
        def next_song():
            st.session_state['music_index'] = (st.session_state['music_index'] + 1) % len(songs)
        
        def prev_song():
            st.session_state['music_index'] = (st.session_state['music_index'] - 1) % len(songs)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.button("上一首", on_click=prev_song, use_container_width=True)
        with btn_col2:
            st.button("下一首", on_click=next_song, use_container_width=True)

    st.audio(current_song['audio'])

with tab5:
    st.header("视频网站")
    st.markdown("#### 来这里轻松一刻")
    
    if 'video_index' not in st.session_state:
        st.session_state['video_index'] = 0

    video_arr = [
        {
            'url': 'https://apd-e5ffce9b9f3cd1ccccc3128f3c9f7002.v.smtcdns.com/vhot2.qqvideo.tc.qq.com/AM0eTcNxNhJR1WOsI31SmKZkJ6EFSwLnjsg3KnfV6tm4/B_3k--xdVBUHYl1q0K2jODe3Czy6jN--S5qKjbKKcWhqc36DnShajnw1opCrr4ZImT980xUUCvORBKLdHtA8ctS0jkVWFGysIyz7HPgphyihA0cqxafmT-MvEkl4o_7uNVKIvFvNEedTY97p2xGmq39Q/svp_50069/gzc_1000035_0b53faaa6aaapyam2e345nujkkgdb4uaad2a.f622.mp4?vkey=320DF7C3B3DDBB8313588485AED7CBE683C7D86A1EEDACB9E0745D89B1E59C7B1A1CE184F6B034F1511189BB98A876B591D64EDB41310F98DBF49A2553A3CFAF441CB4DA13D84C715E2AC9837D9F87F90DB42C44A25B247948227F9E9D64E64352135381ABB8716DF72B1FEE032FE8880DCC962C7319B8723F1C5AF5D5DF9BA7',
            'title': '第一集',
            'text': '分身乏术'
        },
        {
            'url': 'https://www.w3schools.com/html/movie.mp4',
            'title': '第二集',
            'text': '美容院'
        },
        {
            'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4',
            'title': '第三集',
            'text': '对讲机'
        },
        {
            'url': 'https://apd-e5ffce9b9f3cd1ccccc3128f3c9f7002.v.smtcdns.com/vhot2.qqvideo.tc.qq.com/AM0eTcNxNhJR1WOsI31SmKZkJ6EFSwLnjsg3KnfV6tm4/B_3k--xdVBUHYl1q0K2jODe3Czy6jN--S5qKjbKKcWhqc36DnShajnw1opCrr4ZImT980xUUCvORBKLdHtA8ctS0jkVWFGysIyz7HPgphyihA0cqxafmT-MvEkl4o_7uNVKIvFvNEedTY97p2xGmq39Q/svp_50069/gzc_1000035_0b53faaa6aaapyam2e345nujkkgdb4uaad2a.f622.mp4?vkey=320DF7C3B3DDBB8313588485AED7CBE683C7D86A1EEDACB9E0745D89B1E59C7B1A1CE184F6B034F1511189BB98A876B591D64EDB41310F98DBF49A2553A3CFAF441CB4DA13D84C715E2AC9837D9F87F90DB42C44A25B247948227F9E9D64E64352135381ABB8716DF72B1FEE032FE8880DCC962C7319B8723F1C5AF5D5DF9BA7',
            'title': '第四集',
            'text': '电视频道'
        },
        {
            'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4',
            'title': '第五集',
            'text': '留胡子'
        }
    ]

    current_video = video_arr[st.session_state['video_index']]
    st.markdown(f"### {current_video['title']}")
    st.markdown(f"**内容简介：** {current_video['text']}")
    st.video(current_video['url'])

    def play(i):
        st.session_state['video_index'] = int(i)

    cols = st.columns(len(video_arr))
    for i in range(len(video_arr)):
        with cols[i]:
            st.button(f'第{i+1}集', use_container_width=True, on_click=play, args=([i]))

    st.markdown("### 主要角色")
    characters = [
        {'name': '蜡笔小新', 'img_url': 'https://picx.zhimg.com/v2-64e1f6f922e41e90a6e5e5f41376ae8a_720w.jpg?source=172ae18b'},
        {'name': '美伢', 'img_url': 'https://img1.fjdaily.com/app/images/2025-04/15/t0_(0X229X300X429)ed45ee05-4107-454f-890e-25e818172fc5.JPEG'},
        {'name': '野原广志', 'img_url': 'https://i.bobopic.com/small/80835859.jpg'},
        {'name': '小葵', 'img_url': 'https://pic4.zhimg.com/v2-cacb627341245b8ccf0d807a226294a5_1440w.jpg'},
        {'name': '小白', 'img_url': 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1659988190,3144626163&fm=253&gp=0.jpg'}
    ]

    char_cols = st.columns(len(characters))
    for i, char in enumerate(characters):
        with char_cols[i]:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{char['img_url']}" width="80" height="80" style="border-radius: 50%; object-fit: cover;">
                    <p style="margin-top: 5px;"><strong>{char['name']}</strong></p>
                </div>
                """,
                unsafe_allow_html=True
            )

with tab6:
    st.header("个人简历生成器")
    st.markdown("#### 生成专属于自己的一份简历")
    
    # 只保留简历生成器的CSS
    resume_css = """
    <style>
    .main-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3498db;
    }
    .resume-card {
        background-color: white;
        border-radius: 15px;
        padding: 3rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        height: 100%;
    }
    .section-title {
        font-size: 2.4rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-left: 1rem;
        border-left: 6px solid #3498db;
    }
    .subsection-title {
        font-size: 2.0rem;
        font-weight: bold;
        color: #3498db;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .form-section {
        background-color: white;
        border-radius: 15px;
        padding: 2.2rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
        margin-bottom: 2rem;
    }
    .divider {
        border-top: 3px solid #e0e0e0;
        margin: 2.5rem 0;
    }
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
    .skills-tag {
        display: inline-block;
        background-color: #e8f4fc;
        color: #3498db;
        padding: 0.5rem 1.2rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 1.6rem;
        font-weight: 500;
        border: 1px solid #3498db;
    }
    .language-tag {
        display: inline-block;
        background-color: #f0f8ff;
        color: #2c3e50;
        padding: 0.5rem 1.2rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 1.6rem;
        font-weight: 500;
        border: 1px solid #bdc3c7;
    }
    </style>
    """
    st.markdown(resume_css, unsafe_allow_html=True)
    
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
        
        name = st.text_input("姓名", placeholder="请输入您的姓名")
        job_title = st.text_input("职位", placeholder="请输入期望职位")
        
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            phone = st.text_input("电话", placeholder="请输入联系电话")
        with col1_2:
            email = st.text_input("邮箱", placeholder="请输入电子邮箱")
        
        birth_date = st.date_input("出生日期", value=datetime(1995, 1, 1))
        gender = st.radio("性别", options=["男", "女", "其他"], horizontal=True)
        bio = st.text_area("个人简介", placeholder="请简要介绍您的专业背景、职业目标和个人特点...", height=150)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">🎓 教育背景与技能</div>', unsafe_allow_html=True)
        education = st.selectbox("学历", options=["高中", "大专", "本科", "硕士", "博士", "其他"])
        languages = st.multiselect("语言能力", options=["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语", "其他"], default=["中文"])
        skills = st.multiselect("技能（可多选）", options=["Python编程", "数据分析", "项目管理", "UI/UX设计", "市场营销", "财务管理", "团队领导", "沟通协调", "问题解决", "创意写作", "外语翻译", "其他"], placeholder="请选择相关技能")
        custom_skill = st.text_input("其他技能（如上方选项未包含）", placeholder="请输入其他技能，用逗号分隔")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">💼 工作经验与期望</div>', unsafe_allow_html=True)
        experience_years = st.slider("工作经验（年）", min_value=0, max_value=40, value=3)
        salary_min, salary_max = st.slider("期望薪资范围（元）", min_value=3000, max_value=50000, value=(10000, 20000), step=1000)
        contact_time = st.select_slider("最佳联系时间", options=["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00", "18:00"], value="09:00")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">📋 详细信息</div>', unsafe_allow_html=True)
        work_experience = st.text_area("工作经验（详细描述）", placeholder="例如：\n• 2020-2023: 在XX公司担任XX职位，负责...\n• 2018-2020: 在YY公司担任YY职位，负责...", height=180)
        awards = st.text_area("奖项荣誉", placeholder="例如：\n• 2022年获得优秀员工奖\n• 2021年获得行业创新奖\n• 2020年获得优秀新人奖", height=150)
        self_evaluation = st.text_area("自我评价", placeholder="例如：\n• 工作认真负责，有强烈的责任心\n• 学习能力强，能快速适应新环境\n• 具备良好的沟通能力和团队协作精神", height=150)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-title">📸 上传个人照片</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("请上传个人照片（支持JPG, JPEG, PNG格式）", type=["jpg", "jpeg", "png"], help="建议尺寸：180x240像素")
        if uploaded_file is not None:
            st.session_state.uploaded_photo = uploaded_file
            file_bytes = uploaded_file.getvalue()
            st.session_state.photo_base64 = base64.b64encode(file_bytes).decode('utf-8')
            st.image(file_bytes, caption="已上传的个人照片", width=250)
        if st.session_state.uploaded_photo is not None:
            if st.button("清除照片", use_container_width=True):
                st.session_state.uploaded_photo = None
                st.session_state.photo_base64 = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="resume-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">👁️ 简历实时预览</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding: 2rem;">', unsafe_allow_html=True)
        
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.markdown(f'<div class="preview-name">{name if name else "[姓名]"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="preview-job">{job_title if job_title else "[职位]"}</div>', unsafe_allow_html=True)
        
        with header_col2:
            if st.session_state.photo_base64:
                photo_html = f"""
                <div style="display: flex; justify-content: flex-end; align-items: flex-start; margin-top: 20px;">
                    <div style="width: 180px; height: 240px; border: 3px solid #e0e0e0; border-radius: 10px; overflow: hidden;">
                        <img src="data:image/jpeg;base64,{st.session_state.photo_base64}" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                </div>
                """
            else:
                photo_html = """
                <div style="display: flex; justify-content: flex-end; align-items: flex-start; margin-top: 20px;">
                    <div style="width: 180px; height: 240px; border: 3px solid #e0e0e0; border-radius: 10px; background-color: #f8f9fa; display: flex; align-items: center; justify-content: center;">
                        <div style="color: #7f8c8d; text-align: center; padding: 20px; font-size: 1.3rem;">
                            二寸证件照<br>（请上传照片）
                        </div>
                    </div>
                </div>
                """
            st.markdown(photo_html, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">个人信息</p>', unsafe_allow_html=True)
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">电话</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{phone if phone else "未填写"}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">邮箱</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{email if email else "未填写"}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">出生日期</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{birth_date.strftime("%Y/%m/%d")}</div></div>', unsafe_allow_html=True)
        with info_col2:
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">性别</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{gender}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">学历</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{education}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">工作经验</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{experience_years}年</div></div>', unsafe_allow_html=True)
        
        st.markdown('<p class="section-title">个人简介</p>', unsafe_allow_html=True)
        if bio:
            st.markdown(f'<div style="color: #2c3e50; font-size: 2.0rem; line-height: 2.0;">{bio}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color: #2c3e50; font-size: 2.0rem;">这个人很神秘，没有留下任何介绍...</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">技能与语言</p>', unsafe_allow_html=True)
        st.markdown('<div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">语言能力：</div>', unsafe_allow_html=True)
        if languages:
            lang_tags = "".join([f'<span class="language-tag">{lang}</span>' for lang in languages])
            st.markdown(f'<div style="margin-top: 0.5rem;">{lang_tags}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color: #2c3e50; font-size: 2.0rem;">未填写</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem; margin-top: 1.5rem;">技能：</div>', unsafe_allow_html=True)
        all_skills = skills.copy()
        if custom_skill:
            custom_skills = [s.strip() for s in custom_skill.split(",") if s.strip()]
            all_skills.extend(custom_skills)
        if all_skills:
            skill_tags = "".join([f'<span class="skills-tag">{skill}</span>' for skill in all_skills])
            st.markdown(f'<div style="margin-top: 0.5rem;">{skill_tags}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color: #2c3e50; font-size: 2.0rem;">未填写</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">期望与联系方式</p>', unsafe_allow_html=True)
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">期望薪资</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{salary_min:,} - {salary_max:,}元</div></div>', unsafe_allow_html=True)
        with exp_col2:
            st.markdown(f'<div style="margin-bottom: 1.8rem; padding-bottom: 1rem;"><div style="font-weight: bold; color: #7f8c8d; font-size: 1.6rem; margin-bottom: 0.5rem;">最佳联系时间</div><div style="color: #2c3e50; font-size: 2.0rem; line-height: 1.8;">{contact_time}</div></div>', unsafe_allow_html=True)
        
        if work_experience or awards or self_evaluation:
            if work_experience:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="section-title">工作经验</p>', unsafe_allow_html=True)
                lines = work_experience.strip().split('\n')
                for line in lines:
                    if line.strip():
                        st.markdown(f'<div style="margin-bottom: 1.5rem; padding-left: 2rem; position: relative; font-size: 1.8rem; line-height: 1.9;">• {line.strip()}</div>', unsafe_allow_html=True)
            
            if awards:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="section-title">奖项荣誉</p>', unsafe_allow_html=True)
                lines = awards.strip().split('\n')
                for line in lines:
                    if line.strip():
                        st.markdown(f'<div style="margin-bottom: 1.5rem; padding-left: 2rem; position: relative; font-size: 1.8rem; line-height: 1.9;">• {line.strip()}</div>', unsafe_allow_html=True)
            
            if self_evaluation:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="section-title">自我评价</p>', unsafe_allow_html=True)
                lines = self_evaluation.strip().split('\n')
                for line in lines:
                    if line.strip():
                        st.markdown(f'<div style="margin-bottom: 1.5rem; padding-left: 2rem; position: relative; font-size: 1.8rem; line-height: 1.9;">• {line.strip()}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn1:
        if st.button("💾 保存简历", use_container_width=True):
            st.success("简历已保存！（此处为演示功能）")
    with col_btn2:
        if st.button("🖨️ 打印简历", use_container_width=True):
            st.info("打印功能已准备就绪！（此处为演示功能）")
    with col_btn3:
        if st.button("📧 发送简历", use_container_width=True):
            st.success("简历发送功能已准备就绪！（此处为演示功能）")
