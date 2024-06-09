from environs import Env

env = Env()

env.read_env()

BOT_TOKEN: str = env.str('BOT_TOKEN')

FSM_HOST: str = env.str("FSM_HOST")
FSM_PORT: int = env.int("FSM_PORT")
FSM_PASSWORD: str = env.str("FSM_PASSWORD")

DATABASE_NAME: str = env.str("DATABASE_NAME")

