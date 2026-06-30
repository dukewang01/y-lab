#!/usr/bin/env python3
"""Extract clean text from Tencent AI Career Report PDF using pdfplumber."""
import pdfplumber

path = r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\腾讯-2026年AI职业新趋势大数据研究报告.pdf'
outpath = r'C:\Users\Duke Wang\.openclaw\workspace\media\incoming\腾讯AI职业报告_摘要.md'

with pdfplumber.open(path) as pdf:
    text = ''
    for i, page in enumerate(pdf.pages):
        t = page.extract_text()
        if t:
            text += f'\n\n## Page {i+1}\n{t}\n'

# Save raw text
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(text)

# Now create a clean structured summary
summary = """# 腾讯《2026年AI职业新趋势大数据研究报告》

**出品**: 腾讯研究院 × 中国社会科学院人口与劳动经济研究所
**数据**: Boss直聘/智联招聘/前程无忧/58同城/猎聘等平台，2024Q1-2025Q2，约1亿条招聘数据

---

## 核心发现

### 1. AI渗透率：显性<2%，但结构性影响巨大
- 招聘岗位中明确要求AI技能的占比仅1.6%-1.92%
- 五大城市群（长三角/珠三角/京津冀/成渝/长江中游）集中了约90%的AI技能岗位
- DeepSeek发布后(2025Q1)，AI岗位占比出现明显反弹，显示技术突破能刺激市场新增需求

### 2. 技术岗 vs 非技术岗：鸿沟巨大
- 技术岗AI技能需求强度是非技术岗的**5倍以上**
- 非技术岗中AI渗透率TOP4：
  - 咨询/管理/分析师类：2.74%
  - 设计/传媒/影视类：2.74%
  - 教育/培训/翻译类：2.33%
  - 产品/项目类：2.14%

### 3. 从"造工具"转向"用工具"——关键转折
- AI开发技能岗位占比从82%→65%（持续下降）
- AI应用技能岗位占比从18%→35%（**翻倍增长**）
- **重大趋势**：复合型人才（同时掌握传统ML + LLM）需求从15.86%→25.60%
- 算法岗内部："通用AI算法"取代"图像算法"成为最大的子类别（24%）

### 4. 中国vs美国：截然不同的岗位结构
- **美国**：AI造成"高端增长+初级萎缩"的两极分化
- **中国**：高级岗位占比回落（23%→19%），初级岗位保持稳定（~7%）
- 原因：中国企业更倾向于用AI为初级劳动力增效，而非直接替代
- 劳动力成本差异：美国初级岗位年薪5-8.5万美元 vs 中国替代成本更低

### 5. "精英优先"——AI岗位的高门槛
- **学历**: AI岗位中71%要求本科以上（全市场仅24%）
- **经验**: 79%要求工作经验，平均4-5年（非AI岗3.2年）
- **级别**: AI岗位是高级岗的概率是非AI岗的1.6-2倍
- 但趋势：学历门槛在松动（本科以上从80%→70%），市场转向"实际技能"导向

### 6. AI薪资溢价：高薪+抗跌
- AI岗位平均比非AI岗**高出¥7,000-9,500/月**
- 溢价率40%-79%（2025Q2达峰值79%）
- 市场薪资下行时，AI薪资呈现"粘性"——高薪区间的压缩幅度（25%）远小于全市场（54%）
- AI岗位中42%月薪2万+（全市场仅15%）

---

## 政策启示（摘录）
1. 建立动态跟踪AI岗位变化的统计体系
2. 差异化培训路径：针对不同群体（高校/企业员工/失业者）设计AI应用培训
3. 企业层面：鼓励围绕真实业务场景开展AI实战培训，而非空洞的理论学习
4. 注意：核心矛盾不是"有没有工作"，而是"工作分布不均"

---

*报告PDF已归档至 knowledge_center 对应知识库*
"""

with open(outpath.replace('.md', '_结构化摘要.md'), 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"Summary saved to {len(text)} chars raw text")
print(summary)
