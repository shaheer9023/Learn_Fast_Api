from rich import print
def introduction(firstname,lastname,age):
    dict={
        "firstname":firstname,
        "lastname":lastname,
        "age":age
    }
    print(dict)
introduction("shaheer","ahmad",21)