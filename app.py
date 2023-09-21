from llm_utils import *
from pydantic_models import *
from prompt_templates import qna_template, complete_template


app = FastAPI()


@serve.deployment(
    user_config={"model_name": "facebook/opt-2.7b", "model_url": "http://localhost:8000/v1"},
    autoscaling_config=dict(
        min_replicas=2, max_replicas=6, target_num_ongoing_requests_per_replica=5
    ),
    ray_actor_options={"num_cpus": 2.0},
    health_check_period_s=10,
    health_check_timeout_s=30,
)
@serve.ingress(app)
class AppIngress:
    MODEL_NAME = "facebook/opt-2.7b"
    MODEL_URL = "http://localhost:8000/v1"

    def __init__(self):
        self.model_name = self.MODEL_NAME
        self.model_url = self.MODEL_URL
        self.llm = vllm(self.model_name, self.model_url)

    def reconfigure(self, config):
        self.model_name = config.get("model_name", self.MODEL_NAME)
        self.model_url = config.get("model_url", self.MODEL_URL)

    def ask_sync(self, prompt):
        res = run_llm(self.llm, prompt, template=qna_template)
        print(f"\nQuestion: {prompt}\nAnswer: {res}\n")
        return res

    def complete_sync(self, prompt):
        res = run_llm(self.llm, prompt, template=complete_template)
        print(f"\n{prompt} {res}\n")
        return res

    async def ask(self, prompt):
        res = await arun_llm(self.llm, prompt, template=qna_template)
        print(f"\nQuestion: {prompt}\nAnswer: {res}\n")
        return res

    async def complete(self, prompt):
        res = await arun_llm(self.llm, prompt, template=complete_template)
        print(f"\n{prompt} {res}\n")
        return res

    @app.post("/bg_ask")
    async def bg_task(
        self,
        question: str = Query(default="What is the meaning of life?"),
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ):
        background_tasks.add_task(self.ask, question)
        return JSONResponse(content={"Task": "Task Running"})

    @app.post("/ask")
    async def ask_question(
        self, question: str = Query(default="What is the meaning of life?")
    ):
        res = await self.ask(question)
        return JSONResponse(content={"Answer": res})

    @app.post("/complete")
    async def complete_sentence(self, sentence: str = Query(default="The meaning of life is")):
        res = await self.complete(sentence)
        return JSONResponse(content={"Completed": res})

    @app.post("/analyze")
    async def analyze_team(self, team_data: Team):
        prompt = f"Is {team_data.formation} a good formation for {team_data.name}?"
        res = await self.ask_question(prompt)
        return JSONResponse(content={"Analysis": res})
