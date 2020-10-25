from models import PreVerifiedEmail, Club, Tag, NewClub

def fetch_aggregated_rso_list():
    # This pipeline will fill in the 'registered' and 'confirmed' fields into the RSO list
    return list(PreVerifiedEmail.objects.aggregate([
        {
            '$lookup': {
                'from': 'new_base_user',
                'localField': 'email',
                'foreignField': 'email',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$project': {
                '_id': 0,
                'email': 1,
                'registered': {
                    '$cond': [
                        { '$ifNull': [ '$user.registered_on', False] },
                        True,
                        False
                    ]
                },
                'confirmed': {
                    '$ifNull': [ '$user.confirmed', False ]
                }
            }
        }, {
            '$sort': {
                'email': 1
            }
        }
    ]))


def fetch_aggregated_club_list():
    # This pipeline will attach the 'confirmed' field with the list of clubs registered
    return list(Club.objects.aggregate([
        {
            '$lookup': {
                'from': 'user',
                'localField': 'owner',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$project': {
                'name': 1,
                'owner': 1,
                'confirmed': '$user.confirmed'
            }
        }, {
            '$sort': {
                'name': 1
            }
        }
    ]))


def fetch_aggregated_tag_list():
    # This pipeline will associate the tags with the number of clubs that have said tag
    return list(Tag.objects.aggregate([
        {
            '$lookup': {
                'from': 'club',
                'localField': '_id',
                'foreignField': 'tags',
                'as': 'associated_clubs'
            }
        }, {
            '$project': {
                'name': 1,
                'num_clubs': { '$size': '$associated_clubs' }
            }
        }
    ]))


def fetch_aggregated_social_media_usage():
    # This pipeline will count up the number of various social media links from all clubs available
    return list(Club.objects.aggregate([
        {
            '$lookup': {
                'from': 'user',
                'localField': 'owner',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'user.confirmed': True
            }
        }, {
            '$replaceRoot': {
                'newRoot': '$social_media_links'
            }
        }, {
            '$group': {
                '_id': 1,
                'website': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$website', '']}, 1, 0]
                    }
                },
                'facebook': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$facebook', '']}, 1, 0]
                    }
                },
                'instagram': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$instagram', '']}, 1, 0]
                    }
                },
                'linkedin': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$linkedin', '']}, 1, 0]
                    }
                },
                'twitter': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$twitter', '']}, 1, 0]
                    }
                },
                'youtube': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$youtube', '']}, 1, 0]
                    }
                },
                'github': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$github', '']}, 1, 0]
                    }
                },
                'behance': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$behance', '']}, 1, 0]
                    }
                },
                'medium': {
                    '$sum': {
                        '$cond': [{ '$ne': ['$medium', '']}, 1, 0]
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0
            }
        }
    ]));


def fetch_aggregated_club_requirement_stats():
    # This pipeline will count up the number of club requirements various social media links from all clubs available
    return list(Club.objects.aggregate([
        {
            '$lookup': {
                'from': 'user',
                'localField': 'owner',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'user.confirmed': True
            }
        }, {
            '$group': {
                '_id': 1,
                'app_required': {
                    '$sum': {
                        '$cond': ['$app_required', 1, 0]
                    }
                },
                'no_app_required': {
                    '$sum': {
                        '$cond': ['$app_required', 0, 1]
                    }
                },
                'new_members': {
                    '$sum': {
                        '$cond': ['$new_members', 1, 0]
                    }
                },
                'no_new_members': {
                    '$sum': {
                        '$cond': ['$new_members', 0, 1]
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0
            }
        }
    ]));

def fetch_aggregated_picture_stats():
    # This pipeline will count up the number of clubs having logo/banner pictures from all clubs available
    return list(Club.objects.aggregate([
        {
            '$lookup': {
                'from': 'user',
                'localField': 'owner',
                'foreignField': '_id',
                'as': 'user'
            }
        }, {
            '$unwind': {
                'path': '$user',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$match': {
                'user.confirmed': True
            }
        }, {
            '$group': {
                '_id': 1,
                'logo_pic': {
                    '$sum': {
                        '$cond': [
                            '$logo_url', 1, 0
                        ]
                    }
                },
                'no_logo_pic': {
                    '$sum': {
                        '$cond': [
                            '$logo_url', 0, 1
                        ]
                    }
                },
                'banner_pic': {
                    '$sum': {
                        '$cond': [
                            '$banner_url', 1, 0
                        ]
                    }
                },
                'no_banner_pic': {
                    '$sum': {
                        '$cond': [
                            '$banner_url', 0, 1
                        ]
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0
            }
        }
    ]))
