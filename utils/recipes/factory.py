from random import randint, choice
from faker import Faker

def rand_ratio():
    return randint(840,900), randint(473,573)

fake = Faker("pt_BR")

def make_recipe():
    return {
        "id": fake.random_number(digits=2, fix_len=True),
        "title":fake.sentence(nb_words=6),
        "description": fake.sentence(nb_words=12),
        "preparation_time": fake.random_number(digits=2, fix_len=True),
        "preparation_time_unit": "Minutos",
        "servings": fake.random_number(digits=2, fix_len=True),
        "servings_unit": "Porção",
        "preparation_steps": fake.text(3000),
        "created_at": fake.date_time(),
        "author": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name()
        },
        "category": {
            "name": fake.word(),
        },
        "cover": {
            "url": "https://loremflickr.com/%s/%s/food,cook" % rand_ratio(),
        },
    }

def gen_random_int():
    return randint(1,999999)

def make_test_recipe():
    title = fake.sentence(nb_words=6)
    title_splited = title.split()
    title_slug = ""
    for i in range(len(title_splited)):
        title_slug += title_splited[i]
    title_slug = title_slug[:len(title_slug)-1]
    return {
        "title":title,
        "description": fake.sentence(nb_words=12),
        "slug": title_slug,
        "preparation_time": fake.random_number(digits=2, fix_len=True),
        "preparation_time_unit": "Minutos",
        "servings": fake.random_number(digits=2, fix_len=True),
        "servings_unit": "Porção",
        "preparation_steps": fake.text(3000),
        "is_published": choice([True, False]),
        "preparation_steps_is_html": choice([True, False]),
    }

def make_test_author():
    return {
        "username":fake.word()+fake.word(),
        "first_name":fake.first_name(),
        "last_name":fake.last_name(),
        "email":fake.word()+"@"+fake.word()+".com",
        "password":"123456"
    }

def make_test_category():
    return {
        "name":fake.sentence(nb_words=2)
    }


if __name__ == '__main__':
    from pprint import pprint
    pprint(make_recipe())