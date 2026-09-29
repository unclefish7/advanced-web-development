#!/usr/bin/env python3
"""Build an editable Chinese PPTX using only the Python standard library."""
from pathlib import Path
from html import escape
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '搜索与检索增强人工智能汇报.pptx'
FONT = 'Noto Sans CJK SC'
BG, INK, MUTED, TEAL, BLUE, AMBER = 'F7F8FA', '182D46', '65758A', '078A83', '3468C0', 'B87B23'
slides = []
EMU = 914400

def xmltext(s):
    return escape(str(s), quote=True)

class Slide:
    def __init__(self, title, section, notes, source=''):
        self.title, self.notes = title, notes
        self.shapes, self.sid = [], 1
        self.rect(0, 0, 13.333, 7.5, BG)
        self.rect(0, 0, .13, 7.5, TEAL)
        self.text(.55, .3, 11.8, .35, section.upper(), 11, TEAL, True)
        self.text(.55, .82, 12.1, .72, title, 28, INK, True)
        self.text(.55, 7.02, 11.65, .28, source or '高级 Web 开发 · 搜索与检索增强人工智能', 9, MUTED)
        self.text(12.3, 7.0, .5, .3, f'{len(slides)+1:02}', 10, MUTED)
        slides.append(self)

    def rect(self, x, y, w, h, fill, line=None, radius=False):
        self.sid += 1
        geom = 'roundRect' if radius else 'rect'
        self.shapes.append(f'''<p:sp><p:nvSpPr><p:cNvPr id="{self.sid}" name="Shape {self.sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(x*EMU)}" y="{int(y*EMU)}"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>{'<a:ln><a:solidFill><a:srgbClr val="'+line+'"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'}</p:spPr></p:sp>''')

    def text(self, x, y, w, h, text, size=18, color=INK, bold=False, align='l'):
        self.sid += 1
        paras = []
        for line in text.split('\n'):
            paras.append(f'''<a:p><a:pPr algn="{align}"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc><a:spcAft><a:spcPts val="400"/></a:spcAft></a:pPr><a:r><a:rPr lang="zh-CN" sz="{int(size*100)}" b="{int(bold)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:rPr><a:t>{xmltext(line)}</a:t></a:r><a:endParaRPr lang="zh-CN" sz="{int(size*100)}"/></a:p>''')
        self.shapes.append(f'''<p:sp><p:nvSpPr><p:cNvPr id="{self.sid}" name="Text {self.sid}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(x*EMU)}" y="{int(y*EMU)}"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/><a:lstStyle/>{''.join(paras)}</p:txBody></p:sp>''')

    def card(self, x, y, w, h, heading, body, accent=TEAL):
        self.rect(x, y, w, h, 'FFFFFF', 'E3E8EE', True)
        self.rect(x, y+.16, .055, .5, accent)
        self.text(x+.2, y+.2, w-.4, .55, heading, 20, accent, True)
        body_offset = .76 if h < 1.5 else .92
        self.text(x+.2, y+body_offset, w-.4, h-body_offset-.08,
                  body, 14 if h < 1.5 else 17)

    def banner(self, text, y=6.12):
        self.rect(.55, y, 12.2, .63, 'E6F3F1', radius=True)
        self.text(.75, y+.12, 11.8, .42, text, 18, TEAL, True)

    def arrow(self, x, y, label='→'):
        self.text(x, y, .4, .5, label, 24, MUTED, True, 'ctr')


CFV = '来源：Wei et al., CFVBench，论文表 2–4 / §3–6；doi:10.1145/3774904.3792726'
s = Slide('从 Web 搜索到多模态检索增强生成', 'WWW 2026 · RESEARCH REVIEW',
    '大家好，我汇报的主题是从 Web 搜索到多模态检索增强生成。本次汇报分成两部分：先介绍搜索技术如何从关键词匹配发展到为生成模型提供证据，再以 CFVBench 为案例，讨论视频中的细小信息为什么容易被模型遗漏。希望通过这个案例说明，找到相关资料，并不意味着模型已经正确使用了资料。')
s.text(.65, 1.93, 11.8, 1.1, '搜索与检索增强人工智能\n研究综述与 CFVBench 案例分析', 30, INK, True)
s.rect(.65, 3.45, 11.95, .04, TEAL)
for x, num, title, body in [( .65,'01','技术演进','关键词 → 语义 → 证据'),(4.75,'02','研究趋势','可靠性 · 效率 · 多模态'),(8.85,'03','论文案例','CFVBench 与 AVR')]:
    s.text(x, 3.85, 3.5, .6, num, 30, TEAL, True)
    s.text(x, 4.62, 3.5, .5, title, 22, INK, True)
    s.text(x, 5.25, 3.5, .5, body, 16, MUTED)
s.text(.65, 6.25, 11.8, .4, '汇报人：贾文超  ·  高级 Web 开发', 16, MUTED)

s = Slide('技术主线：从“找到网页”到“提供回答依据”', '01 · 技术演进',
    '这张图不是严格的年代划分，而是功能演进。关键词检索利用词项快速定位网页；召回和排序从大量候选里选出更相关的结果；稠密检索进一步理解语义；RAG 再把检索结果作为依据交给生成模型。需要特别注意，新方法没有完全替代旧方法。真实系统常把关键词检索、向量检索和重排序组合起来。',
    '来源：Manning et al., 2008；Karpukhin et al., 2020；Lewis et al., 2020')
steps=[('关键词检索','倒排索引\n词项匹配'),('召回与排序','先选候选\n再判断相关性'),('语义检索','向量表示\n神经重排序'),('RAG','组织证据\n生成回答')]
for i,(h,b) in enumerate(steps):
    x=.55+i*3.15
    s.card(x, 2.15, 2.75, 2.6, h, b, TEAL if i==3 else BLUE)
    if i<3: s.arrow(x+2.78, 3.18)
s.text(.75, 5.25, 11.8, .6, '检索与排序不是过时环节，而是 RAG 的基础。', 23, INK, True)
s.banner('核心变化：评价“相关”之外，还要评价证据能否支撑回答。')

s = Slide('关键词检索：像查一本巨大的词语目录', '01 · 技术演进',
    '假设搜索透明背景导出 PNG，倒排索引记录每个词出现在哪些文档里，因此不用逐个扫描网页。系统可以根据词频、词的区分能力和文档长度，用 BM25 等方法评分。优势是高效，而且能精确匹配术语。困难在于用户与文档可能用不同的表达方式。这个不足为语义检索提供了动机，但不意味着关键词检索没有价值。',
    '来源：Manning et al., Introduction to Information Retrieval；Robertson & Zaragoza, 2009')
s.text(.7, 1.8, 11.8, .6, '查询示例：透明背景 导出 PNG', 23, INK, True)
s.card(.65, 2.7, 5.75, 2.8, '倒排索引：词 → 文档', '“透明背景” → 文档 A、C\n“导出” → 文档 A、B、D\n“PNG” → 文档 A、D')
s.card(6.85, 2.7, 5.75, 2.8, '召回与排序：候选 → 优先级', '召回：先快速选出可能相关的文档\n排序：再把更相关的结果放到前面\nBM25：典型的词项相关性评分方法', BLUE)
s.banner('优势：快速、术语匹配明确；局限：同一意思可能使用不同词语。')

s = Slide('语义检索：不只看“同词”，也看“同义”', '01 · 技术演进',
    '用户可能说如何保留图片透明区域，而文档写的是启用 alpha 通道导出，两者词语不完全相同，但意义有关。稠密检索把问题和文档编码成向量，按向量相似度寻找候选。神经重排序则让模型更细致地检查问题与候选文档的关系。它们通常构成先快后精的两阶段流程。向量相似也不是事实保证，因此需要继续检查证据。',
    '来源：Karpukhin et al., DPR, 2020；Nogueira & Cho, Passage Re-ranking with BERT, 2019')
s.card(.65, 1.95, 5.75, 1.85, '用户表达', '“如何保留图片中的透明区域？”')
s.card(6.85, 1.95, 5.75, 1.85, '文档表达', '“启用 alpha 通道后导出 PNG。”', BLUE)
for i,(h,b) in enumerate([('向量编码','把问题、文档转成语义表示'),('快速召回','找到语义接近的候选'),('神经重排序','更细致地判断候选相关性')]):
    s.card(.65+i*4.15, 4.18, 3.65, 1.63, h, b, BLUE)
    if i<2: s.arrow(4.33+i*4.15, 4.75)
s.banner('“语义相近”仍不等于“包含回答问题所需的确切事实”。')

s = Slide('RAG：让模型先查资料，再组织回答', '01 · 技术演进',
    'RAG 可以理解成开卷答题。它先从外部资料中检索，再把问题与证据一起交给语言模型，最后生成自然语言回答。这里的关键不是简单地把大量资料塞进去，而是资料是否相关、可信、足够，以及回答是否忠实于资料。来源互相矛盾、证据缺失或者模型误读，都可能让答案出错。检索增强是降低风险的方法，不是正确性保证。',
    '来源：Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, 2020')
for i,(h,b) in enumerate([('问题','怎样导出透明背景图片？'),('检索资料','找到软件说明或相关教程'),('生成回答','根据证据整理操作步骤')]):
    s.card(.65+i*4.15, 2.3, 3.65, 2.5, h, b)
    if i<2: s.arrow(4.33+i*4.15, 3.2)
s.text(.85, 5.18, 11.6, .65, '与普通搜索的区别：输出不只是链接，而是基于资料的回答。', 21, INK, True)
s.banner('RAG ≠ 保证正确：资料找错、证据缺失、模型误读，都可能出错。')

s = Slide('WWW 2026：研究重点转向“如何用好证据”', '02 · 研究方向综述',
    '结合会议研究方向说明和录用论文，可以概括出四个重要方向。可靠性关注冲突和幻觉；效率关注检索轮数、上下文长度与成本；多模态关注文字以外的图片、语音和视频；智能体搜索关注是否继续搜索以及调用什么工具。这是对论文主题的归纳，不是会议官方的四分类。接下来选择多模态方向的 CFVBench，具体观察证据使用的困难。',
    '依据：WWW 2026 研究方向说明与录用论文列表；分类为本汇报归纳')
for x,y,h,b in [(.65,1.9,'可靠性','处理冲突、噪声与幻觉\n答案中的陈述能否被证据支持？'),(6.85,1.9,'效率','自适应检索与上下文压缩\n多查、多读，是否真的值得？'),(.65,3.92,'多模态','图像、语音、视频与图表\n能否定位并读懂细小证据？'),(6.85,3.92,'智能体搜索','查询改写、工具选择与停止\n何时搜索，何时已经足够？')]:
    s.card(x,y,5.75,1.85,h,b)
s.banner('共同目标：提供数量适当、来源可信、定位明确、足以回答的证据。')

s = Slide('CFVBench：找到视频，为什么还答不对？', '03 · 论文案例',
    'CFVBench 是一套视频问答基准，也就是考试题、参考事实和评分方法，而不是新的聊天模型。它关注的是细粒度视频 RAG。在检索到相关视频以后，系统还必须捕捉很短暂的画面，读清数字或按钮，并把语音与操作关联起来。作者同时评测检索和生成，再提出 AVR 作为改进方法，因此这篇工作包含基准、实验分析和方法三个部分。', CFV)
s.text(.7,1.8,11.8,.8,'把它理解成一场“允许查视频资料的开卷考试”。',25,INK,True)
for i,(h,b) in enumerate([('找得到','相关视频能否进入检索结果？'),('看得清','按钮、数字、短暂画面有没有被捕捉？'),('答得对','是否整合证据，而不是漏答或猜测？')]):
    s.card(.65+i*4.15,3.0,3.65,2.4,h,b,TEAL if i==1 else BLUE)
s.banner('CFVBench 是考卷；AVR 是作者提出的改进流程。')

s = Slide('数据设计：专门考“细节”，而不只考主题', '03 · 数据集与任务',
    '数据来自公开视频，覆盖三类高信息密度内容。图表报告要读清数值和关系；教程要把语音、界面动作与结果连起来；新闻需要结合画面、字幕和人物。作者抽取文本与视觉关键点，据此生成开放式问题，再通过人工修改和抽查控制质量。这里的开放式问题意味着模型需要自己组织答案，而不是从几个选项里猜一个。', CFV)
for x,n,l in [(.75,'599','公开视频'),(4.8,'约 5,360','开放式问答'),(8.85,'3 类','高密度视频内容')]:
    s.text(x,1.95,3.7,.75,n,36,TEAL,True)
    s.text(x,2.83,3.7,.4,l,17,MUTED)
for i,(h,b) in enumerate([('图表报告','读清数值、表格与关系'),('软件教程','对齐语音、操作与结果'),('新闻视频','整合字幕、画面与事件')]):
    s.card(.65+i*4.15,3.7,3.65,1.78,h,b,BLUE)
s.text(.75,5.73,11.9,.38,'构建流程：选择视频 → 抽取关键点 → 生成问答 → 人工校验',18,INK,True)
s.text(.75,6.28,11.8,.4,'统计注：论文总数为 5,360，分组计数与仓库为 5,363；需区分统计口径。',12,MUTED)

s = Slide('直观例子：关键选项只出现了一秒', '03 · 教学示例（非论文原题）',
    '用一个自编例子说明任务。用户问怎样导出透明背景图片。教程先说导出，再打开菜单，选择 PNG，随后勾选透明背景，最后保存。只听语音可能不知道格式和选项；只看少量截图，又可能漏掉只出现一秒的复选框。完整回答需要串起这些得分点。注意，这个例子是为讲解构造的，不是 CFVBench 中的原始样本。')
s.text(.75,1.8,11.8,.65,'问题：怎样导出透明背景的图片？',24,INK,True)
events=[('00:40','语音','“导出图片”'),('00:43','画面','文件 → 导出'),('00:46','画面','选择 PNG'),('00:48','画面 · 仅 1 秒','勾选透明背景'),('00:51','语音','“点击保存”')]
for i,(t,m,v) in enumerate(events):
    x=.65+i*2.48
    s.text(x,2.85,2.15,.4,t,20,TEAL,True)
    s.rect(x,3.48,2.15,1.58,'FFF0D9' if i==3 else 'FFFFFF','E3E8EE',True)
    s.text(x+.12,3.68,1.91,.4,m,13,AMBER if i==3 else MUTED,True)
    s.text(x+.12,4.25,1.91,.65,v,17,INK,True)
s.text(.75,5.43,11.8,.46,'完整答案：文件 → 导出 → PNG → 勾选透明背景 → 保存',20,INK,True)
s.banner('只看“视频大概讲什么”，不足以回答“具体应该怎样做”。')

s = Slide('评价：把“没找到”与“没用好”分开看', '03 · 评价框架',
    '评价分为两层。检索层的 Recall@10 询问前十个结果是否包含相关视频，但不说明关键画面是否被找到了。生成层则按参考答案中的得分点计算覆盖程度，同时考察答案里的事实是否正确。只说 PNG 可能是正确但不完整；补出视频没有讲的操作则可能无依据。论文还使用文本相似度和模型裁判等指标，因此需要留意自动评分可能有偏差。', CFV)
s.card(.65,2.0,5.75,3.05,'检索：找到相关资料了吗？','Recall@10：前 10 个结果\n是否包含相关视频？\n\n不等于：已定位所有关键画面。',BLUE)
s.card(6.85,2.0,5.75,3.05,'生成：得分点覆盖了吗？','召回率：应答的事实答全了吗？\n精确率：说出的事实正确吗？\nF1：综合覆盖与准确程度。')
s.text(.75,5.45,11.8,.4,'单跳：需要一个关键点；多跳：结合多个位置或模态的关键点。',18,INK)
s.banner('语言流畅不是证据充分；相关视频命中也不是答案正确。')

s = Slide('AVR：先粗看，不够再细看', '03 · 方法：ADAPTIVE VISUAL REFINEMENT',
    '视频不能总是逐帧输入模型，成本太高。AVR 先用语音转写和少量画面做初步理解，再由当前模型判断信息是否足够。如果证据不足，就在相关片段增加采样，并过滤重复画面。问题依赖文字和数字时调用 OCR；依赖物体时调用目标检测。最后仍由原模型回答。它不要求重新训练一个模型，主要改变的是推理时获取证据的流程。', CFV)
s.card(.65,1.94,3.05,2.15,'① 少量画面 + 语音','先理解片段\n初始均匀采样 5 帧',BLUE)
s.arrow(3.81,2.72)
s.card(4.25,1.94,3.4,2.15,'② 判断信息充分性','证据充分：保留\n证据不足：增加采样')
s.arrow(7.8,2.72)
s.card(8.3,1.94,4.3,2.15,'③ 按需补充证据','增加至 20–40 帧并去重\n按需调用文字识别 / 目标检测')
s.card(.65,4.53,5.75,1.22,'文字识别（OCR）','帮助读清按钮文字、字幕和图表数字',BLUE)
s.card(6.85,4.53,5.75,1.22,'最后仍由原模型回答','将画面、转写与工具结果一起作为证据')
s.banner('不是凭空“变聪明”，而是给模型更完整、更清楚的回答依据。')

s = Slide('检索结果：文本与画面有互补作用', '03 · 实验结果（一）',
    '这里展示论文的总体 Recall@10。纯文本检索为 76.11%，LanguageBind 为 76.17%，组合达到 81.37%。这说明文字与视觉信息存在互补性，但不是所有组合或所有任务都一定受益。尤其多点问题仍然难，因为一个问题可能需要多个位置的证据。这张图只衡量相关视频是否出现在前十项中，不能把它理解成最终回答的正确率。',CFV)
for i,(label,val,c) in enumerate([('纯文本检索',76.11,BLUE),('LanguageBind',76.17,BLUE),('二者组合',81.37,TEAL)]):
    y=2.15+i*1.12
    s.text(.75,y+.1,2.85,.5,label,19,INK,True)
    s.rect(3.75,y,7.5,.52,'E7ECF2',radius=True)
    s.rect(3.75,y,7.5*val/100,.52,c,radius=True)
    s.text(11.55,y+.02,1.1,.5,f'{val:.2f}%',19,c,True)
s.text(3.75,5.45,7.5,.3,'条形长度从 0% 开始，满幅为 100%；指标为总体 Recall@10。',12,MUTED)
s.banner('提高相关视频命中率是第一步；是否看清视频细节，还要单独检查。')

s = Slide('生成结果：补充视觉证据能改善表现', '03 · 实验结果（二）',
    '这张图比较四个代表模型使用 AVR 前后的视觉关键点召回率。绿色条都更长，说明补充画面与工具帮助模型覆盖了更多视觉事实。比如 GPT-5-chat 从 0.1552 到 0.2727。注意这不是最终答案正确率，也不是所有模型的同一提升幅度。论文中的 F1 也有改善，但仍不高，因此结论应是改善了证据利用，而不是已经解决视频理解。',CFV)
s.rect(.8,1.83,.2,.18,BLUE)
s.text(1.12,1.77,2.1,.4,'原模型',14,MUTED)
s.rect(3.0,1.83,.2,.18,TEAL)
s.text(3.32,1.77,3.2,.4,'使用 AVR',14,MUTED)
data=[('GPT-5-chat',.1552,.2727),('Gemini-2.5-Flash',.3051,.4625),('MiniCPM-V-2.6',.3793,.4561),('Intern-S1-mini',.2353,.3667)]
for i,(label,a,b) in enumerate(data):
    y=2.45+i*.78
    s.text(.75,y+.08,3.05,.5,label,17,INK,True)
    for off,v,c in [(0,a,BLUE),(.29,b,TEAL)]:
        s.rect(4.0,y+off,7.0,.22,'E7ECF2')
        s.rect(4.0,y+off,7*v,.22,c)
        s.text(4.15+7*v,y+off-.065,1.3,.35,f'{v:.4f}',12,c,True)
s.text(4.0,5.85,8.3,.3,'同一横轴：0–1；视觉关键点召回率 ≠ 最终答案正确率。',12,MUTED)
s.banner('论文同时报告 F1 改善；补充证据有效，但不意味着消除幻觉与遗漏。')

s = Slide('如何评价这篇工作：有价值，也有边界', '03 · 论文评价',
    '我认为它的重要价值是把模糊的视频理解问题拆成可以观察的证据使用问题，并提供开放式、细粒度任务。AVR 的模块化设计也便于附加到已有模型上。不过规划器本身仍会误判，如果第一次完全没看到关键线索，也未必知道应该再看；更多采样和工具调用会增加成本；自动评分也可能有偏差。此外数据统计口径存在差异。公平的评价应同时讨论收益和这些限制。',
    '依据：CFVBench 原文；局限分析为本汇报的阅读评价')
s.card(.65,2.0,5.75,3.45,'贡献','把检索与证据利用分开评价\n覆盖图表、界面、字幕等真实内容\n开放式问题更考验完整回答\nAVR 可附加到不同模型的推理流程')
s.card(6.85,2.0,5.75,3.45,'局限','模型可能误判“证据已经足够”\n补帧与工具调用增加计算成本\n自动关键点评分仍可能有偏差\n样本统计与复现口径需要澄清',AMBER)
s.banner('需要同时衡量：回答质量、证据定位、延迟与计算成本。')

s = Slide('总结：检索的终点，不应该只是“找到”', '04 · 总结与讨论',
    '总结起来，Web 搜索从关键词匹配发展到语义检索，再发展到为生成模型组织证据。WWW 2026 的相关研究更加关注可靠性、效率、多模态和多步搜索。CFVBench 用视频场景说明，找到相关内容并不等于回答正确，还要看清短暂细节并整合证据。AVR 给出的思路是按问题需要补充信息，而不是对所有视频无差别地增加计算。我的汇报到这里，谢谢大家。')
for y,n,h,b in [(1.95,'01','检索基础仍然重要','索引、召回、排序决定可获得什么证据。'),(3.13,'02','关键挑战是证据利用','视频中的短暂细节，会让“相关”与“可回答”分离。'),(4.31,'03','改进方向是按需获取证据','联合优化采样、工具、推理与成本，而不只增加上下文。')]:
    s.text(.75,y,.8,.65,n,31,TEAL,True)
    s.text(1.85,y,10.4,.45,h,22,INK,True)
    s.text(1.85,y+.57,10.4,.5,b,18,MUTED)
s.banner('讨论：如果 AI 没看到关键画面，它怎样知道自己还需要“再看一次”？')

s = Slide('主要资料与 AI 使用说明', '附录 · 不计入主要汇报时间',
    '这页用于提供主要资料与使用说明。详细参考文献见配套论文。汇报中的软件导出示例是教学构造，不是数据集样本；数据图依据 CFVBench 原文重绘，没有重新运行实验。AI 参与了资料整理、结构、文字、图示和文件生成；汇报者应继续核对引用与数据，并对最终表达负责。')
refs=[('研究方向与会议论文','www2026.thewebconf.org/calls/research-tracks.html\ndl.acm.org/doi/proceedings/10.1145/3774904'),('检索基础与语义检索','Manning et al. (2008), Introduction to Information Retrieval\nKarpukhin et al. (2020), Dense Passage Retrieval'),('RAG 与案例论文','Lewis et al. (2020), Retrieval-Augmented Generation\nWei et al. (2026), CFVBench · doi:10.1145/3774904.3792726\n预印本：arxiv.org/abs/2510.09266')]
for y,(h,b) in zip([1.85,3.1,4.35],refs):
    s.text(.75,y,3.1,.5,h,18,TEAL,True)
    s.text(4.05,y,8.45,1.15,b,15,INK)
s.text(.75,6.22,11.8,.55,'AI 参与：资料整理、结构设计、文字初稿、图示及 PPT 生成。教学例子为自编；实验图依原文重绘，未重新运行实验。',12,MUTED)

NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
GROUP = '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
def rels(items):
    return '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{rid}" Type="{REL}{typ}" Target="{target}"/>' for rid,typ,target in items)+'</Relationships>'

theme=f'''<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Chinese Research"><a:themeElements><a:clrScheme name="Research"><a:dk1><a:srgbClr val="{INK}"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="{MUTED}"/></a:dk2><a:lt2><a:srgbClr val="{BG}"/></a:lt2>{''.join(f'<a:accent{i}><a:srgbClr val="{c}"/></a:accent{i}>' for i,c in enumerate([TEAL,BLUE,AMBER,'B45D62','6B66A6','7E9361'],1))}<a:hlink><a:srgbClr val="{BLUE}"/></a:hlink><a:folHlink><a:srgbClr val="6B66A6"/></a:folHlink></a:clrScheme><a:fontScheme name="Chinese"><a:majorFont><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:majorFont><a:minorFont><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:minorFont></a:fontScheme><a:fmtScheme name="Simple"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst>{'<a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>'*3}</a:lnStyleLst><a:effectStyleLst>{'<a:effectStyle><a:effectLst/></a:effectStyle>'*3}</a:effectStyleLst><a:bgFillStyleLst>{'<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'*3}</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>'''
parts={
    '_rels/.rels':rels([('rId1','officeDocument','ppt/presentation.xml')]),
    'ppt/theme/theme1.xml':theme,
    'ppt/presentation.xml':f'<p:presentation {NS}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:notesMasterIdLst><p:notesMasterId r:id="rIdNotes"/></p:notesMasterIdLst><p:sldIdLst>'+''.join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(len(slides)))+f'</p:sldIdLst><p:sldSz cx="{int(13.333*EMU)}" cy="{int(7.5*EMU)}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>',
    'ppt/_rels/presentation.xml.rels':rels([('rId1','slideMaster','slideMasters/slideMaster1.xml'),('rIdNotes','notesMaster','notesMasters/notesMaster1.xml')]+[(f'rId{i+1}','slide',f'slides/slide{i}.xml') for i in range(1,len(slides)+1)]),
    'ppt/slideMasters/slideMaster1.xml':f'<p:sldMaster {NS}><p:cSld><p:spTree>{GROUP}</p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>',
    'ppt/slideMasters/_rels/slideMaster1.xml.rels':rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml'),('rId2','theme','../theme/theme1.xml')]),
    'ppt/slideLayouts/slideLayout1.xml':f'<p:sldLayout {NS} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>{GROUP}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>',
    'ppt/slideLayouts/_rels/slideLayout1.xml.rels':rels([('rId1','slideMaster','../slideMasters/slideMaster1.xml')]),
    'ppt/notesMasters/notesMaster1.xml':f'<p:notesMaster {NS}><p:cSld><p:spTree>{GROUP}</p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:notesStyle/></p:notesMaster>',
    'ppt/notesMasters/_rels/notesMaster1.xml.rels':rels([('rId1','theme','../theme/theme1.xml')]),
}
for i,s in enumerate(slides,1):
    parts[f'ppt/slides/slide{i}.xml']=f'<p:sld {NS}><p:cSld><p:spTree>{GROUP}{"".join(s.shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    parts[f'ppt/slides/_rels/slide{i}.xml.rels']=rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml'),('rId2','notesSlide',f'../notesSlides/notesSlide{i}.xml')])
    parts[f'ppt/notesSlides/notesSlide{i}.xml']=f'''<p:notes {NS}><p:cSld><p:spTree>{GROUP}<p:sp><p:nvSpPr><p:cNvPr id="2" name="Speaker Notes"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:r><a:rPr lang="zh-CN"/><a:t>{xmltext(s.notes)}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>'''
    parts[f'ppt/notesSlides/_rels/notesSlide{i}.xml.rels']=rels([('rId1','slide',f'../slides/slide{i}.xml'),('rId2','notesMaster','../notesMasters/notesMaster1.xml')])
overrides=[('ppt/presentation.xml','presentation'),('ppt/slideMasters/slideMaster1.xml','slideMaster'),('ppt/slideLayouts/slideLayout1.xml','slideLayout')]
overrides += [('ppt/notesMasters/notesMaster1.xml','notesMaster')]
overrides += [(f'ppt/slides/slide{i}.xml','slide') for i in range(1,len(slides)+1)]
overrides += [(f'ppt/notesSlides/notesSlide{i}.xml','notesSlide') for i in range(1,len(slides)+1)]
parts['[Content_Types].xml']='<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'+''.join(f'<Override PartName="/{p}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.{t}{".main" if t=="presentation" else ""}+xml"/>' for p,t in overrides)+'</Types>'
for name,content in parts.items():
    ET.fromstring(content)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    for name,content in parts.items():
        z.writestr(name,'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+content)

# Generated companion notes are deliberately kept as editable Markdown.
notes=['# 搜索与检索增强人工智能：逐页讲稿','',
       '建议时长：10–12 分钟。第 1–15 页为正文，第 16 页为资料附录。', '',
       '所有实验数值来自原论文；本汇报没有重新运行实验。教学案例明确标注为自编。', '']
times=[20,40,40,40,45,50,40,45,60,50,65,40,45,45,35,0]
for i,(s,t) in enumerate(zip(slides,times),1):
    notes += [f'## {i:02} {s.title}', '', f'建议时间：约 {t} 秒。' if t else '附录：按需展示。', '', s.notes, '']
notes += ['## 常见问题与简短回答','',
    '**CFVBench 是模型吗？** 不是，主要是数据集、任务与评价基准。AVR 才是论文提出的改进流程。','',
    '**AVR 要重新训练吗？** 主要改变推理流程，动态增加采样并按需调用工具，而不是训练新的回答模型。','',
    '**81.37% 是回答正确率吗？** 不是，是总体 Recall@10，即相关视频是否进入前 10 个检索结果。','',
    '**多跳一定意味着多个视频吗？** 不一定。这里主要指整合多个关键点，可来自不同时间位置或模态。','',
    '**为什么只选择四个模型画图？** 为便于汇报，选取四个代表模型；不是完整排行榜，也不是本次重跑的结果。','',
    '**为什么问答数不一致？** 论文总数为 5,360，分组与仓库记录为 5,363。这里保留差异，不强行统一。','',
    '**能否保证补帧就答对？** 不能。规划器也可能误判，补充证据不能彻底消除整合错误与幻觉。','']
(ROOT/'逐页讲稿.md').write_text('\n'.join(notes),encoding='utf-8')
print(f'Created {OUT}: {len(slides)} editable slides; {sum(times)} seconds suggested speaking time.')
