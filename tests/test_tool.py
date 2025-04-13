from typing import List, Union

from vkbottle_types.codegen.objects import MessagesGetConversationByIdExtended, MessagesGetConversationById
from vkbottle_types.objects import UsersUserFull

from AmperChatBot.handlers.ABC.ABCAmper import AApiVk

class EUserType:
    BASIC = {
        "id": 689207910,
        "deactivated": None,
        "first_name": "Андрей",
        "hidden": None,
        "last_name": "Васильевич",
        "can_access_closed": True,
        "is_closed": False,
        "sex": None,
        "screen_name": None,
        "photo_50": None,
        "photo_100": None,
        "online_info": None,
        "online": None,
        "online_mobile": None,
        "online_app": None,
        "verified": None,
        "trending": None,
        "friend_status": None,
        "mutual": None,
        "first_name_nom": None,
        "first_name_gen": None,
        "first_name_dat": None,
        "first_name_acc": None,
        "first_name_ins": None,
        "first_name_abl": None,
        "last_name_nom": None,
        "last_name_gen": None,
        "last_name_dat": None,
        "last_name_acc": None,
        "last_name_ins": None,
        "last_name_abl": None,
        "nickname": None,
        "maiden_name": None,
        "contact_name": None,
        "domain": None,
        "bdate": None,
        "city": None,
        "timezone": None,
        "owner_state": None,
        "photo_200": None,
        "photo_max": None,
        "photo_200_orig": None,
        "photo_400_orig": None,
        "photo_max_orig": None,
        "photo_id": None,
        "has_photo": None,
        "has_mobile": None,
        "is_friend": None,
        "is_best_friend": None,
        "wall_comments": None,
        "can_post": None,
        "can_see_all_posts": None,
        "can_see_audio": None,
        "type": None,
        "email": None,
        "skype": None,
        "facebook": None,
        "facebook_name": None,
        "twitter": None,
        "livejournal": None,
        "instagram": None,
        "test": None,
        "video_live": None,
        "is_video_live_notifications_blocked": None,
        "is_service": None,
        "service_description": None,
        "photo_rec": None,
        "photo_medium": None,
        "photo_medium_rec": None,
        "photo": None,
        "photo_big": None,
        "photo_400": None,
        "photo_max_size": None,
        "language": None,
        "stories_archive_count": None,
        "has_unseen_stories": None,
        "wall_default": None,
        "can_call": None,
        "can_call_from_group": None,
        "can_invite_as_voicerooms_speaker": None,
        "can_see_wishes": None,
        "can_see_gifts": None,
        "interests": None,
        "books": None,
        "tv": None,
        "quotes": None,
        "about": None,
        "games": None,
        "movies": None,
        "activities": None,
        "music": None,
        "can_write_private_message": None,
        "can_send_friend_request": None,
        "can_be_invited_group": None,
        "mobile_phone": None,
        "home_phone": None,
        "site": None,
        "status_audio": None,
        "status": None,
        "activity": None,
        "status_app": None,
        "last_seen": None,
        "exports": None,
        "crop_photo": None,
        "followers_count": None,
        "video_live_level": None,
        "video_live_count": None,
        "clips_count": None,
        "blacklisted": None,
        "blacklisted_by_me": None,
        "is_favorite": None,
        "is_hidden_from_feed": None,
        "common_count": None,
        "occupation": None,
        "career": None,
        "military": None,
        "university": None,
        "university_name": None,
        "university_group_id": None,
        "faculty": None,
        "faculty_name": None,
        "graduation": None,
        "education_form": None,
        "education_status": None,
        "home_town": None,
        "relation": None,
        "relation_partner": None,
        "personal": None,
        "universities": None,
        "schools": None,
        "relatives": None,
        "is_subscribed_podcasts": None,
        "can_subscribe_podcasts": None,
        "can_subscribe_posts": None,
        "counters": None,
        "access_key": None,
        "can_upload_doc": None,
        "can_ban": None,
        "hash": None,
        "is_no_index": None,
        "contact_id": None,
        "is_message_request": None,
        "descriptions": None,
        "lists": None
    }


class TUser:
    BASIC_DATA = [UsersUserFull(
            id=689207910, deactivated=None, first_name='Андрей',
            hidden=None, last_name='Васильевич', can_access_closed=True, is_closed=False, sex=None, screen_name=None,
            photo_50=None, photo_100=None, online_info=None, online=None, online_mobile=None, online_app=None,
            verified=None, trending=None, friend_status=None, mutual=None, first_name_nom=None,
            first_name_gen=None, first_name_dat=None, first_name_acc=None, first_name_ins=None, first_name_abl=None,
            last_name_nom=None, last_name_gen=None, last_name_dat=None, last_name_acc=None, last_name_ins=None,
            last_name_abl=None, nickname=None, maiden_name=None, contact_name=None, domain=None, bdate=None, city=None,
            timezone=None, owner_state=None, photo_200=None, photo_max=None, photo_200_orig=None, photo_400_orig=None,
            photo_max_orig=None, photo_id=None, has_photo=None, has_mobile=None, is_friend=None, is_best_friend=None,
            wall_comments=None, can_post=None, can_see_all_posts=None, can_see_audio=None, type=None, email=None,
            skype=None, facebook=None, facebook_name=None, twitter=None, livejournal=None, instagram=None, test=None,
            video_live=None, is_video_live_notifications_blocked=None, is_service=None, service_description=None,
            photo_rec=None, photo_medium=None, photo_medium_rec=None, photo=None, photo_big=None, photo_400=None,
            photo_max_size=None, language=None, stories_archive_count=None, has_unseen_stories=None, wall_default=None,
            can_call=None, can_call_from_group=None, can_invite_as_voicerooms_speaker=None, can_see_wishes=None,
            can_see_gifts=None, interests=None, books=None, tv=None, quotes=None, about=None, games=None, movies=None,
            activities=None, music=None, can_write_private_message=None, can_send_friend_request=None,
            can_be_invited_group=None, mobile_phone=None, home_phone=None, site=None, status_audio=None, status=None,
            activity=None, status_app=None, last_seen=None, exports=None, crop_photo=None, followers_count=None,
            video_live_level=None, video_live_count=None, clips_count=None, blacklisted=None, blacklisted_by_me=None,
            is_favorite=None, is_hidden_from_feed=None, common_count=None, occupation=None, career=None, military=None,
            university=None, university_name=None, university_group_id=None, faculty=None, faculty_name=None,
            graduation=None, education_form=None, education_status=None, home_town=None, relation=None,
            relation_partner=None, personal=None, universities=None, schools=None, relatives=None,
            is_subscribed_podcasts=None, can_subscribe_podcasts=None, can_subscribe_posts=None, counters=None,
            access_key=None, can_upload_doc=None, can_ban=None, hash=None, is_no_index=None, contact_id=None,
            is_message_request=None, descriptions=None, lists=None)]
    USER = BASIC_DATA

    def get_data(self): return self.USER

    def __set_data_user__(self, **data):
        for key, value in data.items():
            if hasattr(self.BASIC_DATA[0], key):
                self.USER[0] = self.USER[0].copy(update=data)

    def __init__(self, **data):
        self.__set_data_user__(**data)


class TApiVK(AApiVk):
    """get_creator_chat"""
    async def get_creater_chat(self, peer_id: Union[str, int]) -> int: return 550091249
    async def get_creater_chat_none(self, peer_id: Union[str, int]) -> None: return None


    """is_creater_chat"""
    async def is_creater_chat(self, id_user: Union[str, int], peer_id: Union[str, int]) -> bool: return True
    async def is_creater_chat_false(self, id_user: Union[str, int], peer_id: Union[str, int]) -> bool: return False


    """bot_is_admin_in_chat"""
    async def bot_is_admin_in_chat(self, peer_id: Union[str, int]) -> bool: return True
    async def bot_is_admin_in_chat_false(self, peer_id: Union[str, int]) -> bool: return False


    """edit_message_chat & send_notif & send_message"""
    async def edit_message_chat(self, peer_id: Union[str, int], conversation_message_id: Union[str, int], message: str,
                                keyboard: tuple = None) -> None: return

    async def send_notif(self, peer_id: Union[str, int], event_id: Union[str, int], user_id: Union[str, int],
                         message: str) -> None: return

    async def send_message(self, peer_id: int, message_text: str) -> None: return


    """get_info_chat"""
    async def get_info_chat(self, peer_id: int) -> Union[MessagesGetConversationByIdExtended, MessagesGetConversationById]:
        pass


    """get_info_user"""
    async def get_info_user(self, user_id: int) -> List[UsersUserFull]: return TUser().get_data()


    """get_users_online"""
    async def get_users_online(self, peer_id: int) -> List[int]: return [689207910, 689207911, 689207912]
    async def get_users_online_void(self, peer_id: int) -> List[int]: return []