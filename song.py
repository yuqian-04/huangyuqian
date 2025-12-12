import streamlit as st

# 设置墨蓝色背景和按钮样式
page_bg = """
<style>
.stApp {
    background-color: #1a1a2e;
    color: #ffffff;
}
h1, h2, h3 {
    color: #ffffff;
}
p, .stText {
    color: #ffffff;
}
.css-1d391kg {
    background-color: #16213e;
}

/* 按钮基础样式 */
.stButton > button {
    color: white !important;
    background-color: #0f3460 !important;
    border: 1px solid #3d5a80 !important;
    border-radius: 5px !important;
    transition: all 0.3s ease !important;
}



/* 按钮点击样式 */
.stButton > button:active,
.stButton > button:focus {
    background-color: #0d2b4e !important;
    border-color: #3d5a80 !important;
    transform: translateY(0) !important;
    box-shadow: none !important;
}

/* 确保所有文本都是白色 */
.stMarkdown, .stText {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.set_page_config(page_title="音乐", page_icon="🐎")
st.title("🎶音乐播放器")

# 使用markdown确保文字颜色为白色
st.markdown("简易音乐播放器，找到属于你的音乐")

songs = [
    {
        'url': "https://img95.699pic.com/photo/60062/6758.jpg_wh860.jpg",
        'text': "专辑封面",
        'name': "Cry For You",
        'author': 'Karry_b',
        'time': "时长：4:57",
        'audio': 'https://music.163.com/song/media/outer/url?id=3323934230.mp3'
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

if 'current_song' not in st.session_state:
    st.session_state['current_song'] = 0

current_index = st.session_state['current_song']
current_song = songs[current_index]

col1, col2 = st.columns([1, 2])

with col1:
    st.image(current_song['url'], caption=current_song['text'])

with col2:
    st.markdown(f"### {current_song['name']}")
    st.markdown(f"**歌手：** {current_song['author']}")
    st.markdown(f"**{current_song['time']}**")
    
    # 上一首/下一首按钮
    def next_song():
        st.session_state['current_song'] = (st.session_state['current_song'] + 1) % len(songs)
    
    def prev_song():
        st.session_state['current_song'] = (st.session_state['current_song'] - 1) % len(songs)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("上一首", on_click=prev_song, use_container_width=True)
    with btn_col2:
        st.button("下一首", on_click=next_song, use_container_width=True)

# 音频播放器放在最下面
st.audio(current_song['audio'])
