import streamlit as st
import random
import pandas as pd
import re

# ==========================================
# 1. 資料庫設定 (包含您 138 個單字 + AI 生成的例句)
# 說明：資料庫已直接嵌入程式碼，以確保 App 獨立運行。
# ==========================================

VOCAB_DB = [
    {
        "english": "application",
        "chinese": "應用",
        "pos": "n.",
        "example": "The new software **application** significantly improves our workflow."
    },
    {
        "english": "invent",
        "chinese": "發明",
        "pos": "v.",
        "example": "Thomas Edison did not **invent** the lightbulb, but he improved it."
    },
    {
        "english": "invest",
        "chinese": "投資",
        "pos": "v.",
        "example": "It's wise to **invest** your money in a diversified portfolio."
    },
    {
        "english": "patent",
        "chinese": "專利",
        "pos": "n.",
        "example": "The company filed a **patent** to protect its unique invention."
    },
    {
        "english": "advance",
        "chinese": "…方面的進展",
        "pos": "n.",
        "example": "We have seen a huge **advance** in mobile communication technology."
    },
    {
        "english": "domestic",
        "chinese": "國內的",
        "pos": "adj.",
        "example": "The factory primarily focuses on **domestic** production for the local market."
    },
    {
        "english": "superior",
        "chinese": "優秀的",
        "pos": "adj.",
        "example": "His performance in the competition was far **superior** to the other candidates."
    },
    {
        "english": "accomplished",
        "chinese": "熟練的",
        "pos": "adj.",
        "example": "She is an **accomplished** pianist who has performed all over the world."
    },
    {
        "english": "accomplish",
        "chinese": "完成",
        "pos": "v.",
        "example": "Despite the difficulties, they managed to **accomplish** their goal on time."
    },
    {
        "english": "accompany",
        "chinese": "陪伴",
        "pos": "v.",
        "example": "I will **accompany** my grandmother to the doctor's appointment."
    },
    {
        "english": "assignment",
        "chinese": "任務",
        "pos": "n.",
        "example": "The professor gave us a difficult **assignment** that is due next week."
    },
    {
        "english": "inquiry",
        "chinese": "詢問",
        "pos": "n.",
        "example": "The customer sent an **inquiry** regarding the product warranty."
    },
    {
        "english": "inquire",
        "chinese": "詢問",
        "pos": "v.",
        "example": "The detective went to **inquire** about the witness's whereabouts."
    },
    {
        "english": "compatible",
        "chinese": "相容的",
        "pos": "adj.",
        "example": "The new hardware is not **compatible** with my old computer system."
    },
    {
        "english": "competitive",
        "chinese": "有競爭力的",
        "pos": "adj.",
        "example": "We need to keep our prices low to stay **competitive** in the market."
    },
    {
        "english": "complicated",
        "chinese": "複雜的",
        "pos": "adj.",
        "example": "The instruction manual for assembling the shelf was very **complicated**."
    },
    {
        "english": "complain",
        "chinese": "抱怨",
        "pos": "v.",
        "example": "If you have an issue, you should **complain** to the manager immediately."
    },
    {
        "english": "devise",
        "chinese": "設計出",
        "pos": "v.",
        "example": "They had to **devise** a new strategy to overcome the unexpected challenge."
    },
    {
        "english": "device",
        "chinese": "裝置",
        "pos": "n.",
        "example": "The small electronic **device** can track your daily steps."
    },
    {
        "english": "corrosion",
        "chinese": "腐蝕",
        "pos": "n.",
        "example": "Exposure to salt water caused **corrosion** on the metal railings."
    },
    {
        "english": "precaution",
        "chinese": "預防措施",
        "pos": "n.",
        "example": "Wearing a helmet is a necessary **precaution** when riding a motorcycle."
    },
    {
        "english": "celebrity",
        "chinese": "名人",
        "pos": "n.",
        "example": "The restaurant is often visited by local **celebrity** chefs."
    },
    {
        "english": "improvise",
        "chinese": "即興演出",
        "pos": "n.",
        "example": "When the script was lost, the actors had to **improvise** the final scene."
    },
    {
        "english": "alumni",
        "chinese": "校友",
        "pos": "n.",
        "example": "The university's most successful **alumni** returned for the graduation ceremony."
    },
    {
        "english": "admission",
        "chinese": "入場",
        "pos": "n.",
        "example": "The ticket price includes free **admission** to all museum exhibits."
    },
    {
        "english": "succeed",
        "chinese": "成功, 繼任",
        "pos": "v.",
        "example": "He worked hard to **succeed** in his new career path."
    },
    {
        "english": "issue",
        "chinese": "(期刊)一期, 議題",
        "pos": "n.",
        "example": "The latest **issue** of the magazine focuses on climate change."
    },
    {
        "english": "anonymous",
        "chinese": "匿名的",
        "pos": "adj.",
        "example": "The donation was given by an **anonymous** benefactor who wished to remain unknown."
    },
    {
        "english": "commit",
        "chinese": "致力, 奉獻",
        "pos": "v.",
        "example": "She decided to **commit** her life to helping underprivileged children."
    },
    {
        "english": "advocate",
        "chinese": "擁護者",
        "pos": "n.",
        "example": "He is a strong **advocate** for environmental protection policies."
    },
    {
        "english": "antique",
        "chinese": "古董",
        "pos": "n.",
        "example": "The old vase in the corner is a valuable **antique** from the Ming Dynasty."
    },
    {
        "english": "auction",
        "chinese": "拍賣",
        "pos": "n.",
        "example": "They decided to sell the collection at an art **auction**."
    },
    {
        "english": "upcoming",
        "chinese": "即將來臨的",
        "pos": "adj.",
        "example": "Everyone is excited about the **upcoming** music festival next month."
    },
    {
        "english": "forthcoming",
        "chinese": "即將來臨的",
        "pos": "adj.",
        "example": "The details about the merger will be **forthcoming** in the next few weeks."
    },
    {
        "english": "monopoly",
        "chinese": "獨佔",
        "pos": "n.",
        "example": "The tech giant holds a **monopoly** on the social media market."
    },
    {
        "english": "monopolize",
        "chinese": "壟斷",
        "pos": "v.",
        "example": "The large corporations often **monopolize** the essential raw materials."
    },
    {
        "english": "apology",
        "chinese": "道歉",
        "pos": "n.",
        "example": "The manager issued a formal **apology** for the poor service."
    },
    {
        "english": "apologize",
        "chinese": "道歉",
        "pos": "v.",
        "example": "You should **apologize** immediately if you realize you made a mistake."
    },
    {
        "english": "consistently",
        "chinese": "始終一貫",
        "pos": "adv.",
        "example": "She **consistently** scores the highest marks in all her subjects."
    },
    {
        "english": "seasoned",
        "chinese": "經驗豐富的",
        "pos": "adj.",
        "example": "We hired a **seasoned** professional with over twenty years of experience."
    },
    {
        "english": "consequtive",
        "chinese": "連續的",
        "pos": "adj.",
        "example": "The team won three **consequtive** games before finally losing the fourth."
    },
    {
        "english": "successive",
        "chinese": "連續的",
        "pos": "adj.",
        "example": "The company has reported profits for five **successive** quarters."
    },
    {
        "english": "aggressively",
        "chinese": "積極地",
        "pos": "adv.",
        "example": "The sales team **aggressively** marketed the new product to a wider audience."
    },
    {
        "english": "absence",
        "chinese": "缺席, 缺少",
        "pos": "n.",
        "example": "Due to the director's unexpected **absence**, the meeting was postponed."
    },
    {
        "english": "assert",
        "chinese": "主張",
        "pos": "v.",
        "example": "He must **assert** his authority if he wants the team to follow his directions."
    },
    {
        "english": "drastic",
        "chinese": "激烈的",
        "pos": "adj.",
        "example": "The company had to take **drastic** measures to cut down its operating costs."
    },
    {
        "english": "prospect",
        "chinese": "展望",
        "pos": "n.",
        "example": "The job offers a good salary and excellent career **prospect** for the future."
    },
    {
        "english": "substitute",
        "chinese": "替代",
        "pos": "v.",
        "example": "If we run out of sugar, we can **substitute** honey in this recipe."
    },
    {
        "english": "substitute",
        "chinese": "代替物",
        "pos": "n.",
        "example": "Almond milk is a popular **substitute** for dairy milk among vegans."
    },
    {
        "english": "implication",
        "chinese": "暗示",
        "pos": "n.",
        "example": "The manager's silence had a strong **implication** of disapproval."
    },
    {
        "english": "adversity",
        "chinese": "逆境",
        "pos": "n.",
        "example": "She faced great **adversity** when her business first started, but she persevered."
    },
    {
        "english": "promising",
        "chinese": "有前途的",
        "pos": "adj.",
        "example": "The young scientist shows **promising** results in her latest research study."
    },
    {
        "english": "installment",
        "chinese": "分期付款",
        "pos": "n.",
        "example": "He decided to buy the expensive car using a monthly **installment** plan."
    },
    {
        "english": "authentic",
        "chinese": "正統的",
        "pos": "adj.",
        "example": "The restaurant claims to serve **authentic** Italian pasta dishes."
    },
    {
        "english": "authorize",
        "chinese": "批准, 授權",
        "pos": "v.",
        "example": "The board had to **authorize** the huge budget expenditure for the new project."
    },
    {
        "english": "authority",
        "chinese": "權威",
        "pos": "n.",
        "example": "You must obtain written **authority** before publishing classified documents."
    },
    {
        "english": "author",
        "chinese": "作者",
        "pos": "n.",
        "example": "The **author** of this thrilling novel will be signing books next week."
    },
    {
        "english": "instruction",
        "chinese": "說明",
        "pos": "n.",
        "example": "Please follow the safety **instruction** carefully before operating the machine."
    },
    {
        "english": "receipt",
        "chinese": "收據",
        "pos": "n.",
        "example": "Keep the sales **receipt** in case you need to return the item later."
    },
    {
        "english": "recipes",
        "chinese": "食譜",
        "pos": "n.",
        "example": "I found a book of traditional Spanish **recipes** in the old library."
    },
    {
        "english": "spare",
        "chinese": "備用的",
        "pos": "nadj",
        "example": "Always keep a **spare** tire in the trunk of your car for emergencies."
    },
    {
        "english": "spare",
        "chinese": "節省",
        "pos": "v.",
        "example": "We can hardly **spare** any more time for discussing the minor details."
    },
    {
        "english": "alter",
        "chinese": "修改",
        "pos": "v.",
        "example": "The tailor will need to **alter** the length of the trousers slightly."
    },
    {
        "english": "clearance",
        "chinese": "清倉, 准許",
        "pos": "n",
        "example": "The store is holding a huge **clearance** sale to make room for new inventory."
    },
    {
        "english": "mutually",
        "chinese": "互相",
        "pos": "adv.",
        "example": "The two countries signed a treaty that was **mutually** beneficial to both sides."
    },
    {
        "english": "redeemable",
        "chinese": "可兌換的",
        "pos": "adj.",
        "example": "This coupon is **redeemable** for a free dessert at any of our restaurants."
    },
    {
        "english": "fabric",
        "chinese": "布料",
        "pos": "n",
        "example": "She chose a silk **fabric** to make her wedding dress."
    },
    {
        "english": "envision",
        "chinese": "想像",
        "pos": "v.",
        "example": "It is hard to **envision** a world without internet connectivity today."
    },
    {
        "english": "grant",
        "chinese": "(正式)授予",
        "pos": "v.",
        "example": "The committee decided to **grant** him the award for his outstanding research."
    },
    {
        "english": "grant",
        "chinese": "(研究)獎助金",
        "pos": "n",
        "example": "The scientist applied for a large **grant** to fund his space exploration project."
    },
    {
        "english": "directory",
        "chinese": "通訊錄",
        "pos": "n",
        "example": "You can find all the staff contact details in the company **directory**."
    },
    {
        "english": "contrary",
        "chinese": "相反(情況)",
        "pos": "n",
        "example": "On the **contrary**, his statements are not based on facts."
    },
    {
        "english": "disturbing",
        "chinese": "令人不安的",
        "pos": "adj.",
        "example": "The recent news about the political unrest is quite **disturbing** to investors."
    },
    {
        "english": "engage",
        "chinese": "參加",
        "pos": "v.",
        "example": "She decided to **engage** in volunteer work during her summer break."
    },
    {
        "english": "foster",
        "chinese": "促進",
        "pos": "v.",
        "example": "The school aims to **foster** a love of reading in all its students."
    },
    {
        "english": "forest",
        "chinese": "森林",
        "pos": "n",
        "example": "The hikers spent the entire day walking through the dense national **forest**."
    },
    {
        "english": "compile",
        "chinese": "彙編, 收集",
        "pos": "v.",
        "example": "It took months for the librarian to **compile** all the historical documents."
    },
    {
        "english": "permanently",
        "chinese": "永久地",
        "pos": "adv.",
        "example": "The old bridge was damaged beyond repair and closed **permanently**."
    },
    {
        "english": "indefinitely",
        "chinese": "無期限地",
        "pos": "adv.",
        "example": "The strike has caused the factory operations to stop **indefinitely**."
    },
    {
        "english": "subsequent",
        "chinese": "隨後的",
        "pos": "adj.",
        "example": "The initial investigation was followed by a **subsequent** inquiry into the firm's finances."
    },
    {
        "english": "consequence",
        "chinese": "後果",
        "pos": "n",
        "example": "Failing to wear a seatbelt can have serious **consequence** in a car accident."
    },
    {
        "english": "overview",
        "chinese": "概要",
        "pos": "n",
        "example": "The manager provided a brief **overview** of the project during the meeting."
    },
    {
        "english": "overlook",
        "chinese": "忽略",
        "pos": "v.",
        "example": "We must not **overlook** the small details, as they often contain important clues."
    },
    {
        "english": "oversee",
        "chinese": "監督",
        "pos": "v.",
        "example": "Her main job responsibility is to **oversee** the entire production process."
    },
    {
        "english": "outlook",
        "chinese": "前景",
        "pos": "n",
        "example": "The economic **outlook** for the next fiscal year seems quite positive."
    },
    {
        "english": "expertise",
        "chinese": "專門知識",
        "pos": "n",
        "example": "We rely on his technical **expertise** to solve these complex engineering problems."
    },
    {
        "english": "expert",
        "chinese": "專家",
        "pos": "n",
        "example": "She is considered a leading **expert** in the field of quantum physics."
    },
    {
        "english": "remainder",
        "chinese": "剩餘的東西",
        "pos": "n",
        "example": "Please finish the main course, and I will pack the **remainder** for you."
    },
    {
        "english": "reminder",
        "chinese": "作為提醒的東西",
        "pos": "n",
        "example": "I set a phone **reminder** so I wouldn't forget my dentist appointment."
    },
    {
        "english": "apparently",
        "chinese": "看起來…",
        "pos": "adv.",
        "example": "The flight was delayed, **apparently** due to bad weather conditions."
    },
    {
        "english": "advisable",
        "chinese": "可取的, 明智的",
        "pos": "adj.",
        "example": "It is **advisable** to book your tickets in advance during peak season."
    },
    {
        "english": "appeal",
        "chinese": "上訴",
        "pos": "v.",
        "example": "The company decided to **appeal** the judge's decision to a higher court."
    },
    {
        "english": "appear",
        "chinese": "出現",
        "pos": "v.",
        "example": "A strange light began to **appear** over the mountain horizon."
    },
    {
        "english": "acquaint",
        "chinese": "使..熟悉",
        "pos": "v.",
        "example": "We need to **acquaint** the new employees with the office safety procedures."
    },
    {
        "english": "acquire",
        "chinese": "取得",
        "pos": "v.",
        "example": "The museum plans to **acquire** a valuable painting at the upcoming auction."
    },
    {
        "english": "instruct",
        "chinese": "指示",
        "pos": "n",
        "example": "The manual provides clear **instruct** on how to set up the new computer system."
    },
    {
        "english": "delegate",
        "chinese": "委任",
        "pos": "v.",
        "example": "A good manager knows how to **delegate** tasks effectively to their team members."
    },
    {
        "english": "delegate",
        "chinese": "代表",
        "pos": "n",
        "example": "The country sent a **delegate** to attend the international peace conference."
    },
    {
        "english": "reluctantly",
        "chinese": "不情願地",
        "pos": "adv.",
        "example": "She **reluctantly** agreed to take on the extra responsibilities at work."
    },
    {
        "english": "concentrate",
        "chinese": "集中",
        "pos": "v.",
        "example": "You need to **concentrate** fully on the road while driving in heavy traffic."
    },
    {
        "english": "prohibit",
        "chinese": "禁止",
        "pos": "v.",
        "example": "Smoking is strictly **prohibit** in all indoor areas of the building."
    },
    {
        "english": "legislation",
        "chinese": "立法",
        "pos": "n",
        "example": "New **legislation** was passed to protect consumers from identity theft."
    },
    {
        "english": "classified",
        "chinese": "機密的",
        "pos": "adj.",
        "example": "These documents are highly **classified** and can only be viewed by authorized personnel."
    },
    {
        "english": "confidential",
        "chinese": "機密的",
        "pos": "adj.",
        "example": "All client records are kept strictly **confidential** to protect their privacy."
    },
    {
        "english": "assume",
        "chinese": "假設",
        "pos": "v.",
        "example": "We should not **assume** that the project will be finished on time; we need a backup plan."
    },
    {
        "english": "persume",
        "chinese": "假設, 承擔",
        "pos": "v.",
        "example": "I **persume** that you have already contacted the client with the good news."
    },
    {
        "english": "resume",
        "chinese": "重新開始",
        "pos": "v.",
        "example": "After a short break for lunch, the meeting will **resume** at two o'clock."
    },
    {
        "english": "undertake",
        "chinese": "承擔",
        "pos": "v.",
        "example": "The construction company agreed to **undertake** the restoration of the old historical building."
    },
    {
        "english": "formal",
        "chinese": "正式的",
        "pos": "adj.",
        "example": "You are required to wear **formal** attire for the evening gala dinner."
    },
    {
        "english": "coordinate",
        "chinese": "協調",
        "pos": "v.",
        "example": "The manager's job is to **coordinate** the efforts of all the different departments."
    },
    {
        "english": "corporation",
        "chinese": "法人",
        "pos": "n",
        "example": "The multinational **corporation** employs thousands of people across the globe."
    },
    {
        "english": "cooperation",
        "chinese": "合作",
        "pos": "n",
        "example": "The successful project was a result of excellent **cooperation** between the two teams."
    },
    {
        "english": "abstract",
        "chinese": "抽象的",
        "pos": "adj.",
        "example": "The philosophy class discussed very difficult and **abstract** concepts."
    },
    {
        "english": "attractive",
        "chinese": "吸引人的",
        "pos": "adj.",
        "example": "The job offer included a very **attractive** benefits package and high salary."
    },
    {
        "english": "attract",
        "chinese": "吸引",
        "pos": "v.",
        "example": "The museum hopes to **attract** more young visitors with its new interactive exhibits."
    },
    {
        "english": "advise",
        "chinese": "建議",
        "pos": "v.",
        "example": "I would **advise** you to seek a second opinion before making a final decision."
    },
    {
        "english": "advice",
        "chinese": "勸告",
        "pos": "n",
        "example": "She gave me some excellent **advice** on how to prepare for the interview."
    },
    {
        "english": "revise",
        "chinese": "修改",
        "pos": "v.",
        "example": "You will need to **revise** your essay to remove all the grammatical errors."
    },
    {
        "english": "means",
        "chinese": "方法, 手段",
        "pos": "n",
        "example": "The internet is a vital **means** of communication in the modern world."
    },
    {
        "english": "contemporary",
        "chinese": "當代的",
        "pos": "adj.",
        "example": "The art gallery features a fascinating collection of **contemporary** sculptures."
    },
    {
        "english": "initial",
        "chinese": "最初的",
        "pos": "adj.",
        "example": "The **initial** plan was very complicated, but we simplified it later."
    },
    {
        "english": "initiate",
        "chinese": "開始 (實施)",
        "pos": "v.",
        "example": "The school decided to **initiate** a new reading program for all elementary students."
    },
    {
        "english": "intensify",
        "chinese": "強化",
        "pos": "v.",
        "example": "The severe storm is expected to **intensify** throughout the night."
    },
    {
        "english": "favorably",
        "chinese": "善意地, 順利地",
        "pos": "adv.",
        "example": "The review board responded **favorably** to his detailed proposal."
    },
    {
        "english": "stagnant",
        "chinese": "停滯的, 不景氣的",
        "pos": "adj.",
        "example": "The company decided to innovate to avoid becoming **stagnant** in the market."
    },
    {
        "english": "disregard",
        "chinese": "忽視",
        "pos": "v.",
        "example": "You should not **disregard** the warning signs posted near the construction zone."
    },
    {
        "english": "incentive",
        "chinese": "獎勵(金)",
        "pos": "n",
        "example": "The company offered a financial **incentive** to employees who met their sales targets."
    },
    {
        "english": "mastermind",
        "chinese": "策畫者",
        "pos": "n",
        "example": "The police are still searching for the **mastermind** behind the large bank robbery."
    },
    {
        "english": "brisk",
        "chinese": "興旺的",
        "pos": "adj.",
        "example": "Despite the global economic slowdown, business has been **brisk** this quarter."
    },
    {
        "english": "boom",
        "chinese": "繁榮",
        "pos": "n",
        "example": "The city experienced an economic **boom** after the new factory opened."
    },
    {
        "english": "thrive",
        "chinese": "繁榮",
        "pos": "v.",
        "example": "Small businesses often **thrive** when they receive local community support."
    },
    {
        "english": "soar",
        "chinese": "(物價)急漲",
        "pos": "v.",
        "example": "Housing prices in the capital city continued to **soar** to new record highs."
    },
    {
        "english": "prosperity",
        "chinese": "繁榮",
        "pos": "n",
        "example": "The government aims to achieve economic **prosperity** and stability for all citizens."
    },
    {
        "english": "boost",
        "chinese": "推動 (景氣)",
        "pos": "v.",
        "example": "The government introduced new policies to **boost** consumer spending and the economy."
    },
    {
        "english": "costly",
        "chinese": "昂貴的",
        "pos": "adj.",
        "example": "Repairing the structural damage to the old building will be extremely **costly**."
    },
    {
        "english": "wane",
        "chinese": "衰退",
        "pos": "n",
        "example": "Enthusiasm for the new management proposal began to **wane** after initial excitement."
    },
    {
        "english": "depression",
        "chinese": "不景氣",
        "pos": "n",
        "example": "The country suffered a deep economic **depression** that lasted for several years."
    },
    {
        "english": "dwindle",
        "chinese": "逐漸減少",
        "pos": "v.",
        "example": "The supply of fresh water began to **dwindle** rapidly during the long drought."
    },
    {
        "english": "impede",
        "chinese": "妨礙",
        "pos": "v.",
        "example": "Heavy snow and ice often **impede** traffic flow during the winter months."
    },
    {
        "english": "determine",
        "chinese": "決定",
        "pos": "v.",
        "example": "The quality control team must **determine** if the product meets safety standards."
    },
    {
        "english": "determine",
        "chinese": "查明",
        "pos": "v.",
        "example": "The scientists are working to **determine** the cause of the mysterious illness."
    },
    {
        "english": "determine",
        "chinese": "決心",
        "pos": "v.",
        "example": "She **determine** to finish the marathon, despite her injury."
    },
    {
        "english": "dedicate",
        "chinese": "致力於",
        "pos": "v.",
        "example": "He chose to **dedicate** his entire career to finding a cure for the rare disease."
    },
    {
        "english": "differentiate",
        "chinese": "區別",
        "pos": "v.",
        "example": "It is sometimes hard to **differentiate** between the two nearly identical species of birds."
    },
    {
        "english": "distinguish",
        "chinese": "區別",
        "pos": "v.",
        "example": "The color-blind person found it difficult to **distinguish** between red and green."
    },
    {
        "english": "estimate",
        "chinese": "估計",
        "pos": "v.",
        "example": "The contractor must **estimate** the total cost of the renovations before starting work."
    },
    {
        "english": "estimate",
        "chinese": "估計",
        "pos": "n.",
        "example": "We received an initial **estimate** for the home repair, but the final cost may vary."
    },
    {
        "english": "eliminate",
        "chinese": "消除",
        "pos": "v.",
        "example": "The company hopes to **eliminate** all paper waste by the end of the year."
    },
    {
        "english": "ensure",
        "chinese": "確保",
        "pos": "v.",
        "example": "We must take immediate action to **ensure** the safety of all our employees."
    },
    {
        "english": "guarantee",
        "chinese": "保證",
        "pos": "v.",
        "example": "The manufacturer will **guarantee** the product against any defect for five years."
    },
    {
        "english": "guarantee",
        "chinese": "保證書",
        "pos": "n.",
        "example": "Always keep your original purchase **guarantee** in case you need warranty service."
    },
    {
        "english": "modify",
        "chinese": "修改",
        "pos": "v.",
        "example": "You may need to **modify** the software settings to improve its performance."
    },
    {
        "english": "modify",
        "chinese": "更改",
        "pos": "v.",
        "example": "The chef decided to **modify** the traditional recipe by adding a modern twist."
    },
    {
        "english": "obligate",
        "chinese": "使負有義務",
        "pos": "v.",
        "example": "The contract will **obligate** the company to finish the construction by May."
    },
    {
        "english": "persuade",
        "chinese": "說服",
        "pos": "v.",
        "example": "It was difficult to **persuade** the client to choose the more expensive but better option."
    },
    {
        "english": "postpone",
        "chinese": "延期",
        "pos": "v.",
        "example": "Due to heavy rain, the outdoor concert had to be **postpone** until the following week."
    },
    {
        "english": "delay",
        "chinese": "延期",
        "pos": "v.",
        "example": "Technical issues **delay** the launch of the new product by several hours."
    },
    {
        "english": "possess",
        "chinese": "擁有",
        "pos": "v.",
        "example": "The old woman **possess** a rare collection of antique silver coins."
    },
    {
        "english": "reduce",
        "chinese": "減少",
        "pos": "v.",
        "example": "The company implemented new measures to **reduce** its energy consumption."
    },
    {
        "english": "resolve",
        "chinese": "解決",
        "pos": "v.",
        "example": "The mediator helped the two parties to **resolve** their long-standing conflict peacefully."
    },
    {
        "english": "restore",
        "chinese": "修復",
        "pos": "v.",
        "example": "Experts worked for months to **restore** the ancient mural painting to its original state."
    },
    {
        "english": "retain",
        "chinese": "保持",
        "pos": "v.",
        "example": "It is difficult for students to **retain** such a large amount of information in a short time."
    },
    {
        "english": "suspend",
        "chinese": "暫停",
        "pos": "v.",
        "example": "The train service was temporarily **suspend** due to an unforeseen accident on the tracks."
    },
    {
        "english": "verify",
        "chinese": "證實",
        "pos": "v.",
        "example": "The bank needs to **verify** the identity of the person withdrawing the large sum of money."
    },
    {
        "english": "attentive",
        "chinese": "專注的",
        "pos": "adj.",
        "example": "The audience was highly **attentive** during the fascinating lecture on astrophysics."
    },
    {
        "english": "attendant",
        "chinese": "服務員",
        "pos": "n.",
        "example": "A friendly flight **attendant** helped me find my seat on the airplane."
    },
    {
        "english": "available",
        "chinese": "可用的",
        "pos": "adj.",
        "example": "The new product will be **available** for purchase starting next Monday."
    },
    {
        "english": "broaden",
        "chinese": "拓寬",
        "pos": "v.",
        "example": "Traveling can help to **broaden** your perspectives and cultural understanding."
    },
    {
        "english": "conclusive",
        "chinese": "決定性的",
        "pos": "adj.",
        "example": "The police lacked **conclusive** evidence to link the suspect to the crime scene."
    },
    {
        "english": "consult",
        "chinese": "諮詢",
        "pos": "v.",
        "example": "You should **consult** your lawyer before signing any important legal documents."
    },
    {
        "english": "counsel",
        "chinese": "勸告",
        "pos": "n.",
        "example": "The school guidance **counsel** helped the student choose the right university major."
    },
    {
        "english": "counter",
        "chinese": "櫃台",
        "pos": "n.",
        "example": "Please proceed to the check-in **counter** with your passport and ticket."
    },
    {
        "english": "definitely",
        "chinese": "明確地",
        "pos": "adv.",
        "example": "I will **definitely** attend the conference next month if my schedule permits."
    },
    {
        "english": "demonstrate",
        "chinese": "示範",
        "pos": "v.",
        "example": "The professor will **demonstrate** how to use the advanced lab equipment."
    },
    {
        "english": "dismiss",
        "chinese": "解散",
        "pos": "v.",
        "example": "The manager had to **dismiss** the employee due to repeated misconduct."
    },
    {
        "english": "elaborate",
        "chinese": "詳細說明",
        "pos": "v.",
        "example": "Could you please **elaborate** further on your proposal's financial benefits?"
    },
    {
        "english": "extensive",
        "chinese": "廣泛的",
        "pos": "adj.",
        "example": "The library has an **extensive** collection of books on world history."
    },
    {
        "english": "handy",
        "chinese": "便利的",
        "pos": "adj.",
        "example": "Always keep a small flashlight **handy** in case of a sudden power outage."
    },
    {
        "english": "highlight",
        "chinese": "突顯",
        "pos": "v.",
        "example": "The presentation will **highlight** the most critical findings of the market research."
    },
    {
        "english": "identical",
        "chinese": "相同的",
        "pos": "adj.",
        "example": "The two brothers look almost **identical**, making it hard to tell them apart."
    },
    {
        "english": "immense",
        "chinese": "龐大的",
        "pos": "adj.",
        "example": "The project requires an **immense** amount of planning and financial resources."
    },
    {
        "english": "impressive",
        "chinese": "令人印象深刻的",
        "pos": "adj.",
        "example": "The architect presented an **impressive** design for the new city museum."
    },
    {
        "english": "install",
        "chinese": "安裝",
        "pos": "v.",
        "example": "We need to hire an electrician to **install** the new lighting fixtures in the hallway."
    },
    {
        "english": "justify",
        "chinese": "證明..是正當的",
        "pos": "v.",
        "example": "You must be able to **justify** your decision with concrete facts and data."
    },
    {
        "english": "legend",
        "chinese": "傳奇",
        "pos": "n.",
        "example": "The local people still tell stories about the ancient **legend** of the sleeping dragon."
    },
    {
        "english": "merge",
        "chinese": "合併",
        "pos": "v.",
        "example": "The two smaller companies decided to **merge** to become a larger, more competitive entity."
    },
    {
        "english": "miniature",
        "chinese": "微小的",
        "pos": "adj.",
        "example": "The collector specialized in painting **miniature** portraits of historical figures."
    },
    {
        "english": "nominal",
        "chinese": "名義上的",
        "pos": "adj.",
        "example": "The charity charges only a **nominal** fee to cover the basic administrative costs."
    },
    {
        "english": "novel",
        "chinese": "小說",
        "pos": "n.",
        "example": "Her latest **novel** is a gripping thriller set in the cold mountains of Norway."
    },
    {
        "english": "novelty",
        "chinese": "新奇",
        "pos": "n.",
        "example": "The toy initially sold well due to its **novelty**, but sales soon dropped off."
    },
    {
        "english": "opponent",
        "chinese": "對手",
        "pos": "n.",
        "example": "He faced a formidable **opponent** in the final round of the boxing championship."
    },
    {
        "english": "overwhelming",
        "chinese": "壓倒性的",
        "pos": "adj.",
        "example": "The positive feedback from the customers has been **overwhelming**."
    },
    {
        "english": "pending",
        "chinese": "未定的",
        "pos": "adj.",
        "example": "The committee's final decision on the merger is still **pending**."
    },
    {
        "english": "plea",
        "chinese": "懇求",
        "pos": "n.",
        "example": "The charity made an urgent **plea** for donations to help the flood victims."
    },
    {
        "english": "practical",
        "chinese": "實用的",
        "pos": "adj.",
        "example": "Learning how to cook is a highly **practical** skill for young students to acquire."
    },
    {
        "english": "prior",
        "chinese": "先前的",
        "pos": "adj.",
        "example": "You need to finish the **prior** paperwork before you can start the application process."
    },
    {
        "english": "prolong",
        "chinese": "延長",
        "pos": "v.",
        "example": "The negotiation tactics were designed specifically to **prolong** the discussion unnecessarily."
    },
    {
        "english": "protest",
        "chinese": "抗議",
        "pos": "v.",
        "example": "Workers gathered outside the factory to **protest** the poor working conditions."
    },
    {
        "english": "protest",
        "chinese": "抗議",
        "pos": "n.",
        "example": "The large-scale **protest** forced the government to reconsider the new policy."
    },
    {
        "english": "rarely",
        "chinese": "很少",
        "pos": "adv.",
        "example": "Because the doctor is so busy, he **rarely** takes any time off during the week."
    },
    {
        "english": "recruit",
        "chinese": "招募",
        "pos": "v.",
        "example": "The company is planning to **recruit** fifty new engineers in the next quarter."
    },
    {
        "english": "remarkable",
        "chinese": "非凡的",
        "pos": "adj.",
        "example": "She made **remarkable** progress in her studies in just six months."
    },
    {
        "english": "rival",
        "chinese": "競爭者",
        "pos": "n.",
        "example": "Our main **rival** just launched a similar product at a lower price point."
    },
    {
        "english": "solid",
        "chinese": "紮實的",
        "pos": "adj.",
        "example": "The new manager has a **solid** background in financial analysis."
    },
    {
        "english": "sophisticated",
        "chinese": "精密的",
        "pos": "adj.",
        "example": "The new surveillance system uses highly **sophisticated** facial recognition technology."
    },
    {
        "english": "spacious",
        "chinese": "寬敞的",
        "pos": "adj.",
        "example": "The apartment has a **spacious** living room that is perfect for entertaining guests."
    },
    {
        "english": "specialize",
        "chinese": "專門研究",
        "pos": "v.",
        "example": "The doctor decided to **specialize** in pediatric cardiology."
    },
    {
        "english": "spontaneous",
        "chinese": "自發的",
        "pos": "adj.",
        "example": "The flash mob performance was completely **spontaneous** and took the crowd by surprise."
    },
    {
        "english": "steady",
        "chinese": "穩定的",
        "pos": "adj.",
        "example": "The economy has shown a **steady** rate of growth over the past decade."
    },
    {
        "english": "subtle",
        "chinese": "細微的",
        "pos": "adj.",
        "example": "The designer made a **subtle** change to the logo that most people didn't notice."
    },
    {
        "english": "tend",
        "chinese": "傾向",
        "pos": "v.",
        "example": "People **tend** to be more productive in the early hours of the morning."
    },
    {
        "english": "transparent",
        "chinese": "透明的",
        "pos": "adj.",
        "example": "The company aims to be completely **transparent** about its financial reporting."
    },
    {
        "english": "uniform",
        "chinese": "制服",
        "pos": "n.",
        "example": "All students at the private school are required to wear a school **uniform**."
    },
    {
        "english": "vital",
        "chinese": "極重要的",
        "pos": "adj.",
        "example": "Maintaining good communication is **vital** for the success of any team."
    }
]

# ==========================================
# 2. 核心邏輯函式
# ==========================================

def get_distractors(correct_word, full_list, count=3, target_key='english'):
    """從資料庫中隨機選取錯誤選項 (目標鍵可以是 english 或 chinese)"""
    # 確保不會選到正確答案
    other_words = [w for w in full_list if w['english'] != correct_word['english']]
    
    # 確保資料量足夠
    if len(other_words) < count:
        # 如果資料不足，回傳所有剩餘的
        distractors = other_words
    else:
        # 隨機選取指定數量的錯誤選項
        distractors = random.sample(other_words, count)
        
    return [d[target_key] for d in distractors]

def initialize_session_state():
    """初始化頁面狀態，用於儲存當前題目"""
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'quiz_type' not in st.session_state:
        st.session_state.quiz_type = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'feedback_type' not in st.session_state:
        st.session_state.feedback_type = None

def reset_quiz():
    """重置測驗題目"""
    st.session_state.current_question = None
    st.session_state.feedback = None
    st.session_state.feedback_type = None

def display_feedback_and_next_button(quiz_key):
    """通用函式：顯示回饋並提供下一題按鈕"""
    if st.session_state.feedback:
        if st.session_state.feedback_type == 'success':
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
        
        # 顯示下一題按鈕
        if st.button("下一題 ➡", key=f'next_{quiz_key}'):
            reset_quiz()
            # 強制重新執行，以刷新題目
            st.rerun()

# ==========================================
# 3. 測驗頁面組件 (全部為選擇題)
# ==========================================

def quiz_cloze_mc():
    """克漏字測驗 (Contextual Multiple Choice)"""
    st.subheader("🔤 克漏字測驗 (選擇題)")
    st.caption("請根據例句和中文提示，從選項中選出正確單字填入空格。")
    
    # 檢查資料量
    if len(VOCAB_DB) < 4:
        st.warning("⚠️ 單字數量不足 4 個，無法生成選擇題。")
        return

    # 抽取題目
    if st.session_state.current_question is None or st.session_state.quiz_type != 'cloze_mc':
        correct_word = random.choice(VOCAB_DB)
        # 取得錯誤選項 (英文單字)
        distractors = get_distractors(correct_word, VOCAB_DB, 3, target_key='english')
        
        options = distractors + [correct_word['english']]
        random.shuffle(options)
        
        st.session_state.current_question = {
            "correct": correct_word,
            "options": options
        }
        st.session_state.quiz_type = 'cloze_mc'
        st.session_state.feedback = None

    q = st.session_state.current_question
    target_word = q['correct']['english']
    
    # 製作挖空例句 (忽略大小寫取代)
    pattern = re.compile(re.escape(target_word), re.IGNORECASE)
    question_sentence = pattern.sub("_______", q['correct']['example'])
    
    # 顯示題目區塊
    st.markdown(f"### 例句: {question_sentence}")
    st.info(f"💡 中文提示: {q['correct']['chinese']} ({q['correct']['pos']})")
    
    # 使用 form 處理選擇題
    with st.form(key='cloze_mc_form'):
        user_choice = st.radio("請選擇正確答案：", q['options'])
        submit_btn = st.form_submit_button("提交答案")
        
        if submit_btn:
            if user_choice == target_word:
                st.session_state.feedback = f"🎉 **正確！** 答案是 **{target_word}**。"
                st.session_state.feedback_type = "success"
            else:
                st.session_state.feedback = f"❌ **錯誤！** 正確答案是 **{target_word}**。"
                st.session_state.feedback_type = "error"
            # 重新運行以顯示結果
            # st.rerun()
            

def quiz_chinese_to_english():
    """中翻英測驗 (Multiple Choice)"""
    st.subheader("🇨🇳 ➡ 🇬🇧 中翻英測驗")
    
    if len(VOCAB_DB) < 4:
        st.warning("⚠️ 單字數量不足 4 個，無法生成選擇題。")
        return

    # 抽取題目
    if st.session_state.current_question is None or st.session_state.quiz_type != 'c_to_e':
        correct = random.choice(VOCAB_DB)
        # 取得錯誤選項 (英文單字)
        distractors_eng = get_distractors(correct, VOCAB_DB, 3, target_key='english')
        
        options = distractors_eng + [correct['english']]
        random.shuffle(options)
        
        st.session_state.current_question = {
            "correct": correct,
            "options": options
        }
        st.session_state.quiz_type = 'c_to_e'
        st.session_state.feedback = None

    q = st.session_state.current_question
    correct_word = q['correct']
    
    st.markdown(f"### 中文：<span style='color:#007bff'>{correct_word['chinese']}</span>", unsafe_allow_html=True)
    st.write(f"詞性：{correct_word['pos']}")
    
    # 顯示選項
    with st.form(key='c_to_e_form'):
        user_choice = st.radio("請選擇正確的英文單字：", q['options'])
        submit_btn = st.form_submit_button("提交答案")
        
        if submit_btn:
            if user_choice == correct_word['english']:
                st.session_state.feedback = f"🎉 **正確！** **{correct_word['english']}** = {correct_word['chinese']}"
                st.session_state.feedback_type = "success"
            else:
                st.session_state.feedback = f"❌ **錯誤！** 正確答案是 **{correct_word['english']}**。"
                st.session_state.feedback_type = "error"
            # st.rerun()


def quiz_english_to_chinese():
    """英翻中測驗 (Multiple Choice)"""
    st.subheader("🇬🇧 ➡ 🇨🇳 英翻中測驗")
    
    if len(VOCAB_DB) < 4:
        st.warning("⚠️ 單字數量不足 4 個，無法生成選擇題。")
        return

    # 抽取題目
    if st.session_state.current_question is None or st.session_state.quiz_type != 'e_to_c':
        correct = random.choice(VOCAB_DB)
        # 取得錯誤選項 (中文意思)
        distractors_chi = get_distractors(correct, VOCAB_DB, 3, target_key='chinese')
        
        options = distractors_chi + [correct['chinese']]
        random.shuffle(options)
        
        st.session_state.current_question = {
            "correct": correct,
            "options": options
        }
        st.session_state.quiz_type = 'e_to_c'
        st.session_state.feedback = None

    q = st.session_state.current_question
    correct_word = q['correct']
    
    st.markdown(f"### 英文：<span style='color:#e83e8c'>{correct_word['english']}</span>", unsafe_allow_html=True)
    st.write(f"詞性：{correct_word['pos']}")
    
    # 顯示選項
    with st.form(key='e_to_c_form'):
        user_choice = st.radio("請選擇正確的中文意思：", q['options'])
        submit_btn = st.form_submit_button("提交答案")
        
        if submit_btn:
            if user_choice == correct_word['chinese']:
                st.session_state.feedback = f"🎉 **正確！** **{correct_word['english']}** 的意思是 {correct_word['chinese']}"
                st.session_state.feedback_type = "success"
            else:
                st.session_state.feedback = f"❌ **錯誤！** 正確答案是 **{correct_word['chinese']}**。"
                st.session_state.feedback_type = "error"
            # st.rerun()


# ==========================================
# 4. 主程式介面 (Main)
# ==========================================

def main():
    st.set_page_config(page_title="英文單字特訓 App", page_icon="🎓", layout="centered")
    initialize_session_state()

    st.title("🎓 英文單字特訓 App")
    st.markdown("基於您 **138** 個單字庫，包含三種選擇題測驗模式。")
    
    # 側邊欄：顯示資料庫狀態
    with st.sidebar:
        st.header("📊 資料庫狀態")
        st.write(f"單字總數：**{len(VOCAB_DB)}** 個")
        st.markdown("---")
        st.write("📖 **單字列表**")
        df = pd.DataFrame(VOCAB_DB)
        st.dataframe(df[['english', 'chinese', 'pos']], height=300, hide_index=True)
        st.caption("註：所有單字皆已備註例句，用於克漏字測驗。")

    # 主要內容區：使用 Tabs 分頁
    tab1, tab2, tab3 = st.tabs(["🔤 克漏字 (選詞)", "🇨🇳➡🇬🇧 中翻英", "🇬🇧➡🇨🇳 英翻中"])

    with tab1:
        quiz_cloze_mc()
        display_feedback_and_next_button('cloze_mc')

    with tab2:
        quiz_chinese_to_english()
        display_feedback_and_next_button('c_to_e')

    with tab3:
        quiz_english_to_chinese()
        display_feedback_and_next_button('e_to_c')

if __name__ == "__main__":

    main()

