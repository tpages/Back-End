#
# Copyright (C) Halk-lai Liff <halkliff@pm.me> & Werberth Lins <werberth.lins@gmail.com>, 2018-present
# Distributed under GNU AGPLv3 License, found at the root tree of this source, by the name of LICENSE
# You can also find a copy of this license at GNU's site, as it follows <https://www.gnu.org/licenses/agpl-3.0.en.html>
#
# THIS SOFTWARE IS PRESENTED AS-IS, WITHOUT ANY WARRANTY, OR LIABILITY FROM ITS AUTHORS
# EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
# IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
# ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
# IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
# WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
# THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
# GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
# USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
# DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
# PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
# EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGES.
#

from pymodm import fields, MongoModel, EmbeddedMongoModel, connect
from pymongo import write_concern as wc, read_concern as rc, IndexModel, ReadPreference
from .config import *
from .post_models import BasePostModel as PostModel

connect(f'{MONGO_URI}/posts', alias='Posts', ssl=USE_SSL,
        username=DB_ADMIN_USERNAME, password=DB_ADMIN_PASSWORD)


class ReactionObj(EmbeddedMongoModel):
    emoji = fields.CharField(required=True, verbose_name='emoji', mongo_name='emoji')
    count = fields.IntegerField(required=True, verbose_name='reaction_count', mongo_name='count', min_value=0,
                                default=0)


class Reaction(EmbeddedMongoModel):
    """

    """
    reactions = fields.EmbeddedDocumentListField(ReactionObj, verbose_name='reactions_list', mongo_name='reactions')
    total_count = fields.BigIntegerField(required=True, verbose_name='total_count', mongo_name='totalCount',
                                         min_value=0, default=0)


class UserReaction(MongoModel):
    """

    """
    user_id = fields.BigIntegerField(verbose_name='user_id', mongo_name='userId', required=True)
    post = fields.ReferenceField(PostModel, on_delete=fields.ReferenceField.CASCADE,
                                 verbose_name='post_id', mongo_name='postId', required=True)
    reaction_index = fields.IntegerField(required=True, verbose_name='reaction_index', mongo_name='reactionIndex',
                                         min_value=0, max_value=3)
    reaction_date = fields.DateTimeField(required=True, verbose_name='reaction_date', mongo_name='reactionDate')

    class Meta:
        connection_alias = 'Posts'
        collection_name = 'reactions'
        cascade = True
        write_concern = wc.WriteConcern(j=True)
        read_preference = ReadPreference.NEAREST
        read_concern = rc.ReadConcern(level='majority')
        indexes = [
            IndexModel('userId', name='userReactionUserIdIndex', sparse=True),
            IndexModel('reactionIndex', name='userReactionReactionIndexIndex', sparse=True),
            IndexModel('reactionDate', name='userReactionDateIndex', sparse=True),
            IndexModel('postId', name='postIdIndex', sparse=True)
        ]
        ignore_unknown_fields = True
