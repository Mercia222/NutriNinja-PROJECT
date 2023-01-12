import requests
‘’'import sqlite3 as sql
#import json’’'
import urllib
from random import randint
IDS = {-1}
APP_ID = “c7fcb2a3”
API_KEY = “98d03f85fae4e195ff9791b508627c99"
URL = f’https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'
def main():
    print()
    print(‘Welcome! I am NutriNinja and I am your guide today! What is your name?‘)
    name = input(‘\t>>> ‘)
    print(f’Hello, {name}! Hope you have a great time with me!‘)
    print()
    command = ‘’
    while command.lower() != ‘q’:
        print(“Are you looking for a Recipe?“)
        print(“1) Yes”)
        print(“2) No”)
        command = input(“\t>>> “)
        print()
        if command == ‘1’:
            query_recipes()
        elif command == ‘2’:
            print(‘Uhohhh! Okay, Have a great day!’)
            break
def query_recipes():
    response = None
    success = False
    index = 0
    while not success:
        print(“Please enter an ingredient:“)
        key_word = input(“\t>>> “)
        data = make_request(get_url_q(key_word))
        data = data[‘hits’]
        if len(data) > 0:
            success = True
        else:
            print(f'0 results for “{key_word}“’)
            input(“”)
    index = display_recipe_labels(data, index)
    print(f”   Select Recipe # (1-{index})\n   (enter ‘m’ to see more)“)
    select = select_from_index(index)
    if select == ‘m’ and index == 20:
        _from = 20
        to = 40
        data2 = make_request(get_url_q(key_word, _from, to))
        data2 = data2[‘hits’]
        index = display_recipe_labels(data2, index)
        data += data2
        select = -1
    select_recipe(data, index, select)
def select_recipe(data,max_index,select):
    invalid = True
    while invalid:
        if select == -1:
            select = select_recipe_from_index(max_index)
        if select == ‘m’:
            display_recipe_labels(data,0)
            select = select_recipe_from_index(max_index)
        if select == ‘q’:
            print()
            return
        try:
            select = int(select)
            invalid = False
        except ValueError:
            invalid = True
            select = -1
    recipe_response = data[select]
    recipe = recipe_response[“recipe”]
    curr_recipe = filter_response(recipe)
    display_recipe_dict(curr_recipe)
    if input(“Would you like to start cooking this recipe? y/n”) == ‘y’:
        print(‘Enjoy! I hope the recipe turns out great, thank you for choosing NutriNinja!’)
    else:
        print()
        print(“1) Give another recipe a try?“)
        print(“2) Go to main menu”)
        command = input(“\t>>> “)
        if command == ‘1’:
            select_recipe(data,max_index,-1)
        else:
            print()
def display_recipe_labels(data, index):
    print()
    for recipe in data:
        index += 1
        print(f”   {index})“, recipe[‘recipe’][‘label’])
    print()
    return index
def select_recipe_from_index(max_index):
    print(f”   Select Recipe # (1-{max_index})“)
    return select_from_index(max_index)
def select_from_index(max_index):
    select = -1
    while select <= 0 or select > max_index:
        select = input(“\t>>> “)
        if select.lower() == ‘q’:
            return ‘q’
        elif select.lower() == ‘m’:
            return ‘m’
        try:
            select = int(select)
        except ValueError as e:
            print(“Input must be an integer!“)
            select = -1
    return select-1
def filter_response(recipe):
    curr_recipe = {
        “ingredients_line” : recipe[“ingredientLines”],
        “ingredients” : recipe[“ingredients”],
        “label” : recipe[“label”],
        “url” : recipe[“url”],
        “uri” : recipe[“uri”]}
    return curr_recipe
def display_recipe_dict(curr_recipe):
    print()
    print(“====================================================“)
    print(f”{curr_recipe[‘label’]}:“)
    print(“----------------------------------------------------“)
    for line in curr_recipe[“ingredients_line”]:
        print(f”    - {line}“)
    print()
    print(f”Directions: {curr_recipe[‘url’]}“)
    print(“====================================================“)
    input()
def make_request(url):
    response = requests.get(url)
    data = response.json()
    return data
def get_url_q(key_word,_from=0,to=20):
    url = URL + f’&q=${key_word}&to={to}&from={_from}'
    return url
def get_url_r(uri):
    return URL + f’&r={uri}'
main()