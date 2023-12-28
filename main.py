
import openai
import os
import pandas as pd
import time
import requests
import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def get_completion(prompt, model="gpt-4-1106-preview"):
    # def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(model=model, messages=messages)

    return response.choices[0].message["content"]


def create_response(prompt):
    print()
    print("Response from ChatGPT:")
    print(prompt)


def similarity_checking(github_f, chatgpt_f):
    github_file = github_f

    with open(github_file, "r+") as file:
        github_data = file.read().replace('\n', '')
        file.write(github_data)
    # print(github_data)

    chatgpt_data = chatgpt_f.replace('\n', '')

    G = github_data
    C = chatgpt_data

    # tokenization
    G_list = word_tokenize(G)
    C_list = word_tokenize(C)

    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 = []
    l2 = []

    # remove stop words from the string
    G_set = {w for w in G_list if not w in sw}
    C_set = {w for w in C_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = G_set.union(C_set)
    for w in rvector:
        if w in G_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in C_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    cos_percentage = float(cosine * 100)

    return cos_percentage


if __name__ == "__main__":

    print()
    print("Write the topic or project name.")
    user_answer = input("Enter your answer: ")
    topic_name = user_answer
    openai.api_key = "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"  # Sir has provided this key
    # openai.api_key = "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"  # Created by own

    # data = input("Please enter a github text file:")

    if topic_name == 'AdmonitionBlock' or topic_name == 'admonitionBlock' or topic_name == 'admonitionblock' or topic_name == 'Admonitionblock':
        github_f = "C:/Users/User/PycharmProjects/automatedPromptUsingChatGPTAPI/admonitionBlock_github.txt"

    elif topic_name == 'Marlin' or topic_name == 'Test version' or topic_name == 'Test_version':
        github_f = "C:/Users/User/PycharmProjects/automatedPromptUsingChatGPTAPI/test_version_github.txt"

    with open(github_f, "r+") as file:
        github_data = file.read()
        file.write(github_data)
    # print(github_data)

    github_question = github_data + (
        " \n Now suppose you are a brilliant coder. So, identify the module, classes, functions and other important tokens to make a prompt like Create a module named ___ which will have a class __  or ask for complete a part of code or write a class __ with _____ . Module or function name should be taken from given code. Or make other prompts like asking create class name or create function __ in __ module. don't need to generate more lines only show the simple prompt. Ask the prompt in a single line.")

    # print(question)
    prompt = get_completion(github_question)

    print("Prompt to chatgpt:")
    print()
    print(prompt)

    response = get_completion(prompt)
    create_response(response)
    print(
        "____________________________________________________________________________________________________________________________________")

    chatgpt_f = response

    similarity = similarity_checking(github_f, chatgpt_f)
    print("similarity: ", similarity, "%")
    print(
        "____________________________________________________________________________________________________________________________________")

    highest_similarity = similarity

    for i in range(5):
        question2 = response + (
            " \n identify most important part of these couple of lines and check similarity with ") + github_data + (
                        " \n Now try to find difference between these 2 part and try to ask to create more specific code inside the class or function based on second part. Make a single line prompt based on previous part which will more clarify other tokens and ask to write part of specific code only. Besides, this single line prompt should be a follow up question of previous one. For example, complete a part of code __ or write the ____ or this __ function will contain ___ or firstly or secondly or on next create ____. Simply ask the prompt in single line.")
        prompt = get_completion(question2)
        print("Prompt to chatgpt:")
        print()
        print(prompt)

        response = get_completion(prompt)
        create_response(response)
        print(
            "____________________________________________________________________________________________________________________________________")

        chatgpt_f = response

        similarity = similarity_checking(github_f, chatgpt_f)
        print("similarity: ", similarity, "%")
        print(
            "____________________________________________________________________________________________________________________________________")

        if similarity > highest_similarity:
            highest_similarity = similarity

        if similarity < 75:
            continue
        else:
            break

    print("Highest Similarity is ", highest_similarity, "%")
