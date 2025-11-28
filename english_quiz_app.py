import streamlit as st
import random
import pandas as pd
import re
import json
import os

# ==========================================
# 1. 載入單字資料庫
# ==========================================

@st.cache_data
def load_vocab_database():
    """載入單字資料庫 (從 vocab_builder.py 生成的 JSON 檔案)"""
    try:
        with open('vocab_database.json', 'r', encoding='utf-8') as f:
            vocab_data = json.load(f)
            return vocab_data
    except FileNotFoundError:
        st. error("❌ 找不到 vocab_database.json 檔案！")
        st.info("📝 請先使用 vocab_builder.py 建立單字資料庫")
        st.code("python vocab_builder.py your_vocab. csv", language="bash")
        return []
    except json.JSONDecodeError:
        st.error("❌ JSON 檔案格式錯誤！")
        return []
    except Exception as e:
        st.error(f"❌ 載入資料庫失敗: {e}")
        return []

# 載入資料庫
VOCAB_DB = load_vocab_database()

# ==========================================
# 2. 核心邏輯函式
# ==========================================

def init_state():
    """初始化 session state"""
    if 'cloze_qid' not in st.session_state:
        st.session_state.cloze_qid = 0
        st.session_state.cloze_q = None
        st.session_state. cloze_submitted = False
        st.session_state.cloze_answer = None
    
    if 'c2e_qid' not in st. session_state:
        st. session_state.c2e_qid = 0
        st.session_state.c2e_q = None
        st. session_state.c2e_submitted = False
        st.session_state.c2e_answer = None
    
    if 'e2c_qid' not in st.session_state:
        st.session_state.e2c_qid = 0
        st.session_state.e2c_q = None
        st.session_state.e2c_submitted = False
        st.session_state.e2c_answer = None

def generate_question(mode):
    """生成新題目"""
    if not VOCAB_DB or len(VOCAB_DB) < 4:
        return None
    
    correct = random.choice(VOCAB_DB)
    others = [w for w in VOCAB_DB if w['english'] != correct['english']]
    distractors = random.sample(others, min(3, len(others)))
    
    if mode in ['cloze', 'c2e']:
        options = [d['english'] for d in distractors] + [correct['english']]
    else:  # e2c
        options = [d['chinese'] for d in distractors] + [correct['chinese']]
    
    random.shuffle(options)
    return {'correct': correct, 'options': options}

# ==========================================
# 3.  主程式介面
# ==========================================

def main():
    st.set_page_config(page_title="英文單字測驗", page_icon="📚", layout="centered")
    st.title("🎓 英文單字特訓 App")
    
    # 檢查資料庫
    if not VOCAB_DB:
        st.warning("⚠️ 沒有單字資料！")
        
        with st.expander("📖 如何建立資料庫？", expanded=True):
            st. markdown("""
            ### 步驟 1: 準備 CSV 檔案
            建立包含以下欄位的 CSV：
            - `english`: 英文單字
            - `chinese`: 中文意思
            - `pos`: 詞性
            
            **範例：**
            ```csv
            english,chinese,pos
            application,應用,n. 
            invent,發明,v.
            invest,投資,v.
            ```
            
            ### 步驟 2: 執行建立工具
            ```bash
            python vocab_builder.py your_vocab.csv
            ```
            
            ### 步驟 3: 重新整理此頁面
            資料庫建立完成後，重新整理此頁面即可開始測驗！
            """)
        
        st.stop()
    
    # 側邊欄
    with st.sidebar:
        st. header("📊 資料庫狀態")
        st.metric("單字總數", len(VOCAB_DB))
        
        # 顯示資料庫檔案資訊 (修正這裡)
        try:
            if os.path.exists('vocab_database.json'):
                file_size = os.path.getsize('vocab_database.json')
                st.caption(f"資料庫大小: {file_size/1024:. 2f} KB")  # 修正：移除空格
        except Exception as e:
            st.caption("無法讀取檔案大小")
        
        if st.button("🔄 重新載入資料庫"):
            st.cache_data.clear()
            st.rerun()
        
        with st.expander("📖 單字列表"):
            df = pd.DataFrame(VOCAB_DB)
            st.dataframe(
                df[['english', 'chinese', 'pos']], 
                hide_index=True,
                use_container_width=True
            )
    
    init_state()
    
    tab1, tab2, tab3 = st.tabs(["🔤 克漏字", "🇨🇳➡🇬🇧 中翻英", "🇬🇧➡🇨🇳 英翻中"])
    
    # ==================== 克漏字測驗 ====================
    with tab1:
        st.subheader("克漏字測驗")
        
        if st.session_state.cloze_q is None:
            st.session_state.cloze_q = generate_question('cloze')
            st.session_state.cloze_submitted = False
        
        q = st.session_state.cloze_q
        if q is None:
            st.error("無法生成題目，請檢查資料庫。")
            return
        
        word = q['correct']
        
        # 挖空例句
        sentence = re.sub(re.escape(word['english']), "_______", word['example'], flags=re.IGNORECASE)
        st.markdown(f"### {sentence}")
        # st.info(f"💡 提示: {word['chinese']} ({word['pos']})")
        
        with st.form(key=f'cloze_form_{st.session_state.cloze_qid}'):
            choice = st.radio("請選擇答案：", q['options'])
            submitted = st.form_submit_button("✅ 提交答案")
            
            if submitted:
                st.session_state.cloze_submitted = True
                st.session_state. cloze_answer = choice
        
        if st.session_state.cloze_submitted:
            user_choice = st.session_state.cloze_answer
            
            st.markdown("---")
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == word['english']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是: **{word['english']}**")
            
            st.markdown("### 📝 單字資訊")
            st.write(f"**• 英文:** {word['english']}")
            st.write(f"**• 詞性:** {word['pos']}")
            st.write(f"**• 中文:** {word['chinese']}")
            st.write(f"**• 例句:** {word['example']}")
            
            if st.button("➡ 下一題", key=f'cloze_next_{st.session_state.cloze_qid}'):
                st.session_state.cloze_qid += 1
                st. session_state.cloze_q = None
                st.session_state.cloze_submitted = False
                st.rerun()
    
    # ==================== 中翻英測驗 ====================
    with tab2:
        st.subheader("中翻英測驗")
        
        if st.session_state.c2e_q is None:
            st.session_state.c2e_q = generate_question('c2e')
            st.session_state.c2e_submitted = False
        
        q = st.session_state.c2e_q
        if q is None:
            st.error("無法生成題目，請檢查資料庫。")
            return
        
        word = q['correct']
        
        st.markdown(f"### 中文: **{word['chinese']}**")
        st.write(f"詞性: {word['pos']}")
        
        with st.form(key=f'c2e_form_{st.session_state.c2e_qid}'):
            choice = st.radio("請選擇英文單字：", q['options'])
            submitted = st.form_submit_button("✅ 提交答案")
            
            if submitted:
                st.session_state.c2e_submitted = True
                st.session_state.c2e_answer = choice
        
        if st. session_state.c2e_submitted:
            user_choice = st.session_state.c2e_answer
            
            st.markdown("---")
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == word['english']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是: **{word['english']}**")
            
            st.markdown("### 📝 單字資訊")
            st.write(f"**• 英文:** {word['english']}")
            st.write(f"**• 詞性:** {word['pos']}")
            st.write(f"**• 中文:** {word['chinese']}")
            st.write(f"**• 例句:** {word['example']}")
            
            if st.button("➡ 下一題", key=f'c2e_next_{st. session_state.c2e_qid}'):
                st. session_state.c2e_qid += 1
                st.session_state.c2e_q = None
                st. session_state.c2e_submitted = False
                st.rerun()
    
    # ==================== 英翻中測驗 ====================
    with tab3:
        st.subheader("英翻中測驗")
        
        if st.session_state.e2c_q is None:
            st.session_state.e2c_q = generate_question('e2c')
            st. session_state.e2c_submitted = False
        
        q = st.session_state.e2c_q
        if q is None:
            st.error("無法生成題目，請檢查資料庫。")
            return
        
        word = q['correct']
        
        st.markdown(f"### 英文: **{word['english']}**")
        st.write(f"詞性: {word['pos']}")
        
        with st. form(key=f'e2c_form_{st.session_state.e2c_qid}'):
            choice = st. radio("請選擇中文意思：", q['options'])
            submitted = st.form_submit_button("✅ 提交答案")
            
            if submitted:
                st.session_state.e2c_submitted = True
                st.session_state.e2c_answer = choice
        
        if st. session_state.e2c_submitted:
            user_choice = st.session_state.e2c_answer
            
            st.markdown("---")
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == word['chinese']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是: **{word['chinese']}**")
            
            st.markdown("### 📝 單字資訊")
            st.write(f"**• 英文:** {word['english']}")
            st.write(f"**• 詞性:** {word['pos']}")
            st.write(f"**• 中文:** {word['chinese']}")
            st.write(f"**• 例句:** {word['example']}")
            
            if st.button("➡ 下一題", key=f'e2c_next_{st. session_state.e2c_qid}'):
                st. session_state.e2c_qid += 1
                st.session_state.e2c_q = None
                st. session_state.e2c_submitted = False
                st.rerun()

if __name__ == "__main__":
    main()






