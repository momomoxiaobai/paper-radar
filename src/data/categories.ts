export const CATEGORY_GROUPS = [
  {
    id: "frontier",
    number: "01",
    label: "前沿雷达",
    cadence: "周一至周五",
    description: "捕捉训练、推理、智能体与系统工程里值得继续跟进的新信号。",
    categories: ["rl", "agent", "llm", "infra"],
  },
  {
    id: "harness",
    number: "02",
    label: "Agent 工程",
    cadence: "周一至周五",
    description:
      "拆解上下文、工具、运行时和技能复用如何把 Agent 变成可靠系统。",
    categories: ["harness", "skill"],
  },
  {
    id: "classic-algorithms",
    number: "03",
    label: "算法重访",
    cadence: "周一至周五",
    description: "借新研究与工程实践，重新理解那些经得起时间的基础方法。",
    categories: ["classic-algorithms"],
  },
  {
    id: "foundation-models",
    number: "04",
    label: "模型档案",
    cadence: "按价值收录",
    description:
      "为具有长期参考价值的基础模型保留完整技术档案，不参与固定更新配额。",
    categories: ["foundation-models"],
  },
  {
    id: "ml-classics",
    number: "05",
    label: "机器学习经典",
    cadence: "专题连载",
    description:
      "从概率建模、树模型、核方法到聚类与降维，重新推导经典机器学习方法，并解释它们今天为什么仍然有用。",
    categories: ["ml-classics"],
  },
  {
    id: "training-methods",
    number: "06",
    label: "训练方法",
    cadence: "专题连载",
    description:
      "沿策略优化、偏好对齐、蒸馏与训练稳定性四条线，拆解 PPO、DPO、GRPO 等方法的目标、实现和失效模式。",
    categories: ["training-methods"],
  },
] as const;

export const SERIES_ROADMAPS = [
  {
    id: "ml-classics",
    number: "05",
    label: "机器学习经典",
    description: "先建立统计学习的共同语言，再进入树、核、集成与序列模型。",
    items: [
      "贝叶斯决策论：先验、似然、后验与 Bayes risk",
      "Naive Bayes：条件独立为何简单但有效",
      "线性回归：最小二乘、MLE 与正则化",
      "Logistic Regression：概率分类与交叉熵",
      "决策树：ID3、C4.5 与 CART",
      "Random Forest：Bagging、特征采样与 OOB",
      "GBDT：函数空间中的梯度下降",
      "XGBoost：二阶近似、正则化与分裂增益",
      "LightGBM / CatBoost：直方图、leaf-wise 与类别特征",
      "SVM：最大间隔、对偶与核技巧",
      "KNN：局部假设、距离度量与维数灾难",
      "K-Means / GMM / EM：硬聚类与软聚类",
      "PCA：最大方差与最小重构误差",
      "LDA / QDA：生成式分类与协方差假设",
      "HMM：Forward-Backward、Viterbi 与 Baum-Welch",
      "CRF：条件图模型与结构化预测",
      "AdaBoost：指数损失与样本重加权",
      "Bagging vs Boosting：方差与偏差的两条路径",
      "MLE / MAP / EM：三种参数估计视角",
      "概率校准：Platt Scaling、Isotonic Regression 与 ECE",
    ],
  },
  {
    id: "training-methods",
    number: "06",
    label: "训练方法",
    description: "从 PPO 起步，贯通强化学习、偏好优化、蒸馏与大模型训练工程。",
    items: [
      "PPO：clip、GAE、actor-critic 与 RLHF",
      "TRPO：信赖域、KL 约束与二阶优化",
      "GAE：优势估计的偏差—方差折中",
      "REINFORCE 与 Actor-Critic",
      "A2C / A3C：同步与异步采样",
      "DQN：Replay Buffer、Target Network 与 Double DQN",
      "SAC：最大熵强化学习",
      "DDPG / TD3：连续控制与双重 critic",
      "RLHF 完整管线：SFT、RM、PPO 与 KL",
      "Reward Model：偏好数据、Bradley–Terry 与过优化",
      "DPO：从 KL 约束 RL 到分类损失",
      "IPO、KTO、ORPO 与 SimPO",
      "GRPO：组内相对优势与无 critic 训练",
      "RLOO、ReMax 与方差缩减",
      "RLVR：可验证奖励与推理训练",
      "Process Reward 与 Outcome Reward",
      "Knowledge Distillation 与 Sequence-level Distillation",
      "Curriculum Learning 与 Self-training",
      "Contrastive Learning 与 Hard-negative Mining",
      "LoRA / QLoRA：低秩适配与量化微调",
      "梯度累积、混合精度与梯度裁剪",
      "SGD、Momentum、Adam、AdamW 与 Adafactor",
      "Warmup、Cosine 与 inverse-square-root 调度",
      "数据配比、采样温度与去重",
      "Continued Pretraining、SFT 与灾难性遗忘",
      "Test-time Training 与 Test-time Adaptation",
    ],
  },
] as const;

export const CATEGORIES = [
  {
    slug: "rl",
    label: "RL",
    description: "强化学习、奖励建模、策略优化与推理时计算。",
  },
  {
    slug: "agent",
    label: "Agent",
    description: "智能体规划、协作、记忆、工具使用与多模态 Agent。",
  },
  {
    slug: "llm",
    label: "LLM",
    description: "大语言模型训练、对齐、评测与能力研究。",
  },
  {
    slug: "infra",
    label: "Infra",
    description: "训练和推理基础设施、并行、服务、编译与硬件。",
  },
  {
    slug: "harness",
    label: "Harness",
    description: "Agent 脚手架、上下文工程、编排、观测与可靠运行。",
  },
  {
    slug: "skill",
    label: "Skill",
    description: "可复用技能、工具学习、程序性记忆与工作流沉淀。",
  },
  {
    slug: "classic-algorithms",
    label: "经典算法",
    description: "搜索、动态规划、优化、采样与基础机器学习算法。",
  },
  {
    slug: "foundation-models",
    label: "基座模型",
    description: "重要基础模型的架构、训练数据、能力边界与技术报告。",
  },
  {
    slug: "ml-classics",
    label: "机器学习经典",
    description:
      "概率模型、线性模型、树模型、核方法、集成学习与经典无监督学习。",
  },
  {
    slug: "training-methods",
    label: "训练方法",
    description: "策略优化、偏好对齐、蒸馏、优化器与大模型训练稳定性。",
  },
] as const;

export type CategorySlug = (typeof CATEGORIES)[number]["slug"];

export function getCategory(slug: CategorySlug | string) {
  return CATEGORIES.find(category => category.slug === slug);
}
