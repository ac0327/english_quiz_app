import streamlit as st
import random
import pandas as pd
import re
import uuid

# ==========================================
# 1.  資料庫設定 (您的 138 個單字 + AI 生成的例句)
# ==========================================

# 您的資料庫內容（已包含例句）
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
        "pos": "adj.",
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
        "pos": "n.",
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
        "pos": "n.",
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
        "pos": "n.",
        "example": "The scientist applied for a large **grant** to fund his space exploration project."
    },
    {
        "english": "directory",
        "chinese": "通訊錄",
        "pos": "n.",
        "example": "You can find all the staff contact details in the company **directory**."
    },
    {
        "english": "contrary",
        "chinese": "相反(情況)",
        "pos": "n.",
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
        "pos": "n.",
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
        "pos": "n.",
        "example": "Failing to wear a seatbelt can have serious **consequence** in a car accident."
    },
    {
        "english": "overview",
        "chinese": "概要",
        "pos": "n.",
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
        "pos": "n.",
        "example": "The economic **outlook** for the next fiscal year seems quite positive."
    },
    {
        "english": "expertise",
        "chinese": "專門知識",
        "pos": "n.",
        "example": "We rely on his technical **expertise** to solve these complex engineering problems."
    },
    {
        "english": "expert",
        "chinese": "專家",
        "pos": "n.",
        "example": "She is considered a leading **expert** in the field of quantum physics."
    },
    {
        "english": "remainder",
        "chinese": "剩餘的東西",
        "pos": "n.",
        "example": "Please finish the main course, and I will pack the **remainder** for you."
    },
    {
        "english": "reminder",
        "chinese": "作為提醒的東西",
        "pos": "n.",
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
        "chinese": "使.. 熟悉",
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
        "pos": "v.",
        "example": "The manual provides clear instructions on how to set up the new computer system."
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
        "pos": "n.",
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
        "example": "Smoking is strictly **prohibited** in all indoor areas of the building."
    },
    {
        "english": "legislation",
        "chinese": "立法",
        "pos": "n.",
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
        "english": "presume",
        "chinese": "假設, 承擔",
        "pos": "v.",
        "example": "I **presume** that you have already contacted the client with the good news."
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
        "pos": "n.",
        "example": "The multinational **corporation** employs thousands of people across the globe."
    },
    {
        "english": "cooperation",
        "chinese": "合作",
        "pos": "n.",
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
        "pos": "n.",
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
        "pos": "n.",
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
        "pos": "n.",
        "example": "The company offered a financial **incentive** to employees who met their sales targets."
    },
    {
        "english": "mastermind",
        "chinese": "策畫者",
        "pos": "n.",
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
        "pos": "n.",
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
        "pos": "n.",
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
        "pos": "v.",
        "example": "Enthusiasm for the new management proposal began to **wane** after initial excitement."
    },
    {
        "english": "depression",
        "chinese": "不景氣",
        "pos": "n.",
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
        "english": "modify",
        "chinese": "修改",
        "pos": "v.",
        "example": "You may need to **modify** the software settings to improve its performance."
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
        "example": "Due to heavy rain, the outdoor concert had to be **postponed** until the following week."
    },
    {
        "english": "delay",
        "chinese": "延期",
        "pos": "v.",
        "example": "Technical issues **delayed** the launch of the new product by several hours."
    },
    {
        "english": "possess",
        "chinese": "擁有",
        "pos": "v.",
        "example": "The old woman **possesses** a rare collection of antique silver coins."
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
        "example": "The train service was temporarily **suspended** due to an unforeseen accident on the tracks."
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
        "example": "The school guidance **counselor** helped the student choose the right university major."
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
        "chinese": "證明.. 是正當的",
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
# 初始化 session state
if 'question_id' not in st.session_state:
    st.session_state. question_id = 0
if 'question' not in st.session_state:
    st.session_state.question = None
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = None

def generate_question(mode):
    """生成新題目"""
    correct = random.choice(VOCAB_DB)
    others = [w for w in VOCAB_DB if w['english'] != correct['english']]
    distractors = random.sample(others, min(3, len(others)))
    
    if mode == 'cloze':
        options = [d['english'] for d in distractors] + [correct['english']]
    elif mode == 'c2e':
        options = [d['english'] for d in distractors] + [correct['english']]
    else:  # e2c
        options = [d['chinese'] for d in distractors] + [correct['chinese']]
    
    random.shuffle(options)
    return {'correct': correct, 'options': options}

def reset_question(mode):
    """重置題目"""
    st.session_state.question_id += 1
    st.session_state.question = generate_question(mode)
    st.session_state.user_answer = None
    st.session_state.show_result = False

def submit_answer(user_choice):
    """提交答案"""
    st.session_state.user_answer = user_choice
    st.session_state. show_result = True

def main():
    st.set_page_config(page_title="英文單字測驗", page_icon="📚", layout="centered")
    st.title("🎓 英文單字特訓 App")
    
    tab1, tab2, tab3 = st.tabs(["🔤 克漏字", "🇨🇳➡🇬🇧 中翻英", "🇬🇧➡🇨🇳 英翻中"])
    
    # ==================== 克漏字測驗 ====================
    with tab1:
        st.subheader("克漏字測驗")
        
        # 切換模式時重置
        if st.session_state. quiz_mode != 'cloze':
            st.session_state.quiz_mode = 'cloze'
            reset_question('cloze')
        
        # 生成新題
        if st.session_state.question is None:
            reset_question('cloze')
        
        q = st.session_state.question
        word = q['correct']
        
        # 挖空例句
        sentence = re.sub(re. escape(word['english']), "_______", word['example'], flags=re.IGNORECASE)
        st.markdown(f"### {sentence}")
        st.info(f"💡 提示: {word['chinese']} ({word['pos']})")
        
        # 如果還沒顯示結果，顯示選項和提交按鈕
        if not st.session_state.show_result:
            # 使用 question_id 作為 key 的一部分，確保每次題目更新時重置選項
            choice = st.radio(
                "請選擇答案：", 
                q['options'], 
                key=f'cloze_choice_{st.session_state.question_id}'
            )
            
            if st.button("✅ 提交答案", key=f'cloze_submit_{st. session_state.question_id}'):
                submit_answer(choice)
                st.rerun()
        
        # 顯示結果
        if st.session_state.show_result:
            user_choice = st.session_state.user_answer
            
            # 顯示用戶的選擇
            st.write(f"**您的答案:** {user_choice}")
            
            # 判斷對錯
            if user_choice == word['english']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是: **{word['english']}**")
            
            # 顯示完整單字資訊
            st.markdown("---")
            st.markdown("### 📝 單字資訊")
            st.write(f"**英文:** {word['english']}")
            st.write(f"**詞性:** {word['pos']}")
            st.write(f"**中文:** {word['chinese']}")
            st.write(f"**例句:** {word['example']}")
            
            # 下一題按鈕
            if st.button("➡ 下一題", key=f'cloze_next_{st.session_state.question_id}'):
                reset_question('cloze')
                st. rerun()
    
    # ==================== 中翻英測驗 ====================
    with tab2:
        st. subheader("中翻英測驗")
        
        if st.session_state.quiz_mode != 'c2e':
            st.session_state.quiz_mode = 'c2e'
            reset_question('c2e')
        
        if st.session_state.question is None:
            reset_question('c2e')
        
        q = st. session_state.question
        word = q['correct']
        
        st.markdown(f"### 中文: **{word['chinese']}**")
        st.write(f"詞性: {word['pos']}")
        
        if not st.session_state.show_result:
            choice = st. radio(
                "請選擇英文單字：", 
                q['options'], 
                key=f'c2e_choice_{st.session_state.question_id}'
            )
            
            if st.button("✅ 提交答案", key=f'c2e_submit_{st.session_state.question_id}'):
                submit_answer(choice)
                st.rerun()
        
        if st.session_state.show_result:
            user_choice = st.session_state.user_answer
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == word['english']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是: **{word['english']}**")
            
            st.markdown("---")
            st.markdown("### 📝 單字資訊")
            st.write(f"**英文:** {word['english']}")
            st.write(f"**詞性:** {word['pos']}")
            st.write(f"**中文:** {word['chinese']}")
            st.write(f"**例句:** {word['example']}")
            
            if st.button("➡ 下一題", key=f'c2e_next_{st. session_state.question_id}'):
                reset_question('c2e')
                st.rerun()
    
    # ==================== 英翻中測驗 ====================
    with tab3:
        st.subheader("英翻中測驗")
        
        if st.session_state.quiz_mode != 'e2c':
            st.session_state. quiz_mode = 'e2c'
            reset_question('e2c')
        
        if st.session_state.question is None:
            reset_question('e2c')
        
        q = st.session_state.question
        word = q['correct']
        
        st. markdown(f"### 英文: **{word['english']}**")
        st.write(f"詞性: {word['pos']}")
        
        if not st.session_state. show_result:
            choice = st.radio(
                "請選擇中文意思：", 
                q['options'], 
                key=f'e2c_choice_{st.session_state.question_id}'
            )
            
            if st.button("✅ 提交答案", key=f'e2c_submit_{st. session_state.question_id}'):
                submit_answer(choice)
                st.rerun()
        
        if st.session_state.show_result:
            user_choice = st.session_state.user_answer
            st.write(f"**您的答案:** {user_choice}")
            
            if user_choice == word['chinese']:
                st.success("🎉 **正確！**")
            else:
                st.error(f"❌ **錯誤！** 正確答案是: **{word['chinese']}**")
            
            st.markdown("---")
            st.markdown("### 📝 單字資訊")
            st.write(f"**英文:** {word['english']}")
            st. write(f"**詞性:** {word['pos']}")
            st.write(f"**中文:** {word['chinese']}")
            st.write(f"**例句:** {word['example']}")
            
            if st.button("➡ 下一題", key=f'e2c_next_{st. session_state.question_id}'):
                reset_question('e2c')
                st.rerun()

if __name__ == "__main__":
    main()
