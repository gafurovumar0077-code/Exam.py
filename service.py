from connection import *


async def create_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) Values
        ($1, $2, $3)
                     """, username, full_name, str(telegram_id))
        return True
    except Exception as Error:
        print(f"Create user Error: {Error}")
        return False
    finally:
        await conn.close()
        

async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()


async def add_recipe(title):
    conn = await connection_db()
    try:
        return await conn.fetchval(
            "insert into recipe(title) values ($1) returning recipe.recipe_id",
            title
        )
    except Exception as error:
        print(f"Adding recipe Error: {error}")
    finally:
        await conn.close()


async def add_ingredient(recipe_id, name, amount):
    conn = await connection_db()
    try:
        await conn.execute(
            """insert into ingredients(recipe_id, name, amount) values 
            ($1, $2, $3)""", recipe_id, name, amount
        )
        return True
    except Exception as error:
        print(f"Adding Ingredients Error: {error}")
        return False
    finally:
        await conn.close()
    


async def recipe(recipe_id):
    conn = await connection_db()
    try:
        rec = await conn.fetchrow("""
         select title from recipe 
         where recipe_id = $1""", recipe_id)
        return rec
    except Exception as error:
        print(f"Recipe Error: {error}")
    finally:
        await conn.close()
        


async def ingredints(recipe_id):
    conn = await connection_db()
    try:
        ingred = await conn.fetch("""
         select name, amount from ingredients
         where recipe_id = $1
                                      """, recipe_id)
        return ingred
    except Exception as error:
        print(f"Ingredients Error: {error}")
    finally:
        await conn.close()
        


async def add_to_plan(telegram_id, day_of_week, recipe_id):
    conn=await connection_db()
    try:
        if not (1 <= day_of_week <= 7):
            print("Ошибка: День недели должен быть от 1 до 7")
            return False
        user = await conn.fetchrow("""
            select user_id from users
            where telegram_id = $1
                                   """, str(telegram_id))
        
        recipe_exists = await conn.fetchrow("""
            select recipe_id from recipe
            where recipe_id = $1
        """, recipe_id)
        
        if not recipe_exists:
            print(f"Ошибка: Рецепт с ID {recipe_id} не существует!")
            return False
        
        await conn.execute("""
            insert into meal_plan(user_id, recipe_id, day_of_week) values
            ($1, $2, $3)
                           """, user["user_id"], recipe_id, int(day_of_week))
        return True
    except Exception as error:
        print(f"Plan Error {error}")
    finally:
        await conn.close()        
