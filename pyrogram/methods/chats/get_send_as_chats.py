#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import List, Optional, Union

import pyrogram
from pyrogram import raw, types


class GetSendAsChats:
    async def get_send_as_chats(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        for_paid_reactions: Optional[bool] = None,
    ) -> List["types.Chat"]:
        """Get the list of "send_as" chats available.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            for_paid_reactions (``bool``, *optional*):
                Pass True to get the list of available send_as chats for paid reactions.

        Returns:
            List[:obj:`~pyrogram.types.Chat`]: The list of chats.

        Example:
            .. code-block:: python

                chats = await app.get_send_as_chats(chat_id)
                print(chats)
        """
        r = await self.invoke(
            raw.functions.channels.GetSendAs(
                peer=await self.resolve_peer(chat_id),
                for_paid_reactions=for_paid_reactions,
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        send_as_chats = types.List()

        for p in r.peers:
            if isinstance(p.peer, raw.types.PeerUser):
                send_as_chats.append(
                    types.Chat._parse_chat(self, users[p.peer.user_id])
                )
            else:
                send_as_chats.append(
                    types.Chat._parse_chat(self, chats[p.peer.channel_id])
                )

        return send_as_chats
