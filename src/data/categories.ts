export const CATEGORY_GROUPS = [
  {
    id: "frontier",
    label: "前沿雷达",
    cadence: "周一至周五",
    description: "捕捉训练、推理、智能体与系统工程里值得继续跟进的新信号。",
    categories: ["rl", "agent", "llm", "infra"],
  },
  {
    id: "harness",
    label: "Agent 工程",
    cadence: "周一至周五",
    description:
      "拆解上下文、工具、运行时和技能复用如何把 Agent 变成可靠系统。",
    categories: ["harness", "skill"],
  },
  {
    id: "classic-algorithms",
    label: "算法重访",
    cadence: "周一至周五",
    description: "借新研究与工程实践，重新理解那些经得起时间的基础方法。",
    categories: ["classic-algorithms"],
  },
  {
    id: "foundation-models",
    label: "模型档案",
    cadence: "按价值收录",
    description:
      "为具有长期参考价值的基础模型保留完整技术档案，不参与固定更新配额。",
    categories: ["foundation-models"],
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
] as const;

export type CategorySlug = (typeof CATEGORIES)[number]["slug"];

export function getCategory(slug: CategorySlug | string) {
  return CATEGORIES.find(category => category.slug === slug);
}
