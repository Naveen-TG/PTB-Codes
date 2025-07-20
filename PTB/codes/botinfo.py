from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import (
    BotDescriptionLimit,
    BotNameLimit,
    ParseMode,
)
from telegram.error import TelegramError
from PTB import application, LOGGER  

class LimitExceededError(Exception):
    pass

async def SetMyName(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text(
                "❌ _Please provide a new bot name!_", parse_mode=ParseMode.MARKDOWN
            )
            return

        new_name = " ".join(context.args).strip()
        max_length = BotNameLimit.MAX_NAME_LENGTH.value

        if len(new_name) > max_length:
            await update.message.reply_text(
                f"❌ _Bot name too long!_ Maximum length is `{max_length}` characters.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        success = await context.bot.set_my_name(name=new_name)

        if success:
            await update.message.reply_text(
                f"✅ *Bot name updated successfully to:*\n`{new_name}`",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "⚠️ _Failed to update bot name. Try again later._",
                parse_mode=ParseMode.MARKDOWN
            )

    except TelegramError as e:
        LOGGER.error("TelegramError while setting bot name: %s", e)
        await update.message.reply_text(
            "🚫 _Telegram API Error occurred while updating the name._",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        LOGGER.error("Unexpected error in SetMyName: %s", e)
        await update.message.reply_text(
            "🚫 _An unexpected error occurred while setting the name._",
            parse_mode=ParseMode.MARKDOWN
        )

async def GetMyName(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        my_name = await context.bot.get_my_name()
        await update.message.reply_text(
            f"*📝 Current Bot Name:*\n`{my_name.name}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except TelegramError as e:
        LOGGER.error("Error getting bot name: %s", e)

async def SetMyDescription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if context.args:
            new_desc = " ".join(context.args).strip()
        elif update.message.reply_to_message and update.message.reply_to_message.text:
            new_desc = update.message.reply_to_message.text.strip()
        else:
            await update.message.reply_text(
                "❌ _Please provide a description or reply to a message with the desired description._",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        max_length = BotDescriptionLimit.MAX_DESCRIPTION_LENGTH.value

        if len(new_desc) > max_length:
            await update.message.reply_text(
                f"❌ _Description too long!_ Max length: `{max_length}` characters.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        success = await context.bot.set_my_description(description=new_desc)

        if success:
            await update.message.reply_text(
                f"✅ *Bot description updated!*```\n{new_desc}```",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "⚠️ _Failed to update the description. Try again later._",
                parse_mode=ParseMode.MARKDOWN
            )

    except TelegramError as e:
        LOGGER.error("TelegramError while setting bot description: %s", e)
        await update.message.reply_text(
            "🚫 _Telegram API Error while updating the description._",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        LOGGER.error("Unexpected error in SetMyDescription: %s", e)
        await update.message.reply_text(
            "🚫 _An unexpected error occurred._",
            parse_mode=ParseMode.MARKDOWN
        )

async def GetMyDescription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        desc = await context.bot.get_my_description()
        await update.message.reply_text(
            f"*📝 My Current Description:*```\n{desc.description}```",
            parse_mode=ParseMode.MARKDOWN,
        )
    except TelegramError as e:
        LOGGER.error("Error getting bot description: %s", e)

async def SetMyShortDescription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if context.args:
            new_short_desc = " ".join(context.args).strip()
        elif update.message.reply_to_message and update.message.reply_to_message.text:
            new_short_desc = update.message.reply_to_message.text.strip()
        else:
            await update.message.reply_text(
                "❌ _Please provide a short description or reply to a message containing it._",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        max_length = BotDescriptionLimit.MAX_SHORT_DESCRIPTION_LENGTH.value
        if len(new_short_desc) > max_length:
            await update.message.reply_text(
                f"❌ _Short description too long!_ Max allowed: *{max_length}* characters.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        await context.bot.set_my_short_description(short_description=new_short_desc)

        safe_desc = new_short_desc.replace("`", "'").replace("*", "")

        await update.message.reply_text(
            f"✅ *Short description updated!*\n`{safe_desc}`",
            parse_mode=ParseMode.MARKDOWN,
        )

    except TelegramError as e:
        LOGGER.error("TelegramError while setting short description: %s", e)
        await update.message.reply_text(
            "🚫 _Telegram API Error while updating the short description._",
            parse_mode=ParseMode.MARKDOWN,
        )

    except Exception as e:
        LOGGER.error("Unexpected error in SetMyShortDescription: %s", e)
        await update.message.reply_text(
            "🚫 _An unexpected error occurred._",
            parse_mode=ParseMode.MARKDOWN,
        )

async def GetMyShortDescription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        short_desc = await context.bot.get_my_short_description()
        await update.message.reply_text(
            f"*📝 My Short Description:*```\n{short_desc.short_description}```",
            parse_mode=ParseMode.MARKDOWN,
        )
    except TelegramError as e:
        LOGGER.error("Error getting short description: %s", e)

application.add_handler(CommandHandler("getmyname", GetMyName))
application.add_handler(CommandHandler("setmyname", SetMyName))
application.add_handler(CommandHandler("getmydescription", GetMyDescription))
application.add_handler(CommandHandler("setmydescription", SetMyDescription))
application.add_handler(CommandHandler("getmyshortdescription", GetMyShortDescription))
application.add_handler(CommandHandler("setmyshortdescription", SetMyShortDescription))

