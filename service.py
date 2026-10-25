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
    
