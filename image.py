import streamlit as st

st.set_page_config(page_title="相册", page_icon="🐎")
st.title("我的动漫相册")

if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

images = [
    {
        'url': "https://img-baofun.zhhainiao.com/fs/a4cdaadfb481ce7358b658f2f3de7f9c.jpg",
        'text': '蜡笔小新'
    },
    {
        'url': "https://file.moyubuluo.com/d/file/2025-06-03/0176c88a7184c3a883e608a3f2e3b7a4.jpg",
        'text': '疯狂动物城'
    },
    {
        'url': "http://vsd-picture.cdn.bcebos.com/5e516089e12c1fcd43d79dfaab8930a53c61766f.jpg",
        'text': '风之谷'
    },
    {
        'url': "https://www.bizhigq.com/caiji-img/0495428d2e0d62f29753b9a101e11087.jpg",
        'text': '千与千寻'
    }
]

st.image(images[st.session_state['ind']]['url'], 
         caption=images[st.session_state['ind']]['text'])

def nextImg():
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(images)

def prevImg():
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(images)

c1, c2 = st.columns(2)

with c1:
    st.button("上一张", on_click=prevImg, use_container_width=True)
with c2:
    st.button("下一张", on_click=nextImg, use_container_width=True)
