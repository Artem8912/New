import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class SomeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        state: FSMContext = data.get('state')
        user_state = await state.get_state()
        user_data = await state.get_data()
        
        logger.debug('User state is %s, user data is %s', user_state, user_data)

        return await handler(event, data)

# class FSMContext:
#     def __init__(self, storage: BaseStorage, key: StorageKey) -> None:
#         self.storage = storage
#         self.key = key

#     async def set_state(self, state: StateType = None) -> None:
#         await self.storage.set_state(key=self.key, state=state)

#     async def get_state(self) -> Optional[str]:
#         return await self.storage.get_state(key=self.key)

#     async def set_data(self, data: Dict[str, Any]) -> None:
#         await self.storage.set_data(key=self.key, data=data)

#     async def get_data(self) -> Dict[str, Any]:
#         return await self.storage.get_data(key=self.key)

#     async def update_data(
#         self, data: Optional[Dict[str, Any]] = None, **kwargs: Any
#     ) -> Dict[str, Any]:
#         if data:
#             kwargs.update(data)
#         return await self.storage.update_data(key=self.key, data=kwargs)

#     async def clear(self) -> None:
#         await self.set_state(state=None)
#         await self.set_data({})