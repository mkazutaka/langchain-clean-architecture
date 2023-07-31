from dependency_injector import containers, providers

from app.gateway.chat_model.azure_chat_model import AzureChatModel
from app.gateway.chat_model.openai_chat_model import OpenAIChatModel
from app.interactor.chat_interactor import ChatInteractor


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.chat_completions",
        ]
    )

    openai_chat_model = providers.Factory(
        OpenAIChatModel,
        model_name=config.openai.model_name,
        openai_api_key=config.openai.api_key,
        streaming=True,
    )
    openai_chat_interactor = providers.Factory(
        ChatInteractor,
        chat_model=openai_chat_model,
    )

    azure_chat_model = providers.Factory(
        AzureChatModel,
        deployment_name=config.azure.openai.deployment_name,
        openai_api_key=config.azure.openai.api_key,
        openai_api_base=config.azure.openai.api_base,
        openai_api_version=config.azure.openai.api_version,
        streaming=True,
    )
    azure_chat_interactor = providers.Factory(
        ChatInteractor,
        chat_model=azure_chat_model,
    )
