# TODO List

## 1. 核心挑战解析
- **上下文窗口限制**  
  - 分析大模型（如 GPT-4）上下文窗口的限制（目前最大 128k tokens），及如何规避或缓解这一限制。
- **线性存储效率低下**  
  - 目前对话记录采用线性存储方式，存在效率问题，需探索更高效的存储和检索策略。
- **信息稀释问题**  
  - 混杂重要事件与日常对话导致关键信息被淹没。需要将关键信息与普通对话分离管理。

## 2. 分层记忆架构方案
- **设计并实现以下层次**：
  - **实时交互层**：用于即时处理用户输入和模型响应。
  - **工作记忆区**：缓存最近对话记录，作为短期记忆。
  - **长期记忆库**：存储经过摘要提取后的关键信息、事件和情绪数据。
  - **记忆强化模块**：通过向量检索和事件图谱进行关键记忆召回，并动态注入到实时上下文中。

- **可视化流程图**（Mermaid）：
  ```mermaid
  graph TD
      A[实时交互层] -->|即时处理| B[工作记忆区]
      B -->|摘要提取| C[长期记忆库]
      C -->|向量检索| D[记忆强化模块]
      D -->|动态注入| A
  ```

## 3. 关键技术实现

### 3.1 记忆压缩技术
- **即时摘要**：
  - 每 5 轮对话生成一次结构化摘要（包括人物、事件、情感）。
- **周期摘要**：
  - 每日汇总生成里程碑记录，标记当日关键进展。

### 3.2 智能检索系统
- **构建混合索引体系**：
  - 使用 FAISS 构建语义相似度向量检索库。
  - 使用 TimeTree 建立时间线索引。
  - 使用 Neo4j 构建事件关系图谱。

- **实现 MemoryIndex 类**：
  ```python
  class MemoryIndex:
      def __init__(self):
          self.vector_db = FAISS()  # 语义相似度检索
          self.time_index = TimeTree()  # 时间线索引
          self.event_graph = Neo4j()  # 事件关系图谱

      def recall_memory(self, query, n=3):
          # 实现多维度记忆召回策略
          return hybrid_search(query, n)
  ```

### 3.3 动态上下文管理
- **自适应上下文窗口**：
  - 保留当前对话的最新部分（例如最近 10 轮）。
  - 结合从长期记忆库中召回的战略记忆，动态构建上下文。

- **示例方法实现**：
  ```python
  def dynamic_context_window(current_dialog, memory_recalls):
      base_context = current_dialog[-10:]  # 保留最近 10 轮对话
      strategic_memories = select_strategic_points(memory_recalls)
      return strategic_memories + base_context
  ```

## 4. 记忆强化策略

### 4.1 进度锚点机制
- **创建记忆锚点**：
  - 在关键攻略节点（如首次获得道具、BOSS 战败）创建记忆锚点，便于后续查询和增强响应。

- **锚点示例结构**：
  ```json
  {
      "anchor_id": "BOSS_023",
      "type": "combat",
      "timestamp": "2023-08-20T14:30:00",
      "related_events": ["quest_045", "npc_12"],
      "emotional_weight": 0.87
  }
  ```

### 4.2 遗忘补偿算法
- **记忆衰减模型**：
  - 设计记忆强度的衰减公式：  
    记忆强度 = 初始强度 × e^(-λ×Δt) × Σ(触发次数)
- **触发补偿**：
  - 当记忆强度低于某一阈值时，自动生成提示问题（如"还记得我们上次击败XX的情形吗？"），引导用户回忆并强化相关记忆。

## 5. 用户体验优化

### 5.1 渐进式记忆唤醒
- **三级唤醒策略**：
  - **Level 1**：模糊提及（"之前有个重要时刻..."）
  - **Level 2**：特征提示（"那个使用火焰剑的战斗..."）
  - **Level 3**：完整回忆（"2023年8月20日我们击败炎魔时..."）

### 5.2 情感连续性保持
- **人格一致性引擎**：
  - 实现一个 PersonaEngine 类，保证回复风格和情感连续性。
  ```python
  class PersonaEngine:
      def __init__(self):
          self.base_persona = "helpful_guide"
          self.relationship = RelationshipMatrix()
          
      def respond(self, query):
          response_style = self.relationship.get_style()
          memory_weight = calculate_memory_relevance()
          return generate_response(query, style=response_style, memory=memory_weight)
  ```

## 6. 实施建议
- **架构策略**：
  - 采用 RAG（检索增强生成）架构构建记忆系统，提高信息检索与生成的一体化效果。
  
- **流水线框架**：
  - 探索使用 LangChain 等现有框架统一管理记忆流水线。

- **记忆强化系数**：
  - 为关键节点设置 1.5-3 倍的强化系数，提升记忆的权重。

- **定期整理**：
  - 开发 MemGC（Memory Garbage Collection）模块，定期清理和整理记忆库，避免信息水污染。

## 附加任务
- 优化现有对话记录的存储机制，以减少冗余数据。
- 扩展命令功能，允许用户主动查询或唤醒长期记忆。