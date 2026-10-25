import asyncpg
from dotenv import load_dotenv 
import os

load_dotenv()

pass_db = os.getenv("PASSWORD_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            user="postgres",
            database="shop_list",
            password=pass_db,
            host="localhost",
            port=5432
        )
        return conn
    except Exception as Error:
        print(f"Connection error: {Error}")
    
    
async def create_table_db():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            user_id serial primary key,
            username varchar(200),
            full_name varchar(200),
            telegram_id varchar(300),
            is_active boolean default true,
            created_at timestamp default now()
        );
        
        create table if not exists recipe(
            recipe_id serial primary key,
            title varchar(200),
            telegram_id varchar(300),
            is_active boolean default true,
            created_at timestamp default now()
        );
        create table if not exists ingredients(
            ingredients_id serial primary key,
            recipe_id int references recipe(recipe_id) on delete cascade,
            name varchar(200),
            amount int,
            created_at timestamp default now() 
        );

        create table if not exists meal_plan(
            meal_id serial primary key,
            user_id int references users(user_id) on delete cascade,
            recipe_id int references recipe(recipe_id) on delete cascade,
            day_of_week int,
            created_at timestamp default now()
        )
    
                     """)
        print("Table created!")
    except Exception as Error:
        print(f"Create table error: {Error}")
    finally:
        await conn.close()
