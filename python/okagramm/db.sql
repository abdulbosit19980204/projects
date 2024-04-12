CREATE TABLE MyUser
(
    user               bigint,
    user_image         text,
    cover_image        text,
    follower_count     int,

    about_me           text,
    location           text,
    working_at         char,
    relationship       char,

    active             bool      default True,
    who_can_follow     bool      default False,
    show_my_activities bool      default True,
    search_engines     bool      default True,
    allow_commenting   bool      default True,

    created_at         timestamp default CURRENT_TIMESTAMP,
    updated_at         time      default now()
);


CREATE TABLE Post
(
    author            bigint,
    post_image        text,
    like_count        int,

    write_comment     bool      default True,
    disable_btn_title text      default 'Disable',

    created_at        timestamp default CURRENT_TIMESTAMP,
    updated_at        time      default now()
);

CREATE TABLE CommentPost
(
    post       bigint,
    author     bigint,
    message    text,

    created_at timestamp default CURRENT_TIMESTAMP,
    updated_at time      default now()
);

CREATE TABLE LikePost
(
    author     bigint,
    post       bigint,
    liked      bool,

    created_at timestamp default CURRENT_TIMESTAMP,
    updated_at time      default now()
);

CREATE TABLE FollowMyUser
(
    follower     bigint,
    following    bigint,
    follow       bool,
    follow_title text,

    created_at   timestamp default CURRENT_TIMESTAMP,
    updated_at   time      default now()
);

CREATE TABLE Notification
(
    user          bigint,
    reporter_user bigint,
    post          bigint,
    message       text,
    is_read       bool,


    created_at    timestamp default CURRENT_TIMESTAMP,
    updated_at    time      default now()
);