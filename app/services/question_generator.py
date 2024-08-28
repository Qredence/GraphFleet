from graphrag.query.question_gen.local_gen import LocalQuestionGen
from app.services.search_engine import create_search_engine

def create_question_generator():
    search_engine = create_search_engine()
    
    return LocalQuestionGen(
        llm=search_engine.llm,
        context_builder=search_engine.context_builder,
        token_encoder=search_engine.token_encoder,
        llm_params=search_engine.llm_params,
        context_builder_params=search_engine.context_builder_params,
    )

question_generator = create_question_generator()