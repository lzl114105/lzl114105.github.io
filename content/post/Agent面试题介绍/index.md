---
title: "Agent面试题介绍"
slug: "Agent面试题介绍"
description: ""
date: 2026-10-26T21:57:36+08:00
image: ""
categories:
    - 技术
tags:
draft: false
---

<!--more-->

## 什么是Agent？与大模型有什么本质不同？

### 回答：

- 我理解的Agent和大模型最主要的区别就是\[自主性]和\[能行动]。
- 传统大模型就是对话式的，问一句答一句，不会拆分复杂任务自己完成，而现在的Agent有自己的规划能力，能主动拆分任务，通过调用工具、访问记忆、感知环境来一步步执行，最终完成任务。

### 解析：

- 普通大模型缺陷：
  1. 知识冻结
  2. 无法行动
  3. 没有持续状态

- Agent核心逻辑：感知->规划->行动->再感知
- 核心能力：
  1. 工具调用：知识冻结找搜索引擎；不能行动接邮件API，代码执行器；
     ```python
     tools = [
       {
         "name": "get_weather",
         "description": "获取指定城市的天气",
         "parameters" :{
           "type": "object",
           "properties": {
             "city" :{"type": "string", "description": "城市名"}
           },
           "required": ["city"]
         }
       },
       {
         "name": "send_mail",
         "description": "发送邮件给指定联系人",
         "parameters": {
           "type": "object",
           "properties": {
             "to": {"type": "object"},
             "subject": {"type": "string"},
             "body": {"type": "string}
           },
           "required": ["to", "subject", "body"]
         }
       }
     ]
     ```

  2. 记忆机制：短期记忆存储在上下文，长期记忆存储在向量数据库

  3. 多步推理和自我纠错

## Harness是什么？

- 是大模型智能体的运行底座，不属于大模型本身。大模型只负责推理和生成思考，Harness负责[思考->行动->观察]的agent循环，提供管控、隔离、校验、约束模型行为、解决幻觉、死循环、工具异常等问题。
- 核心组成

  1. 循环调度器：
  2. 上下文与状态管理
  3. 工具网关
  4. 结果校验层

### Agent沙箱应该如何设计？

- 核心是让代码只拿到当前任务所需要的权限，并把资源消耗限制在预算内。模型生成的代码要按照不可信代码处理，不能只靠prompt约束，也不应该继承宿主的全部权限
- 执行环境可以只提供本次任务的输入，把输入设置为只读，给临时目录和输出目录写权限，用地权限身份运行，网络按需开放
