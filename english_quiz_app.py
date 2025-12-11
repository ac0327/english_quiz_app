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
        st.error("❌ 找不到 vocab_database.json 檔案！")
        st.info("📝 請先使用 vocab_builder.py 建立單字資料庫")
        st.code("python vocab_builder.py your_vocab. csv", language="bash")
        return []
    except json.JSONDecodeError:
        st.error("❌ JSON 檔案格式錯誤！")
        return []
    except Exception as e:
        st.error(f"❌ 載入資料庫失敗:  {e}")
        return []

# 載入資料庫
VOCAB_DB = load_vocab_database()

# ==========================================
# 2. 核心邏輯函式
# ==========================================

def remove_chinese_from_text(text):
    """移除文字中括號內的中文"""
    if not text:
        return text
    
    text = re.sub(r'\([^)]*[\u4e00-\u9fff][^)]*\)', '', text)
    text = re.sub(r'（[^）]*[\u4e00-\u9fff][^）]*）', '', text)
    text = re.sub(r'\[[^\]]*[\u4e00-\u9fff][^\]]*\]', '', text)
    text = re.sub(r'【[^】]*[\u4e00-\u9fff][^】]*】', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_common_prefix_length(word1, word2):
    """計算兩個單字的共同前綴長度"""
    min_len = min(len(word1), len(word2))
    for i in range(min_len):
        if word1[i]. lower() != word2[i].lower():
            return i
    return min_len

def find_similar_words(target_word, word_list, min_common_chars=3, max_results=3):
    """找出與目標單字相似的單字"""
    similar_words = []
    target_lower = target_word['english'].lower()
    
    for word in word_list: 
        if word['english'] == target_word['english']: 
            continue
        
        word_lower = word['english'].lower()
        
        # 檢查共同前綴
        common_prefix = get_common_prefix_length(target_lower, word_lower)
        
        # 檢查共同子字串
        common_substring = 0
        for i in range(len(target_lower)):
            for j in range(i + min_common_chars, len(target_lower) + 1):
                substring = target_lower[i:j]
                if substring in word_lower and len(substring) > common_substring:
                    common_substring = len(substring)
        
        max_common = max(common_prefix, common_substring)
        
        if max_common >= min_common_chars:
            similar_words.append({
                'word': word,
                'similarity': max_common
            })
    
    similar_words.sort(key=lambda x: x['similarity'], reverse=True)
    return [item['word'] for item in similar_words[:max_results]]

def generate_confusing_question_set():
    """生成一組易混淆單字，並為每個單字準備考題"""
    if not VOCAB_DB or len(VOCAB_DB) < 10:
        return None
    
    max_attempts = 50
    for _ in range(max_attempts):
        target_word = random.choice(VOCAB_DB)
        similar_words = find_similar_words(target_word, VOCAB_DB, min_common_chars=3, max_results=3)
        
        if len(similar_words) >= 2:
            all_words = [target_word] + similar_words
            
            # 為每個單字生成一題
            questions = []
            for word in all_words:
                other_words = [w for w in all_words if w['english'] != word['english']]
                options = [w['chinese'] for w in other_words] + [word['chinese']]
                random.shuffle(options)
                
                questions.append({
                    'target': word,
                    'all_words': all_words,
                    'options': options
                })
            
            return {
                'questions': questions,
                'current_index': 0,
                'all_words': all_words
            }
    
    return None

def init_state():
    """初始化 session state"""
    if 'cloze_qid' not in st.session_state:
        st.session_state.cloze_qid = 0
        st.session_state.cloze_q = None
        st.session_state.cloze_submitted = False
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
    
    if 'match_qid' not in st.session_state:
        st.session_state.match_qid = 0
        st.session_state.match_q = None
        st.session_state.match_submitted = False
        st.session_state.match_answers = {}
    
    if 'confuse_qid' not in st.session_state:
        st.session_state.confuse_qid = 0
        st.session_state.confuse_q_set = None
        st.session_state.confuse_submitted = False
        st.session_state.confuse_answer = None

def generate_question(mode):
    """生成新題目"""
    if not VOCAB_DB or len(VOCAB_DB) < 4:
        return None
    
    correct = random.choice(VOCAB_DB)
    others = [w for w in VOCAB_DB if w['english'] != correct['english']]
    distractors = random.sample(others, min(3, len(others)))
    
    if mode in ['cloze', 'c2e']:
        options = [d['english'] for d in distractors] + [correct['english']]
    else:
        options = [d['chinese'] for d in distractors] + [correct['chinese']]
    
    random.shuffle(options)
    return {'correct': correct, 'options': options}

def generate_matching_question(count=10):
    """生成配對題"""
    if not VOCAB_DB or len(VOCAB_DB) < count:
        return None
    
    selected_words = random.sample(VOCAB_DB, count)
    english_list = [(i+1, word['english'], word) for i, word in enumerate(selected_words)]
    chinese_list = [word['chinese'] for word in selected_words]
    random.shuffle(chinese_list)
    
    return {
        'english_list':  english_list,
        'chinese_list': chinese_list,
        'correct_answers': {word['english']: word['chinese'] for word in selected_words}
    }

# ==========================================
# 3. 主程式介面
# ==========================================

def main():
    st.set_page_config(page_title="TOEIC, Target 900!", page_icon="📚", layout="wide")
    st.title("🎓 TOEIC Vocabulary Test App")
    
    if not VOCAB_DB: 
        st.warning("⚠️ 沒有單字資料！")
        with st.expander("📖 如何建立資料庫？", expanded=True):
            st.markdown("""
            ### 步驟 1: 準備 CSV 檔案
            ### 步驟 2: 執行建立工具  
            ### 步驟 3: 重新整理此頁面
            """)
        st.stop()
    
    with st.sidebar:
        st.header("📊 資料庫狀態")
        st.metric("單字總數", len(VOCAB_DB))
        
        try:
            if os.path.exists('vocab_database.json'):
                file_size = os.path.getsize('vocab_database.json')
                st.caption(f"資料庫大小: {file_size/1024:.2f} KB")
        except Exception: 
            st.caption("無法讀取檔案大小")
        
        if st.button("🔄 重新載入資料庫"):
            st.cache_data.clear()
            st.rerun()
        
        with st.expander("📖 單字列表"):
            df = pd.DataFrame(VOCAB_DB)
            st.dataframe(df[['english', 'chinese', 'pos']], hide_index=True, use_container_width=True)
    
    init_state()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔤 克漏字", 
        "🇨🇳➡🇬🇧 中翻英", 
        "🇬🇧➡🇨🇳 英翻中",
        "🔗 配對題",
        "⚠️ 易混淆"
    ])
    
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
        clean_example = remove_chinese_from_text(word['example'])
        sentence = re.sub(re.escape(word['english']), "_______", clean_example, flags=re.IGNORECASE)
        
        st.markdown(f"### {sentence}")
        
        with st.form(key=f'cloze_form_{st.session_state.cloze_qid}'):
            choice = st.radio("請選擇答案：", q['options'])
            
            # ✨ 修改：將提交和下一題按鈕都放在 Form 內
            col1, col2 = st. columns([1, 1])
            with col1:
                submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)
            with col2:
                next_question = st.form_submit_button("➡ 下一題", use_container_width=True)
            
            if submitted: 
                st.session_state. cloze_submitted = True
                st.session_state.cloze_answer = choice
            
            if next_question:
                st. session_state.cloze_qid += 1
                st.session_state.cloze_q = None
                st.session_state.cloze_submitted = False
                st.rerun()
        
        if st.session_state.cloze_submitted:
            user_choice = st.session_state.cloze_answer
            
            st.markdown("---")
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == word['english']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是:  **{word['english']}**")
            
            st.markdown("### 📝 單字資訊")
            st.write(f"**• 英文:** {word['english']}")
            st.write(f"**• 詞性:** {word['pos']}")
            st.write(f"**• 中文:** {word['chinese']}")
            st.write(f"**• 例句:** {clean_example}")
    
    # ==================== 中翻英測驗 ====================
    with tab2:
        st.subheader("中翻英測驗")
        
        if st.session_state.c2e_q is None:
            st.session_state.c2e_q = generate_question('c2e')
            st.session_state. c2e_submitted = False
        
        q = st.session_state.c2e_q
        if q is None: 
            st.error("無法生成題目，請檢查資料庫。")
            return
        
        word = q['correct']
        
        st.markdown(f"### 中文: **{word['chinese']}**")
        st.write(f"詞性: {word['pos']}")
        
        with st.form(key=f'c2e_form_{st.session_state.c2e_qid}'):
            choice = st.radio("請選擇英文單字：", q['options'])
            
            col1, col2 = st. columns([1, 1])
            with col1:
                submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)
            with col2:
                next_question = st. form_submit_button("➡ 下一題", use_container_width=True)
            
            if submitted:
                st.session_state.c2e_submitted = True
                st. session_state.c2e_answer = choice
            
            if next_question:
                st. session_state.c2e_qid += 1
                st.session_state.c2e_q = None
                st. session_state.c2e_submitted = False
                st.rerun()
        
        if st.session_state.c2e_submitted:
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
            
            clean_example = remove_chinese_from_text(word['example'])
            st.write(f"**• 例句:** {clean_example}")
    
    # ==================== 英翻中測驗 ====================
    with tab3:
        st.subheader("英翻中測驗")
        
        if st.session_state.e2c_q is None:
            st.session_state.e2c_q = generate_question('e2c')
            st.session_state. e2c_submitted = False
        
        q = st.session_state.e2c_q
        if q is None: 
            st.error("無法生成題目，請檢查資料庫。")
            return
        
        word = q['correct']
        
        st.markdown(f"### 英文: **{word['english']}**")
        st.write(f"詞性: {word['pos']}")
        
        with st.form(key=f'e2c_form_{st.session_state.e2c_qid}'):
            choice = st.radio("請選擇中文意思：", q['options'])
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)
            with col2:
                next_question = st.form_submit_button("➡ 下一題", use_container_width=True)
            
            if submitted:
                st.session_state.e2c_submitted = True
                st.session_state. e2c_answer = choice
            
            if next_question: 
                st.session_state. e2c_qid += 1
                st.session_state.e2c_q = None
                st.session_state. e2c_submitted = False
                st.rerun()
        
        if st.session_state.e2c_submitted:
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
            
            clean_example = remove_chinese_from_text(word['example'])
            st.write(f"**• 例句:** {clean_example}")
    
    # ==================== 配對題 ====================
    with tab4:
        st.subheader("🔗 英中配對題")
        st.caption("請將左側的英文單字與右側的中文意思配對")
        
        if len(VOCAB_DB) < 10:
            st.warning(f"⚠️ 資料庫只有 {len(VOCAB_DB)} 個單字，需要至少 10 個才能進行配對題。")
            return
        
        if st.session_state.match_q is None:
            st.session_state.match_q = generate_matching_question(10)
            st.session_state.match_submitted = False
            st.session_state.match_answers = {}
        
        q = st. session_state.match_q
        if q is None:
            st.error("無法生成題目，請檢查資料庫。")
            return
        
        with st.form(key=f'match_form_{st.session_state.match_qid}'):
            col1, col2 = st. columns([1, 1])
            
            with col1:
                st.markdown("### 📝 英文單字")
                for num, eng, word_data in q['english_list']: 
                    st.markdown(f"**{num}. ** {eng}")
            
            with col2:
                st.markdown("### 🎯 選擇中文意思")
                
                user_answers = {}
                for num, eng, word_data in q['english_list']:
                    options = ['請選擇... '] + q['chinese_list']
                    selected = st.selectbox(
                        f"{num}.  {eng}",
                        options,
                        key=f'match_{num}_{st.session_state.match_qid}'
                    )
                    user_answers[eng] = selected
            
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)
            with col_btn2:
                next_match = st.form_submit_button("➡ 下一組配對題", use_container_width=True)
            
            if submitted: 
                if '請選擇...' in user_answers. values():
                    st.warning("⚠️ 請完成所有配對！")
                else:
                    st.session_state.match_submitted = True
                    st.session_state. match_answers = user_answers
            
            if next_match: 
                st.session_state.match_qid += 1
                st.session_state.match_q = None
                st.session_state.match_submitted = False
                st.session_state.match_answers = {}
                st.rerun()
        
        if st.session_state.match_submitted:
            st.markdown("---")
            st.markdown("## 📊 答題結果")
            
            correct_count = 0
            total_count = len(q['correct_answers'])
            
            for num, eng, word_data in q['english_list']:
                user_ans = st.session_state.match_answers.get(eng, '')
                correct_ans = q['correct_answers'][eng]
                
                if user_ans == correct_ans: 
                    st.success(f"✅ **{num}. {eng}** → {user_ans} (正確)")
                    correct_count += 1
                else:
                    st.error(f"❌ **{num}. {eng}** → 您的答案: {user_ans} | 正確答案: {correct_ans}")
            
            score = (correct_count / total_count) * 100
            st.markdown("---")
            
            if score == 100:
                st.balloons()
                st.success(f"🎉 **完美！** 您答對了 {correct_count}/{total_count} 題！")
            elif score >= 70:
                st.success(f"👍 **很好！** 您答對了 {correct_count}/{total_count} 題 ({score:.0f}%)")
            elif score >= 50:
                st.warning(f"💪 **還不錯！** 您答對了 {correct_count}/{total_count} 題 ({score:.0f}%)")
            else:
                st.info(f"📚 **繼續加油！** 您答對了 {correct_count}/{total_count} 題 ({score:. 0f}%)")
    
    # ==================== 易混淆單字測驗 ====================
    with tab5:
        st.subheader("⚠️ 易混淆單字測驗")
        st.caption("這些單字拼法相似，每個都會出題測試！")
        
        if st. session_state.confuse_q_set is None:
            st. session_state.confuse_q_set = generate_confusing_question_set()
            st.session_state.confuse_submitted = False
        
        q_set = st.session_state. confuse_q_set
        
        if q_set is None: 
            st.warning("⚠️ 資料庫中找不到足夠的相似單字。")
            with st.expander("💡 什麼是易混淆單字？"):
                st.markdown("""
                易混淆單字是指拼法相似、容易搞混的單字，例如：
                - **over**view, **over**look, **over**see
                - **app**lication, **app**eal, **app**ear
                """)
            return
        
        current_q = q_set['questions'][q_set['current_index']]
        target = current_q['target']
        all_words = current_q['all_words']
        total_questions = len(q_set['questions'])
        
        st.progress((q_set['current_index'] + 1) / total_questions)
        st.caption(f"題目 {q_set['current_index'] + 1} / {total_questions}")
        
        st. markdown("### 🎯 請選出以下單字的正確中文意思：")
        
        cols = st.columns(len(all_words))
        for idx, word in enumerate(all_words):
            with cols[idx]: 
                if word == target:
                    st.markdown(f"### 🔹 **{word['english']}**")
                else:
                    st.markdown(f"### {word['english']}")
        
        st. markdown("---")
        st.markdown(f"### 📝 題目 {q_set['current_index'] + 1}:  請選擇 **{target['english']}** 的中文意思")
        
        with st.form(key=f'confuse_form_{st.session_state.confuse_qid}_{q_set["current_index"]}'):
            choice = st.radio(
                f"**{target['english']}** 的意思是？",
                current_q['options'],
                key=f'confuse_radio_{st.session_state. confuse_qid}_{q_set["current_index"]}'
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submitted = st.form_submit_button("✅ 提交答案", use_container_width=True)
            with col2:
                if q_set['current_index'] < total_questions - 1:
                    next_question = st.form_submit_button("➡ 下一題", use_container_width=True)
                else:
                    restart = st.form_submit_button("🔄 開始新的一組", use_container_width=True)
            
            if submitted: 
                st.session_state.confuse_submitted = True
                st.session_state.confuse_answer = choice
            
            if q_set['current_index'] < total_questions - 1:
                if 'next_question' in locals() and next_question:
                    q_set['current_index'] += 1
                    st.session_state.confuse_submitted = False
                    st.session_state.confuse_answer = None
                    st.rerun()
            else:
                if 'restart' in locals() and restart:
                    st.session_state.confuse_qid += 1
                    st.session_state.confuse_q_set = None
                    st.session_state.confuse_submitted = False
                    st.session_state.confuse_answer = None
                    st. rerun()
        
        if st.session_state.confuse_submitted:
            user_choice = st.session_state.confuse_answer
            
            st.markdown("---")
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == target['chinese']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是:  **{target['chinese']}**")
            
            st.markdown("### 📝 單字資訊")
            with st.expander(f"**{target['english']}** = {target['chinese']} ({target['pos']})", expanded=True):
                clean_example = remove_chinese_from_text(target['example'])
                st.write(f"**例句:** {clean_example}")
            
            if q_set['current_index'] == total_questions - 1:
                st.success("🎊 **恭喜！您已完成這組易混淆單字測驗！**")
                
                st.markdown("---")
                st.markdown("### 📚 易混淆單字總複習")
                for word in all_words:
                    with st.expander(f"**{word['english']}** = {word['chinese']} ({word['pos']})"):
                        clean_example = remove_chinese_from_text(word['example'])
                        st.write(f"**例句:** {clean_example}")

if __name__ == "__main__": 
    main()

