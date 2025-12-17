import streamlit as st

# 页面配置
st.set_page_config(
    page_title="多功能应用集合",
    page_icon="🚀",
    layout="wide"
)

# 自定义CSS样式 - 点击后按钮变深灰色
st.markdown("""
<style>
/* 侧边栏按钮基础样式 */
.stButton button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 5px !important;
    margin: 2px 0 !important;
    padding: 12px 20px !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 16px !important;
    transition: all 0.2s ease !important;
}

/* 鼠标悬停效果 */
.stButton button:hover {
    background-color: #f5f5f5 !important;
    border-color: #999 !important;
}

/* 点击后/选中状态的按钮 - 深灰色 */
.stButton button:active,
.stButton button:focus {
    background-color: #424242 !important;  /* 深灰色 */
    color: white !important;
    border-color: #424242 !important;
}

/* 侧边栏标题样式 */
div[data-testid="stSidebar"] h1 {
    text-align: center !important;
    margin-bottom: 20px !important;
}

/* 分隔线样式 */
div[data-testid="stSidebar"] hr {
    margin: 15px 0 !important;
    border: none !important;
    height: 1px !important;
    background-color: #e0e0e0 !important;
}

/* 信息框样式 */
div[data-testid="stSidebar"] .stAlert {
    font-size: 14px !important;
    padding: 8px !important;
    margin-top: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# 侧边栏导航
st.sidebar.title("📱 应用导航")
st.sidebar.markdown("---")

# 应用列表
apps = [
    "🏠 首页",
    "🦐 南宁美食", 
    "🎡 动漫视频",
    "📚 学生作业",
    "🖼️ 动漫相册",
    "🎶 音乐播放"
]

# 创建垂直排列的按钮
for app in apps:
    if st.sidebar.button(app, use_container_width=True):
        st.session_state['selected_app'] = app

# 初始化选中状态
if 'selected_app' not in st.session_state:
    st.session_state['selected_app'] = "🏠 首页"

st.sidebar.markdown("---")


# 获取当前选中的应用
selected_app = st.session_state['selected_app']

# 主页内容
if selected_app == "🏠 首页":
    st.image("https://www.gxvnu.edu.cn/lib/images/logo.png")
    st.title("🏠 应用首页")
    st.markdown("### 欢迎使用多功能应用集合")
    st.image("https://www.gxvnu.edu.cn/lib/images/home/ba01.jpg")
    st.text("欢迎来到我们的多功能应用乐园！这里汇集了大家最爱的精彩内容：南宁美食天地带你探索地道老友味，动漫影视馆有蜡笔小新陪你欢乐每一天，学习小伙伴帮你轻松管理作业进度，动漫画廊展示精美动漫图集，音乐时光机提供随时随地的美妙陪伴。点击左侧导航栏，开始探索这些精彩功能吧！每个应用都有独特惊喜等着你发现，让生活更便捷，让时光更美好！✨😊")
    
    
    

# 其他应用通过读取文件内容直接执行
else:
    # 映射应用名称到文件名
    app_files = {
        "🦐 南宁美食": "delicacy.py",
        "🎡 动漫视频": "video.py", 
        "📚 学生作业": "homework.py",
        "🖼️ 动漫相册": "image.py",
        "🎶 音乐播放": "song.py"
    }
    
    if selected_app in app_files:
        filename = app_files[selected_app]
        try:
            # 显示当前应用标题（不显示返回按钮）
            st.markdown(f"# {selected_app}")
            
            # 直接读取并执行文件内容
            with open(filename, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # 使用exec执行文件代码
            exec(file_content, globals())
            
        except FileNotFoundError:
            st.error(f"找不到文件: {filename}")
            st.info("请确保以下文件存在于同一目录下：")
            st.code("delicacy.py\nvideo.py\nhomework.py\nimage.py\nsong.py")
            
        except Exception as e:
            st.error(f"加载应用时出错: {str(e)}")
            
    else:
        st.error("应用不存在")
