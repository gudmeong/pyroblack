#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
from datetime import datetime
import pyrogram
from pyrogram import raw, types, utils
from ..object import Object
from typing import List, Dict


class Giveaway(Object):
    """A giveaway.

    Parameters:
        chats (List of :obj:`~pyrogram.types.Chat`):
            List of channel(s) which host the giveaway.

        quantity (``int``):
            Quantity of the giveaway prize.

        months (``int``, *optional*):
            How long the telegram premium last (in month).

        stars (``int``, *optional*):
            How many stars the giveaway winner(s) get.

        expire_date (:py:obj:`~datetime.datetime`):
            Date the giveaway winner(s) will be choosen.

        new_subscribers (``bool``):
            True, if the giveaway only for new subscribers.

        additional_price (``str``, *optional*):
            Additional prize for the giveaway winner(s).

        allowed_countries (List of ``str``, *optional*):
            List of ISO country codes which eligible to join the giveaway.

        private_channel_ids (List of ``int``, *optional*):
            List of Unique channel identifier of private channel which host the giveaway.

        is_winners_hidden (``bool``):
            True, if the giveaway winners are hidden.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chats: List["types.Chat"],
        quantity: int,
        months: int,
        expire_date: datetime,
        new_subscribers: bool,
        stars: int = None,
        additional_price: str = None,
        allowed_countries: List[str] = None,
        is_winners_hidden: bool = None,
    ):
        super().__init__(client)

        self.chats = chats
        self.quantity = quantity
        self.months = months
        self.expire_date = expire_date
        self.new_subscribers = new_subscribers
        self.stars = stars
        self.additional_price = additional_price
        self.allowed_countries = allowed_countries
        self.is_winners_hidden = is_winners_hidden

    @staticmethod
    async def _parse(
        client, message: "raw.types.Message", chats: Dict[int, "raw.types.Chat"] = None
    ) -> "Giveaway":
        giveaway: "raw.types.MessageMediaGiveaway" = message.media
        chats = types.List(
            [
                types.Chat._parse_channel_chat(client, chats.get(i))
                for i in giveaway.channels
            ]
        )

        return Giveaway(
            chats=chats,
            quantity=giveaway.quantity,
            months=giveaway.months,
            expire_date=utils.timestamp_to_datetime(giveaway.until_date),
            new_subscribers=giveaway.only_new_subscribers,
            stars=giveaway.stars,
            additional_price=giveaway.prize_description,
            allowed_countries=(
                giveaway.countries_iso2 if len(giveaway.countries_iso2) > 0 else None
            ),
            is_winners_hidden=not giveaway.winners_are_visible,
            client=client,
        )
