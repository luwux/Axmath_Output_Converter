import re
import pyperclip

displaymath = 1
autoinline = 1
addblank = 1


def add_dollar_signs(s):
    return f"${s}$"


def delete_blank(input_str):
    dollar_count = 0  # 用于计算$的数量
    output = []  # 用列表来构建输出字符串

    i = 0
    while i < len(input_str):
        if input_str[i] == "$":
            dollar_count += 1
            output.append(input_str[i])

            # 如果是奇数个$，则检查下一个字符是否为空格
            if (
                dollar_count % 2 != 0
                and i + 1 < len(input_str)
                and input_str[i + 1] == " "
            ):
                i += 1  # 跳过空格
            # 如果是偶数个$，则检查前一个字符是否为空格
            elif dollar_count % 2 == 0 and len(output) > 1 and output[-2] == " ":
                output = output[:-2]  # 移除空格和$
                output.append("$")  # 重新加入$
        else:
            output.append(input_str[i])
        i += 1

    return "".join(output)  # 将列表转换为字符串并返回


def add_blank(input_str):
    dollar_count = 0  # 用于计数$的数量
    output_str = ""  # 初始化输出字符串

    for i, char in enumerate(input_str):
        if char == "$":
            dollar_count += 1  # 遇到$时计数增加

            if dollar_count % 2 == 0:  # 第偶数个$
                output_str += char
                if i != len(input_str) - 1 and input_str[i + 1] != '，' and input_str[i + 1] != '。':
                    output_str += " "  # 在$后面添加空格
            else:  # 第奇数个$
                if i != 0 and input_str[i - 1] != '，' and input_str[i - 1] != '。': # 若$不是第一个字符
                    output_str += " "  # 在$前面添加空格
                output_str += char
        else:
            output_str += char  # 复制非$字符

    return output_str


def replace_before1(s, before, after):
    return s.replace(before, after)


def convert_latex_single_line(input_str):
    output = ["$"]  # 在开头添加 $
    i, j = 0, 1  # 从索引 1 开始，为开头的 $ 留空间
    inkuohao = 0 # 确认是否位于大括号内
    inbigkuohao = 0 # 确认是否位于 latex 需要闭合的括号内
    inlineornot = 0
    in_latex_text = False # 是否位于 \text{} 内

    while i < len(input_str):
        # 如果是换行符，跳过它
        if input_str[i] == "\n":
            i += 1
            continue

        # 检查 \text{ 命令的开始
        if input_str[i : i + 6] == "\\text{" and inkuohao == 0:
            i += 6
            output.append("$")
            in_latex_text = True
            inlineornot += 1
            continue

        # 检查 LaTeX 文本模式的结束
        if input_str[i] == "}" and in_latex_text:
            output.append("$")
            if displaymath == 1 and (autoinline == 0 or inlineornot != 0):
                output.extend(list("\\displaystyle "))
            in_latex_text = False
            i += 1
            continue

        # 括号的处理
        if input_str[i] == "{" and not in_latex_text:
            inkuohao += 1
        if input_str[i] == "}" and not in_latex_text:
            inkuohao -= 1

        # 识别是否在大圆括号内以便优化括号内文字
        if input_str[i] == "(" and i >= 5 and input_str[i - 5 : i + 1] == '\\left(' and not in_latex_text:
            inbigkuohao += 1
        if input_str[i] == ")" and i >= 5 and input_str[i - 6 : i + 1] == '\\right)' and not in_latex_text:
            inbigkuohao -= 1

        # 复制当前字符（包括 \ 字符）
        output.append(input_str[i])

        # 移动到下一个字符
        i += 1

    output.append("$")  # 在结尾添加 $
    output_str = "".join(output)

    # 处理连续的两个 $ 符号
    output_str = output_str.replace("$$", "")

    # 结束处理部分，处理inline，displaystyle等事情
    if (
        output_str.startswith("$")
        and displaymath == 1
        and (autoinline == 0 or inlineornot != 0)
    ):
        output_str = "$\\displaystyle " + output_str[1:]

    # 替换部分模式
    output_str = output_str.replace("$.$", ".") # 去除多余的点点，下同
    output_str = output_str.replace("$\\displaystyle $", "")
    output_str = output_str.replace("$\\displaystyle .$", ".")
    output_str = output_str.replace("$\\displaystyle .\\,\\,$", ". ")
    output_str = output_str.replace("\\mathrm{arc}\\tan", "\\arctan") # 将 \mathrm{arc}\tan 替换为 \arctan

    # 删除空白字符
    output_str = delete_blank(output_str)

    # 添加空白
    if addblank == 1:
        output_str = add_blank(output_str)

    # 添加美元符号
    if autoinline == 1 and inlineornot == 0 and len(input_str) != 0:
        output_str = "$" + output_str + "$"

    return output_str


def convert_latex_multiline(input_str):
    max_lines = 100
    max_line_length = 7000

    lines = input_str.split("\n\\\\\n")[
        :max_lines
    ]  # 将输入字符串按 "\n\\\\\n" 分割成多行
    converted_lines = []

    for line in lines:
        converted_line = convert_latex_single_line(
            line[:max_line_length]
        )  # 调用已定义的函数转换每一行
        converted_lines.append(converted_line)

    output_str = "\n".join(converted_lines)  # 将转换后的多行合并成一个字符串
    return output_str


pyperclip.copy(convert_latex_multiline(pyperclip.paste()))
