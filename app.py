from app_utils import *
from redis_kv_store import *
from async_llm_utils import *
from pydantic_models import *
from prompt_templates import *


app = FastAPI()


@serve.deployment(
    health_check_period_s=10,
    health_check_timeout_s=30,
)
@serve.ingress(app)
class AppIngress:
    LLM_CONFIG = {}
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    def __init__(self):
        self.llm_config = self.LLM_CONFIG
        self.redis_host = self.REDIS_HOST
        self.redis_port = self.REDIS_PORT
        self.set_up()

    def init_kv_store(self):
        self.kv_store = KeyValueStore(redis_host=self.redis_host, redis_port=self.redis_port)

    def init_llm(self):
        if "llm_fn" not in self.llm_config:
            self.llm_config["llm_fn"] = None
        llm_fn = llm_fn_dict.get(self.llm_config["llm_fn"], None)
        if llm_fn is not None:
            self.llm = llm_fn(**{k: v for k, v in self.llm_config.items() if k != "llm_fn"})
        else:
            self.llm = None

    def set_up(self):
        self.init_kv_store()
        self.init_llm()

    def reconfigure(self, config):
        self.llm_config = config.get("llm_config", self.LLM_CONFIG)
        self.redis_host = config.get("redis_host", self.REDIS_HOST)
        self.redis_port = config.get("redis_port", self.REDIS_PORT)
        self.set_up()

    @app.get("/task/{task_id}")
    async def get_task(self, task_id: str):
        task = self.kv_store.get(task_id)
        return JSONResponse(content=task)

    @app.post("/bulk_task")
    async def bulk_task(
        self,
        input: str = Query(default="Hello Background Task!"),
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ):
        task_id = start_task(self.kv_store)
        background_tasks.add_task(long_running_task, input=input)
        return JSONResponse(content={"Task": "Task Running"})

    @app.post("/ask")
    async def ask_question(
        self, question: str = Query(default="What is the meaning of life?")
    ):
        task_id = start_task(self.kv_store)
        try:
            res = await async_ask_q(self.llm, question)
        except Exception as e:
            fail_task(task_id, self.kv_store, str(e))
        return JSONResponse(content={"Answer": res})

    @app.post("/industry_problem")
    async def industry_problem(self, problem: IndustryProblem):
        task_id = start_task(self.kv_store)
        try:
            res = await async_run_llm(
                self.llm, problem.dict(), template=industry_problem_template
            )
        except Exception as e:
            fail_task(task_id, self.kv_store, str(e))
        return JSONResponse(content={"Answer": res})

    @app.post("/analyze")
    async def analyze_team(self, team_data: Team):
        task_id = start_task(self.kv_store)
        try:
            prompt = f"Is {team_data.formation} a good formation for {team_data.name}?"
            res = await async_ask_q(self.llm, prompt)
        except Exception as e:
            fail_task(task_id, self.kv_store, str(e))
        return JSONResponse(content={"Analysis": res})
