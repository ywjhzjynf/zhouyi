# 🏛️ OpenClaw 系统架构图

**绘制时间：** 2026-03-20  
**版本：** v1.0

---

## 整体架构

```mermaid
graph TB
    subgraph 飞书平台
        F1[🤖 内阁首辅机器人<br/>cli_a936b7...<br/>✅ 已连接]
        F2[🤖 监正御史机器人<br/>cli_a9311b...<br/>⚠️ 配置就绪]
    end

    subgraph 主 Agent 会话
        MAIN[🏛️ 内阁首辅 - 青词<br/>总揽全局 / 协调三省六部<br/>模型：qwen3.5-plus<br/>100 万上下文]
    end

    subgraph 三省
        ZS[📜 中书省<br/>zhongshu<br/>策略规划]
        MS[🔍 门下省<br/>menxia<br/>审核把关]
        SS[⚙️ 尚书省<br/>shangshu<br/>执行协调]
    end

    subgraph 六部
        GB[🔨 工部<br/>gongbu<br/>开发]
        BB[⚔️ 兵部<br/>bingbu<br/>算法]
        HB[📊 户部<br/>hubu<br/>数据]
        LB[🎋 礼部<br/>liwu<br/>日常事务]
    end

    subgraph 独立部门
        JZ[🛡️ 监正<br/>jianzheng<br/>系统运维]
    end

    subgraph 监控系统
        MON[📈 网关监控<br/>30 秒检测<br/>自动重启]
        LOG[📝 日志系统<br/>gateway-monitor.log]
        START[⚙️ 开机自启<br/>快捷方式]
    end

    F1 <--> MAIN
    F2 -.->|⚠️ 子 Agent 限制 | MAIN
    
    MAIN --> ZS
    MAIN --> MS
    MAIN --> SS
    
    SS --> GB
    SS --> BB
    SS --> HB
    SS --> LB
    
    MAIN --> JZ
    
    MAIN --> MON
    MON --> LOG
    MON --> START

    style MAIN fill:#1e88e5,stroke:#0d47a1,stroke-width:3px,color:#fff
    style F1 fill:#43a047,stroke:#1b5e20,stroke-width:2px,color:#fff
    style F2 fill:#ffb74d,stroke:#e65100,stroke-width:2px,color:#000
    style ZS fill:#8e24aa,stroke:#4a148c,stroke-width:2px,color:#fff
    style MS fill:#8e24aa,stroke:#4a148c,stroke-width:2px,color:#fff
    style SS fill:#8e24aa,stroke:#4a148c,stroke-width:2px,color:#fff
    style GB fill:#e53935,stroke:#b71c1c,stroke-width:2px,color:#fff
    style BB fill:#e53935,stroke:#b71c1c,stroke-width:2px,color:#fff
    style HB fill:#e53935,stroke:#b71c1c,stroke-width:2px,color:#fff
    style LB fill:#e53935,stroke:#b71c1c,stroke-width:2px,color:#fff
    style JZ fill:#00acc1,stroke:#006064,stroke-width:2px,color:#fff
    style MON fill:#43a047,stroke:#1b5e20,stroke-width:2px,color:#fff
    style LOG fill:#43a047,stroke:#1b5e20,stroke-width:2px,color:#fff
    style START fill:#43a047,stroke:#1b5e20,stroke-width:2px,color:#fff
```

---

## 数据流

```mermaid
sequenceDiagram
    participant 陛下
    participant 飞书
    participant 内阁首辅
    participant 子 Agent
    participant 网关

    陛下->>飞书：发送消息
    飞书->>内阁首辅：转发消息
    内阁首辅->>内阁首辅：分析需求
    alt 简单任务
        内阁首辅->>子 Agent: 分派任务
        子 Agent->>子 Agent: 执行
        子 Agent-->>内阁首辅：返回结果
        内阁首辅->>飞书：发送回复
        飞书->>陛下：显示消息
    else 复杂任务
        内阁首辅->>子 Agent: 分派给多部协作
        子 Agent->>子 Agent: 协作执行
        子 Agent-->>内阁首辅：返回结果
        内阁首辅->>飞书：发送回复
        飞书->>陛下：显示消息
    end

    Note over 内阁首辅，网关：网关监控并行运行
    网关监控->>网关：每 30 秒检测
    alt 网关正常
        网关-->>网关监控：响应 OK
    else 网关断连
        网关监控->>网关：自动重启
        网关监控->>飞书：发送告警
    end
```

---

## Agent 职责

```mermaid
mindmap
  root((🏛️ 内阁首辅))
    三省
      中书省
        ::icon(fa fa-scroll)
        策略规划
        方案起草
      门下省
        ::icon(fa fa-check-circle)
        审核把关
        质量检查
      尚书省
        ::icon(fa fa-cogs)
        执行协调
        任务分派
    六部
      工部
        ::icon(fa fa-code)
        开发
        界面设计
      兵部
        ::icon(fa fa-shield-alt)
        算法
        核心技术
      户部
        ::icon(fa fa-database)
        数据
        资料整理
      礼部
        ::icon(fa fa-bell)
        日常事务
        查询服务
    独立
      监正
        ::icon(fa fa-eye)
        系统运维
        网关监控
```

---

## 网关监控流程

```mermaid
flowchart TD
    A[🔍 开始监控] --> B{WebSocket 检测}
    B -->|OK| C{HTTP 检测}
    B -->|FAIL| D[失败计数 +1]
    C -->|OK| E[重置计数器]
    C -->|FAIL| D
    D --> F{连续 3 次？}
    F -->|否 | B
    F -->|是 | G[🔄 自动重启网关]
    G --> H{重启成功？}
    H -->|是 | I[✅ 记录日志]
    H -->|否 | J[❌ 飞书告警]
    I --> B
    J --> B

    style A fill:#1e88e5,stroke:#0d47a1,color:#fff
    style B fill:#ffb74d,stroke:#e65100,color:#000
    style C fill:#ffb74d,stroke:#e65100,color:#000
    style D fill:#e53935,stroke:#b71c1c,color:#fff
    style E fill:#43a047,stroke:#1b5e20,color:#fff
    style F fill:#ffb74d,stroke:#e65100,color:#000
    style G fill:#1e88e5,stroke:#0d47a1,color:#fff
    style H fill:#ffb74d,stroke:#e65100,color:#000
    style I fill:#43a047,stroke:#1b5e20,color:#fff
    style J fill:#e53935,stroke:#b71c1c,color:#fff
```

---

## 配置状态

```mermaid
quadrantChart
    title 配置完成度
    x-axis 未完成 --> 已完成
    y-axis 不重要 --> 重要
    quadrant-1 优先完成
    quadrant-2 保持现状
    quadrant-3 可选优化
    quadrant-4 低优先级
    网关运行：[0.95, 0.95]
    内阁首辅飞书：[0.95, 0.9]
    网关监控：[0.9, 0.85]
    开机自启：[0.85, 0.7]
    9 个 Agent: [0.9, 0.8]
    监正配置：[0.7, 0.6]
    监正飞书配对：[0.3, 0.5]
```

---

## 关键指标

| 指标 | 数值 | 状态 |
|------|------|------|
| Agent 总数 | 9 个 | ✅ |
| 飞书账号 | 2 个 | ✅ |
| 网关端口 | 18789 | ✅ |
| 监控间隔 | 30 秒 | ✅ |
| 失败阈值 | 3 次 | ✅ |
| 重启重试 | 3 次 | ✅ |
| 日志文件 | 2 个 | ✅ |

---

**🏛️ 内阁首辅 - 青词 呈**
