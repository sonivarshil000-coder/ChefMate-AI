def format_recipe(recipe):

    recipe = recipe.replace("**", "")

    recipe = recipe.replace("*", "•")

    recipe = recipe.replace("#", "")

    return recipe