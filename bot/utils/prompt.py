import json


class Prompts:
    def __init__(self, model, msg=None):
        if msg is None:
            msg = []
        self.model = model
        self.temperature = 0.7
        self.messages = msg
        self.tools = []
        self.toolChoice = "auto"

    def addSystemMessage(self, content):
        """
        添加系统消息

        Args:
            content (str): 系统消息内容

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        self.messages.append({
            "role": "system",
            "content": content
        })
        return self

    def addUserMessage(self, content):
        """
        添加用户消息

        Args:
            content (str): 用户消息内容，可以是字符串或消息内容数组

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        if isinstance(content, str):
            self.messages.append({
                "role": "user",
                "content": content
            })
        else:
            self.messages.append({
                "role": "user",
                "content": content
            })
        return self

    def addAssistantMessage(self, content, toolCalls=None):
        """
        添加助手消息

        Args:
            content (str): 助手消息内容
            toolCalls (list, optional): 工具调用列表

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        message = {
            "role": "assistant",
            "content": content
        }

        if toolCalls:
            message["tool_calls"] = toolCalls

        self.messages.append(message)
        return self

    def addToolResponse(self, toolCallId, content):
        """
        添加工具响应消息

        Args:
            toolCallId (str): 工具调用ID
            content (str): 工具响应内容

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        self.messages.append({
            "role": "tool",
            "tool_call_id": toolCallId,
            "content": content
        })
        return self

    def addImage(self, imageUrl, detail="auto", messageIndex=-1):
        """
        向最后一条用户消息添加图片

        Args:
            imageUrl (str): 图片URL或base64编码
            detail (str): 图片详细程度，可选值：'auto', 'low', 'high'
            messageIndex (int): 要添加图片的消息索引，默认为最后一条消息

        Returns:
            Prompts: 返回自身以支持链式调用

        Raises:
            ValueError: 如果指定的消息不是用户消息或不存在
        """
        if not self.messages:
            raise ValueError("没有消息可添加图片")

        targetIndex = messageIndex if messageIndex >= 0 else len(self.messages) + messageIndex

        if targetIndex < 0 or targetIndex >= len(self.messages):
            raise ValueError(f"消息索引{messageIndex}超出范围")

        if self.messages[targetIndex]["role"] != "user":
            raise ValueError("只能向用户消息添加图片")

        # 确保content是列表格式
        if isinstance(self.messages[targetIndex]["content"], str):
            self.messages[targetIndex]["content"] = [{"type": "text", "text": self.messages[targetIndex]["content"]}]

        # add img
        image_content = {
            "type": "image_url",
            "image_url": {
                "url": imageUrl,
                "detail": detail
            }
        }

        self.messages[targetIndex]["content"].append(image_content)
        return self

    def defineTool(self, name, description, parameters):
        """
        定义一个工具

        Args:
            name (str): 工具名称
            description (str): 工具描述
            parameters (dict): 工具参数的JSON Schema

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        tool = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }

        self.tools.append(tool)
        return self

    def setModel(self, model):
        self.model = model
        return self

    def setToolChoice(self, choice):
        """
        设置工具选择模式

        Args:
            choice: 可以是"auto"、"none"或特定工具名称的字典

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        self.toolChoice = choice
        return self

    def setTemperature(self, temperature):
        self.temperature = temperature
        return self

    # def toDict(self):
    #     request = {
    #         "model": self.model,
    #         "messages": self.messages,
    #         "temperature": self.temperature,
    #         "max_tokens": self.maxTokens
    #     }
    #
    #     if self.tools:
    #         request["tools"] = self.tools
    #         request["tool_choice"] = self.toolChoice
    #
    #     return request

    # def keepLastNRounds(self, n):
    #     """
    #     保留最后n轮对话，每轮对话包含一对用户消息和助手消息
    #     系统消息总是被保留
    #
    #     Args:
    #         n (int): 要保留的对话轮数
    #
    #     Returns:
    #         Prompts: 返回自身以支持链式调用
    #     """
    #     if n <= 0:
    #         raise ValueError("轮数必须为正整数")
    #     if isinstance(self.messages, str):
    #         if self.messages.startswith("["):
    #             messagesList = json.loads(f"{self.messages}")
    #         else:
    #             messagesList = json.loads(f"[{self.messages}]")
    #     else:
    #         messagesList = self.messages
    #
    #     # 分离系统消息和对话消息
    #     systemMessages = [msg for msg in messagesList if msg["role"] == "system"]
    #     nonSystemMessages = [msg for msg in messagesList if msg["role"] != "system"]
    #
    #     # 按轮次组织消息
    #     rounds = []
    #     currentRound = []
    #
    #     for msg in nonSystemMessages:
    #         currentRound.append(msg)
    #
    #         # 当消息是助手消息时，认为一轮对话结束
    #         if msg["role"] == "assistant":
    #             rounds.append(currentRound)
    #             currentRound = []
    #
    #     # 处理可能剩余的未完成轮次
    #     if currentRound:
    #         rounds.append(currentRound)
    #
    #     # 只保留最后n轮
    #     keptRounds = rounds[-n:] if n < len(rounds) else rounds
    #
    #     # 重建消息列表
    #     finalMessages = systemMessages.copy()
    #     for round_msgs in keptRounds:
    #         finalMessages.extend(round_msgs)
    #
    #     # 更新消息列表
    #     self.messages = finalMessages
    #     return self
    def keepLastNRounds(self, n):
        """
        保留最后n轮对话，每轮对话包含一对用户消息和助手消息
        系统消息（第一条消息）总是被保留

        Args:
            n (int): 要保留的对话轮数

        Returns:
            Prompts: 返回自身以支持链式调用
        """
        if n <= 0:
            raise ValueError("轮数必须为正整数")
        if isinstance(self.messages, str):
            if self.messages.startswith("["):
                messagesList = json.loads(f"{self.messages}")
            else:
                messagesList = json.loads(f"[{self.messages}]")
        else:
            messagesList = self.messages

        # 假设第一条消息是系统消息
        systemMessage = messagesList[0:1]  # 取第一个消息
        nonSystemMessages = messagesList[1:]  # 取第一个消息之外的所有消息

        # 按轮次组织消息
        rounds = []
        currentRound = []

        for msg in nonSystemMessages:
            currentRound.append(msg)

            # 当消息是助手消息时，认为一轮对话结束
            if msg["role"] == "assistant":
                rounds.append(currentRound)
                currentRound = []

        # 处理可能剩余的未完成轮次
        if currentRound:
            rounds.append(currentRound)

        # 只保留最后n轮
        keptRounds = rounds[-n:] if n < len(rounds) else rounds

        # 重建消息列表
        finalMessages = systemMessage.copy()
        for round_msgs in keptRounds:
            finalMessages.extend(round_msgs)

        # 更新消息列表
        self.messages = finalMessages
        return self

    def toString(self):
        """
        将Prompts对象转换为易读的字符串格式

        Returns:
            str: 格式化的字符串表示
        """
        output = []

        # 添加基本配置信息
        output.append(f"Model: {self.model}")
        output.append(f"Temperature: {self.temperature}")
        output.append("")

        # 添加消息历史
        output.append("Messages:")
        for i, msg in enumerate(self.messages):
            role = msg["role"].upper()
            output.append(f"[{i}] {role}:")

            if role == "TOOL":
                output.append(f"  Tool Call ID: {msg.get('tool_call_id', 'N/A')}")
                output.append(f"  Content: {msg.get('content', '')}")
            elif role == "ASSISTANT" and "tool_calls" in msg:
                output.append(f"  Content: {msg.get('content', '')}")
                output.append("  Tool Calls:")
                for tool_call in msg["tool_calls"]:
                    output.append(f"    - ID: {tool_call.get('id', 'N/A')}")
                    output.append(f"      Function: {tool_call.get('function', {}).get('name', 'N/A')}")
                    output.append(f"      Arguments: {tool_call.get('function', {}).get('arguments', '{}')}")
            else:
                # 处理普通文本内容
                if isinstance(msg.get("content"), str):
                    output.append(f"  Content: {msg.get('content', '')}")
                # 处理多模态内容
                elif isinstance(msg.get("content"), list):
                    output.append("  Content (multimodal):")
                    for item in msg["content"]:
                        if item.get("type") == "text":
                            output.append(f"    - Text: {item.get('text', '')}")
                        elif item.get("type") == "image_url":
                            url = item.get("image_url", {}).get("url", "N/A")
                            detail = item.get("image_url", {}).get("detail", "auto")
                            output.append(f"    - Image: {url} (detail: {detail})")

        # 添加工具信息
        if self.tools:
            output.append("\nTools:")
            for i, tool in enumerate(self.tools):
                if tool.get("type") == "function":
                    func = tool.get("function", {})
                    output.append(f"[{i}] Function: {func.get('name', 'N/A')}")
                    output.append(f"  Description: {func.get('description', 'N/A')}")
                    output.append(f"  Parameters: {func.get('parameters', {})}")

            output.append(f"\nTool Choice: {self.toolChoice}")

        return "\n".join(output)
