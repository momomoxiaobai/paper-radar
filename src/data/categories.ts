export const CATEGORY_GROUPS = [
  {
    id: "frontier",
    label: "一线资讯",
    cadence: "工作日日更",
    description: "追踪训练、推理与应用一线进展。",
    categories: ["rl", "agent", "llm", "infra"],
  },
  {
    id: "harness",
    label: "Harness",
    cadence: "工作日日更",
    description: "关注 Agent 工程骨架、工具调用、Skill 与运行时。",
    categories: ["harness", "skill"],
  },
  {
    id: "classic-algorithms",
    label: "经典算法",
    cadence: "工作日日更",
    description: "重读长期有效的搜索、优化、采样与学习算法。",
    categories: ["classic-algorithms"],
  },
  {
    id: "foundation-models",
    label: "基座收藏夹",
    cadence: "持续收录 · 非日更第四路",
    description: "收录混元 HY、Qwen、DeepSeek、Llama 等基座模型专文。",
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
    description: "混元 HY 等重要基座模型的架构、训练和技术报告。",
  },
] as const;

export type CategorySlug = (typeof CATEGORIES)[number]["slug"];

export function getCategory(slug: CategorySlug | string) {
  return CATEGORIES.find(category => category.slug === slug);
}
