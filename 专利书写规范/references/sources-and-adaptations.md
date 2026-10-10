# 来源与融合说明

本文件记录“专利书写规范”skill 的主要来源、抽象规则和许可边界。使用时应优先核对当前国家知识产权局官方原文。

## 一、国家知识产权局官方来源

### 1. 《中华人民共和国专利法》（2020年修正）
https://www.cnipa.gov.cn/art/2020/11/23/art_524_171347.html

用于：
- 新颖性、创造性、实用性基本门槛；
- 疾病诊断和治疗方法的专利客体限制；
- 说明书充分公开和权利要求支持的法律基础。

### 2. 《中华人民共和国专利法实施细则》（2023年修订）
https://www.cnipa.gov.cn/art/2023/12/21/art_98_189197.html

用于：
- 说明书章节结构；
- 权利要求书基本形式；
- 摘要；
- 附图；
- 序列表；
- 生物材料保藏；
- 遗传资源披露；
- 诚实信用和真实发明创造要求。

### 3. 《专利审查指南》（2023）及修改解读
总入口：
https://www.cnipa.gov.cn/art/2024/1/18/art_66_189848.html

智能医疗/创造性相关：
https://www.cnipa.gov.cn/art/2024/1/18/art_2199_189878.html

计算机程序/AI相关：
https://www.cnipa.gov.cn/art/2024/1/18/art_2199_189865.html
https://www.cnipa.gov.cn/art/2024/1/18/art_2199_189877.html

用于：
- 智能医疗诊断方法判断；
- 全部步骤由计算机实施的信息处理方法的审查口径；
- 创造性三步法；
- 算法与技术特征整体考虑；
- 方法、装置、存储介质、程序产品等保护主题。

### 4. 国家知识产权局第84号令
https://www.cnipa.gov.cn/art/2025/11/14/art_99_202568.html

2026-01-01 起施行。用于：
- AI、大数据算法案件；
- 技术贡献特征进入权利要求；
- AI 模型结构/训练/输入输出的说明书公开要求；
- 创造性示例；
- 生物信息预测癌症的充分公开反例。

政策解读：
https://www.cnipa.gov.cn/art/2025/12/4/art_66_202935.html

### 5. 《人工智能相关发明专利申请指引（试行）》
https://www.cnipa.gov.cn/art/2024/12/31/art_66_196988.html

用于 AI 发明专利申请中的客体、撰写和审查政策理解。

### 6. CNIPA 摘要字数官方咨询
https://www.cnipa.gov.cn/jact/front/mailpubdetail.do?transactId=472691

用于确认摘要文字部分（含标点）不超过 300 字的现行审查要求。

## 二、公开中国专利样本

这些专利仅用于观察公开申请文件的组织方式、保护主题和技术链表达。第三方页面显示的法律状态不作为本 skill 的最终法律结论。

### 生物信息学/多组学

- CN116741397B：基于多组学数据融合的癌症分型方法、系统及存储介质  
  https://patents.google.com/patent/CN116741397B/zh
- CN111291777B：一种基于多组学集成的癌症亚型分类方法  
  https://patents.google.com/patent/CN111291777B/zh
- CN118296442B：多组学癌症亚型分类方法、系统、设备、介质及程序产品  
  https://patents.google.com/patent/CN118296442B/zh
- CN119581048B：一种基于图表征的多组学癌症样本表示方法及相关装置  
  https://patents.google.com/patent/CN119581048B/zh
- CN116825188B：基于高通量测序技术在多组学层面识别肿瘤新抗原的方法、装置及计算机可读存储介质  
  https://patents.google.com/patent/CN116825188B/zh
- CN114596918B：一种检测突变的方法及装置  
  https://patents.google.com/patent/CN114596918B/zh
- CN120015323B：一种基于多组学数据融合的肺癌预后预测方法  
  https://patents.google.com/patent/CN120015323B/zh

### 医学影像

- CN107016665B：一种基于深度卷积神经网络的 CT 肺结节检测方法  
  https://patents.google.com/patent/CN107016665B/zh

吸收的仅是高层模式：
- 技术链应具体到数据、处理、中间产物和输出；
- 从属权利要求形成层级；
- 软件发明可形成方法/系统/设备/介质/程序产品等主题；
- 实施例应支撑核心特征。

不复制专利文本、公式或具体权利要求。

## 三、本轮提供的真实医学 AI 专利样本

开发本 skill 时分析了一份由用户提供的完整医学 AI 发明专利申请样本。该材料未复制或上传到公开仓库。

仅抽象吸收：

- 摘要—权利要求—发明内容—实施例—附图围绕同一核心流程镜像；
- 独立方法权利要求建立完整步骤链；
- 从属权利要求按数据、特征、模型、阈值、输出等逐层下钻；
- 系统权利要求映射方法模块；
- 多实施例扩展不同部署/使用场景。

同时建立反模式：

- 不凭空写病例数、性能、阈值和硬件；
- 不将临床治疗/活检/随访路径无必要塞入核心算法权利要求；
- 不靠模型名堆叠扩展保护范围；
- 不加入与核心技术问题无关的“高级技术”装饰模块。

## 四、开源项目

### Zaoqu-Liu/cn-patent
https://github.com/Zaoqu-Liu/cn-patent  
License：MIT（以其仓库当前 LICENSE 为准）

吸收的高层工作流：
- CNIPA-first 查新；
- 项目材料 → 专利点 → 现有技术 → 交底；
- 技术问题—技术方案—技术效果；
- 充分公开、支持性和质量门禁；
- 版本化迭代。

本 skill 没有复制其具体代码、提示词、模板文本或脚本，独立重写并扩展到完整申请文件、医疗客体、生物信息学和 2026 AI 规则。

### patsnap/mcp
https://github.com/patsnap/mcp  
License：Apache-2.0（以仓库当前 LICENSE 为准）

吸收的高层思路：
- 关键词、语义、相似度的多通道专利检索；
- patent family、legal status、novelty/FTO、技术问题—方案—效果等结构化检索维度；
- life sciences 与 IP 数据协同。

本 skill 不依赖 Patsnap 服务，也不复制其实现。

### rbouadjenek/patent-search
https://github.com/rbouadjenek/patent-search

用于认识 prior-art IR 中的术语选择和 query reformulation 思路。未复制代码。正式使用时应自行核查其许可。

### VolodymyrLinuxovich/claimchecker
https://github.com/VolodymyrLinuxovich/claimchecker

用于抽象“申请草稿 ↔ invention disclosure/supporting context”核对思路，形成 claim-support matrix。未复制代码或界面文本。

## 五、来源优先级

出现冲突时：

1. 现行法律；
2. 现行实施细则；
3. 当前有效《专利审查指南》及修改决定；
4. CNIPA 官方解读/办事答复；
5. 已公开专利和审查实践；
6. WIPO/EPO 等国外规范（仅作比较）；
7. 学术论文；
8. GitHub/第三方工作流。

GitHub 不能覆盖法律规则；公开专利也不能证明某种写法对新案件一定可授权。

## 六、版权与保密

- 不把用户未公开的专利草稿、论文、实验数据、患者资料放入公开仓库；
- 不大段复制公开专利文本；
- 不复制第三方 skill 或代码后声称为原创；
- 引入外部代码前单独核查许可证；
- 本 skill 以独立总结、结构化流程和原创模板为主。