import datetime as dt
import re
import statistics
import typing as tp

from ..vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    def age(day, month, year):
        today = dt.date.today()
        return today.year - year - ((today.month, today.day) < (month, day))

    friends = get_friends(user_id, fields=["bdate"]).items
    res = []
    for friend in friends:
        if "bdate" in friend:
            if re.findall(r"\d[.]\d[.]\d", friend["bdate"]):
                born = friend["bdate"].split(".")
                res.append(age(int(born[0]), int(born[1]), int(born[2])))
    return statistics.median(res) if res else None
