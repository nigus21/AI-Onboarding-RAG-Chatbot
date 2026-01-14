from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # type: ignore
from langchain_core.output_parsers import StrOutputParser  # type: ignore
from langchain_core.runnables import RunnablePassthrough  # type: ignore


class Assistant:
    def __init__(
        self,
        system_prompt,
        llm,
        message_history=[],
        vector_store=None,
        employee_information=None,
    ):
        self.system_prompt = system_prompt
        self.llm = llm
        self.messages = message_history
        self.vector_store = vector_store
        self.employee_information = employee_information

        self.chain = self._get_conversation_chain()

    def get_response(self, user_input):
        return self.chain.stream(user_input)

    def _get_conversation_chain(self):
        prompt = ChatPromptTemplate(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder("conversation_history"),
                ("human", "{user_input}"),
            ]
        )

        llm = self.llm

        output_parser = StrOutputParser()

        def _get_retrieved_policies(_):
            # If the vector store failed to initialize (e.g. due to API quota),
            # gracefully degrade by returning an empty string instead of crashing.
            if self.vector_store is None:
                return ""
            return self.vector_store.as_retriever()

        chain = (
            {
                "retrieved_policy_information": _get_retrieved_policies,
                "employee_information": lambda x: self.employee_information,
                "user_input": RunnablePassthrough(),
                "conversation_history": lambda x: self.messages,
            }
            | prompt
            | llm
            | output_parser
        )
        return chain