import telegram
from config import tokens
from Connection import Connection


class Bot():
  def __init__(self, channel_name: str):
    self._bot = telegram.Bot(tokens['bot'])
    self._connection = Connection()
    self._channel_name = channel_name
  
  def send_message(self, message: str, disable_notification=True, disable_preview=True) -> telegram.Message:
    message_sent = self._bot.send_message(
      chat_id=self._channel_name, text=message, parse_mode=telegram.ParseMode.MARKDOWN,
      disable_notification=disable_notification, disable_preview=disable_preview
    )
    self._connection.insert_message(message_sent.message_id, message_sent.date, message, self._channel_name)
    return message_sent
  
  def delete_message(self, message_id: int) -> bool:
    self._connection.mark_delete(message_id=message_id, channel_name=self._channel_name)
    return self._bot.delete_message(chat_id=self._channel_name, message_id=message_id)
  
  def clean_channel(self):
    yesterday_not_deleted = self._connection.get_yesterday_not_deleted()
    for message in yesterday_not_deleted:
      self._delete_message(message_id=message)
