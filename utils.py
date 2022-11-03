from slugify import slugify
import uuid

def get_random():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code

'''
print(get_random())

txt = "Büşra Oran"
r = slugify(txt + " "+ get_random())
print(r)
print(type(r))
'''