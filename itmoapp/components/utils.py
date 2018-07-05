import random
import string


class Utils:

    @staticmethod
    def endings(count, form1, form2, form5):
        """
        Return word with right ending

        :param integer count:
        :param string form1: стол, дерево, ложка
        :param string form2: стола, дерева, ложки
        :param string form5: столов, деревьев, ложек
        :return:
        """
        n = count % 100
        n1 = count % 10

        if 10 < n < 20:
            return form5

        if 1 < n1 < 5:
            return form2

        if n1 == 1:
            return form1

        return form5

    @staticmethod
    def generate_hash(size=8, chars=string.ascii_uppercase + string.digits):
        """
        Generate unique string

        :param size: size in symbols
        :param chars: letters used
        :return: string token
        """
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

    @staticmethod
    def satisfaction_emoji(percentage):
        """
        Return emoji for satisfaction percentage

        :param percentage:
        :return:
        """
        emoji = {
            "100": "😎",
            "90": "😄",
            "80": "😏",
            "70": "🙂",
            "60": "😐",
            "50": "🙁",
            "40": "😒",
            "30": "😞",
            "20": "😣",
            "10": "😫",
            "0": "😵"
        }

        if percentage >= 100:
            index = "100"
        elif percentage < 0:
            index = "0"
        else:
            index = str((percentage // 10) * 10)

        return emoji[index]

    @staticmethod
    def create_collection_name(collection, payload):
        """
        Add bot hash from payload to collection name if it exists

        :param string collection:
        :param payload:
        :return string:
        """
        bot_hash = payload.get('bot', '')

        if bot_hash:
            collection = "{}:{}".format(bot_hash, collection)

        return collection
