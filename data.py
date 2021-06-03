def Articles(title,description,author,edit):
    articles = {
        'title' : title,
        'description' : description,
        'author' : author,
        'edit' : edit,
    }
    return articles

def Users(name, email, username, password):
    users = {
    'name' : name,
    'email' : email,
    'username' : username,
    'password': password
}
    return users