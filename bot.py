import turingChat, math,re
from telegram.ext import Updater
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi')


def best(bot, update):
    bot.sendMessage(update.message.chat_id, text='Python is the best language ever.')


def calculate_permutations_and_combianations(bot, update, args):
    if not len(args[0]):
        send_message = 'Usage example:\n /AC 4C2\nResult: 6'
    else:
        try:
            re_result=re.match(r'\d+(\w)\d+',args[0])
            operation=re_result.group(1)
            if operation == 'C':
                re_result=re.match(r'(\d+)C(\d+)',args[0])
                first_number=int(re_result.group(1))
                second_number=int(re_result.group(2))
                result = math.factorial(first_number) / \
                         (math.factorial(second_number) * math.factorial(first_number - second_number))
            elif operation == 'A':
                re_result=re.match(r'(\d+)A(\d+)',args[0])
                first_number=int(re_result.group(1))
                second_number=int(re_result.group(2))
                result = math.factorial(first_number) / math.factorial(first_number - second_number)
            else:
                raise ValueError
            send_message = '%s(%s,%s) = %s' % (operation, first_number, second_number, int(result))
        except ValueError:
            send_message = 'Value error!\nUsage example:\n /AC 4C2\nResult: 6'
        except IndexError:
            send_message = 'Value error!\nUsage example:\n /AC 4C2\nResult: 6'
    bot.sendMessage(update.message.chat_id, text=send_message)


def study(bot, update, args):
    chat_id = update.message.chat_id
    try:
        due = int(args[0])
        if due < 0:
            bot.sendMessage(chat_id, text='好好學習！！！！')
            return

        def alarm(bot):
            bot.sendMessage(chat_id, text='時間到啦，可以休息一會')

        job_queue.put(alarm, due, repeat=False)
        bot.sendMessage(chat_id, text='%s 開始學習了呢, %s秒以後再來找我哦' % (update.message.from_user.username, due))
    except IndexError:
        bot.sendMessage(chat_id, text='Usage: /study <seconds> \n設置學習時間\n好好學習，自習滿績人生巔峯！')
    except ValueError:
        bot.sendMessage(chat_id, text='Usage: /study <seconds> \n設置學習時間\n好好學習，自習滿績人生巔峯！')

        # bot.sendMessage(update.message.chat_id, text='%s' % update.message.chat_id)


def echo(bot, update, args):
    print(args[0])
    if len(args[0]):
        send_message = args[0]
    else:
        send_message = 'Usage: /echo <message>'
    bot.sendMessage(update.message.chat_id, text=send_message)


def chat(bot, update, args):
    if len(args[0]):
        send_message = turingChat.turning_chat(update.message.text[5:], turing_key)
    else:
        send_message = 'Usage: /chat <chat message>'
    bot.sendMessage(update.message.chat_id, text=send_message)


def worst(bot, update):
    bot.sendMessage(update.message.chat_id, text='PHP is the worst language ever!!!!!!!!!')


def get_key():
    try:
        with open('key.txt') as key_file:
            tele_key = key_file.readline()
            turing_key = key_file.readline()
        return tele_key, turing_key
    except Exception as e:
        print(e)
        exit(0)


def main():
    global tele_key, turing_key, job_queue
    tele_key, turing_key = get_key()
    tele_key = tele_key[:-1]

    my_updater = Updater(tele_key)
    job_queue = my_updater.job_queue
    dp = my_updater.dispatcher

    command_list = {'start': start,
                    'study': study,
                    'best': best,
                    'worst': worst,
                    'echo': echo,
                    'chat': chat,
                    'AC': calculate_permutations_and_combianations}

    for (command, function) in command_list.items():
        dp.addTelegramCommandHandler(command, function)

    my_updater.start_polling()
    my_updater.idle()


if __name__ == '__main__':
    main()
