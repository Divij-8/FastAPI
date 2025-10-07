'''def get_full_name(first_name:str,last_name:str):
    full_name=first_name.title()+" "+last_name.title()
    return full_name

print(get_full_name("john","doe"))

def get_name_with_age(name:str,age:int):
    name_with_age=name+" is this old: "+str(age)
    return name_with_age

print(get_name_with_age("Alice",30))
'''
def process_items(items:list[str]):
    for item in items:
        print(item)

process_items(["apple","banana","cherry"])