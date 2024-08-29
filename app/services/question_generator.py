from graphrag.query.question_gen.local_gen import (
    LocalQuestionGen,
    LocalContextBuilder,
)
from app.services.search_engine import create_search_engines


class ConcreteLocalContextBuilder(LocalContextBuilder):
    def build_context(self, *args, **kwargs):
        # Implement the build_context method
        pass


def create_question_generator():
    search_engines = create_search_engines()
    search_engine = search_engines[0]
    
    context_builder = (
        search_engine.context_builder 
        if isinstance(search_engine.context_builder, LocalContextBuilder)
        else ConcreteLocalContextBuilder()
    )

    return LocalQuestionGen(
        llm=search_engine.llm,
        context_builder=context_builder,
        token_encoder=search_engine.token_encoder,
        llm_params=search_engine.llm_params,
        context_builder_params=search_engine.context_builder_params,
    )


question_generator = create_question_generator()
